from collections import defaultdict
from pathlib import Path

from pymetrica.models import Graph, Node

PackagePath = tuple[str, ...]


def _register_package(
    package: PackagePath,
    child_packages: dict[PackagePath, set[PackagePath]],
) -> None:
    for depth in range(1, len(package) + 1):
        parent = package[: depth - 1]
        child_packages.setdefault(parent, set()).add(package[:depth])


def _element_id(
    name: str,
    node_ids: dict[str, str],
    package_ids: dict[PackagePath, str],
) -> str:
    if name in node_ids:
        return node_ids[name]
    return package_ids[tuple(name.split("."))]


def graph_to_mermaid(graph: Graph) -> str:
    nodes = sorted(graph.nodes, key=lambda node: node.name)
    node_ids = {node.name: f"module_{index}" for index, node in enumerate(nodes)}
    modules_by_package = defaultdict[PackagePath, list[Node]](list)
    child_packages = defaultdict[PackagePath, set[PackagePath]](set)

    for node in nodes:
        package = tuple(node.name.split("."))[:-1]
        modules_by_package[package].append(node)
        _register_package(package, child_packages)

    for edge in graph.edges:
        if edge.target not in node_ids:
            _register_package(tuple(edge.target.split(".")), child_packages)

    package_ids = {
        package: f"package_{index}"
        for index, package in enumerate(
            sorted(
                package for children in child_packages.values() for package in children
            ),
        )
    }
    lines = ["flowchart LR"]

    def render_package(package: PackagePath, indent: int) -> None:
        prefix = "    " * indent
        lines.append(
            f'{prefix}subgraph {package_ids[package]}["{package[-1]}"]',
        )
        lines.append(f"{prefix}    direction TB")

        for node in modules_by_package[package]:
            module_label = node.name.rsplit(".", maxsplit=1)[-1]
            lines.append(
                f'{prefix}    {node_ids[node.name]}["{module_label}"]',
            )

        for child in sorted(child_packages[package]):
            render_package(child, indent + 1)

        lines.append(f"{prefix}end")

    for node in modules_by_package[()]:
        lines.append(f'    {node_ids[node.name]}["{node.name}"]')

    for root_package in sorted(child_packages[()]):
        render_package(root_package, indent=1)

    for edge in sorted(graph.edges, key=lambda edge: (edge.source, edge.target)):
        lines.append(
            f"    {_element_id(edge.source, node_ids, package_ids)}"
            f" --> {_element_id(edge.target, node_ids, package_ids)}",
        )

    return "\n".join(lines)


def create_diagram(graph: Graph, filename: str | None = None) -> str:
    diagram = graph_to_mermaid(graph)
    if filename:
        Path(filename).write_text(f"{diagram}\n", encoding="utf-8")
    return diagram
