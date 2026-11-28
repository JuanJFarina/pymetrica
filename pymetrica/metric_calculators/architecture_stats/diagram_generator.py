from pathlib import Path

from pymetrica.models import Component, Container

MERMAID_INIT_DIRECTIVE = (
    '%%{init: {"themeCSS": ".cluster rect { stroke-width: 4px !important;} '
    ".edgeLabel {font-size: 30px;} .cluster-label "
    '{font-size: 20px !important;}"}}%%'
)
COMPONENT_HASH_PREFIX_LENGTH = 16


def _abstraction_id(
    name: str,
    component_ids: dict[str, str],
    container_ids: dict[str, str],
) -> str:
    if name in component_ids:
        return component_ids[name]
    if name in container_ids:
        return container_ids[name]
    raise ValueError(f"Unknown architecture dependency target: {name}")


def _collect_abstractions(
    root: Container,
) -> tuple[list[Container], list[Component]]:
    containers = [root]
    components = list[Component]()
    for child in root.childs:
        if isinstance(child, Container):
            child_containers, child_components = _collect_abstractions(child)
            containers.extend(child_containers)
            components.extend(child_components)
        else:
            components.append(child)
    return containers, components


def architecture_to_mermaid(architecture: Container) -> str:
    containers, components = _collect_abstractions(architecture)
    containers.sort(key=lambda container: container.name)
    components.sort(key=lambda component: component.name)
    container_ids = {
        container.name: f"container_{index}"
        for index, container in enumerate(containers)
    }
    component_ids = {
        component.name: (f"component_{component.hash[:COMPONENT_HASH_PREFIX_LENGTH]}")
        for component in components
    }
    if len(set(component_ids.values())) != len(component_ids):
        raise ValueError("Component hash prefix collision")
    lines = [MERMAID_INIT_DIRECTIVE, "", "flowchart TB"]

    def render_container(container: Container, indent: int) -> None:
        prefix = "    " * indent
        lines.append(
            f"{prefix}subgraph {container_ids[container.name]}"
            f'["{container.name.rsplit(".", maxsplit=1)[-1]}"]',
        )
        lines.append(f"{prefix}    direction TB")
        direct_components = sorted(
            (child for child in container.childs if isinstance(child, Component)),
            key=lambda component: component.name,
        )
        child_containers = sorted(
            (child for child in container.childs if isinstance(child, Container)),
            key=lambda child_container: child_container.name,
        )
        for component in direct_components:
            lines.append(
                f"{prefix}    {component_ids[component.name]}"
                f'["{component.name.rsplit(".", maxsplit=1)[-1]}"]',
            )
        for child in child_containers:
            render_container(child, indent + 1)
        lines.append(f"{prefix}end")

    render_container(architecture, indent=1)
    for component in components:
        for dependency in sorted(
            component.dependencies,
            key=lambda item: item.target,
        ):
            target_id = _abstraction_id(
                dependency.target,
                component_ids,
                container_ids,
            )
            lines.append(
                f"    {component_ids[component.name]}"
                f" -->|{dependency.weight}| {target_id}",
            )

    return "\n".join(lines)


def create_diagram(
    architecture: Container,
    filename: str | None = None,
) -> str:
    diagram = architecture_to_mermaid(architecture)
    if filename:
        Path(filename).write_text(f"{diagram}\n", encoding="utf-8")
    return diagram
