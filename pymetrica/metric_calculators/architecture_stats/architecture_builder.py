from collections import Counter
from hashlib import sha256
from json import dumps

from pymetrica.models import Component, Container, Dependency, Graph

PackagePath = tuple[str, ...]
SYNTHETIC_ROOT = "<root>"


def _stable_hash(kind: str, name: str) -> str:
    return sha256(f"{kind}:{name}".encode()).hexdigest()


def _component_code_hash(
    component_name: str,
    concrete_modules: list[str],
    module_hashes: dict[str, str],
) -> str:
    payload = {
        "component": component_name,
        "modules": [
            {
                "name": module_name,
                "code_hash": module_hashes[module_name],
            }
            for module_name in sorted(concrete_modules)
        ],
    }
    serialized = dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(serialized.encode()).hexdigest()


def _package_paths(graph: Graph) -> set[PackagePath]:
    module_names = {node.name for node in graph.nodes}
    paths = set[PackagePath]()

    def add_with_parents(package: PackagePath) -> None:
        paths.update(package[:depth] for depth in range(1, len(package) + 1))

    for node in graph.nodes:
        add_with_parents(tuple(node.name.split("."))[:-1])
    for edge in graph.edges:
        if edge.source not in module_names:
            add_with_parents(tuple(edge.source.split(".")))
        if edge.target not in module_names:
            add_with_parents(tuple(edge.target.split(".")))

    return paths


def _root_name(
    graph: Graph,
    package_paths: set[PackagePath],
) -> tuple[str, bool]:
    top_level_packages = {path[0] for path in package_paths if path}
    has_root_modules = any("." not in node.name for node in graph.nodes)
    if len(top_level_packages) == 1 and not has_root_modules:
        return next(iter(top_level_packages)), False
    return SYNTHETIC_ROOT, True


def _new_container(
    name: str,
    depth_level: int,
    parent_container_name: str | None,
    concrete_packages: list[str],
) -> Container:
    return Container(
        hash=_stable_hash("container", name),
        name=name,
        depth_level=depth_level,
        parent_container_name=parent_container_name,
        concrete_packages=concrete_packages,
        childs=[],
    )


def _new_component(
    name: str,
    parent: Container,
) -> Component:
    return Component(
        hash=_stable_hash("component", name),
        name=name,
        depth_level=parent.depth_level + 1,
        parent_container_name=parent.name,
        concrete_modules=[],
        dependencies=[],
    )


class _ArchitectureBuilder:
    def __init__(self, graph: Graph, max_container_levels: int) -> None:
        self.graph = graph
        self.package_paths = _package_paths(graph)
        root_name, synthetic_root = _root_name(graph, self.package_paths)
        self.max_package_parts = (
            max_container_levels - 1 if synthetic_root else max_container_levels
        )
        self.root = _new_container(
            name=root_name,
            depth_level=0,
            parent_container_name=None,
            concrete_packages=[] if synthetic_root else [root_name],
        )
        self.containers = {self.root.name: self.root}
        self.components = dict[str, Component]()
        self.owner_by_concrete_name = dict[str, str]()

    def build(self, group_deps_to_container: bool) -> Container:
        self._build_containers()
        self._build_components()
        self._map_packages()
        self._hash_components()
        self._project_dependencies(group_deps_to_container)
        self._sort_architecture(self.root)
        return self.root

    def _build_containers(self) -> None:
        for package in sorted(
            self.package_paths,
            key=lambda path: (len(path), path),
        ):
            if len(package) > self.max_package_parts:
                continue
            name = ".".join(package)
            if name == self.root.name:
                continue
            parent_name = ".".join(package[:-1]) if package[:-1] else self.root.name
            parent = self.containers[parent_name]
            container = _new_container(
                name=name,
                depth_level=parent.depth_level + 1,
                parent_container_name=parent.name,
                concrete_packages=[name],
            )
            self.containers[name] = container
            parent.childs.append(container)

    def _ensure_component(self, name: str, parent_name: str) -> Component:
        if name not in self.components:
            component = _new_component(name, self.containers[parent_name])
            self.components[name] = component
            self.containers[parent_name].childs.append(component)
        return self.components[name]

    def _build_components(self) -> None:
        for node in sorted(self.graph.nodes, key=lambda item: item.name):
            package = tuple(node.name.split("."))[:-1]
            parent_name = ".".join(package[: self.max_package_parts]) or self.root.name
            component_name = node.name
            if len(package) > self.max_package_parts:
                component_name = ".".join(
                    package[: self.max_package_parts + 1],
                )
            component = self._ensure_component(component_name, parent_name)
            component.concrete_modules.append(node.name)
            self.owner_by_concrete_name[node.name] = component.name

    def _map_packages(self) -> None:
        module_names = {node.name for node in self.graph.nodes}
        for package in self.package_paths:
            package_name = ".".join(package)
            if package_name in module_names:
                continue
            if len(package) <= self.max_package_parts:
                self.owner_by_concrete_name[package_name] = package_name
                continue
            parent_name = ".".join(package[: self.max_package_parts]) or self.root.name
            component_name = ".".join(
                package[: self.max_package_parts + 1],
            )
            self._ensure_component(component_name, parent_name)
            self.owner_by_concrete_name[package_name] = component_name

    def _hash_components(self) -> None:
        module_hashes = {node.name: node.code_hash for node in self.graph.nodes}
        for component in self.components.values():
            component.hash = _component_code_hash(
                component.name,
                component.concrete_modules,
                module_hashes,
            )

    def _dependency_target(
        self,
        source: str,
        target: str,
        group_deps_to_container: bool,
    ) -> str | None:
        projected_target = target
        if group_deps_to_container:
            target_component = self.components.get(target)
            if (
                target_component is not None
                and target_component.parent_container_name != self.root.name
            ):
                projected_target = target_component.parent_container_name
        if self._targets_ancestor_container(source, projected_target):
            return None
        return projected_target

    def _targets_ancestor_container(self, source: str, target: str) -> bool:
        if target not in self.containers:
            return False
        source_component = self.components.get(source)
        if source_component is None:
            return False
        parent_name = source_component.parent_container_name
        while parent_name is not None:
            if parent_name == target:
                return True
            parent = self.containers[parent_name]
            parent_name = parent.parent_container_name
        return False

    def _project_dependencies(self, group_deps_to_container: bool) -> None:
        dependencies = {name: Counter[str]() for name in self.components}
        for edge in self.graph.edges:
            source = self.owner_by_concrete_name.get(edge.source)
            target = self.owner_by_concrete_name.get(edge.target)
            if source is None or target is None:
                continue
            target = self._dependency_target(
                source,
                target,
                group_deps_to_container,
            )
            if target is None or source == target:
                continue
            if source in dependencies:
                dependencies[source][target] += edge.weight

        for name, component in self.components.items():
            component.concrete_modules.sort()
            component.dependencies = [
                Dependency(target=target, weight=weight)
                for target, weight in sorted(dependencies[name].items())
            ]

    def _sort_architecture(self, container: Container) -> None:
        for child in container.childs:
            if isinstance(child, Container):
                self._sort_architecture(child)
        container.childs.sort(key=lambda child: child.name)


def from_graph_to_architecture(
    graph: Graph,
    max_container_levels: int = 1,
    group_deps_to_container: bool = False,
) -> Container:
    if max_container_levels < 1:
        raise ValueError("max_container_levels must be at least 1")
    return _ArchitectureBuilder(graph, max_container_levels).build(
        group_deps_to_container,
    )
