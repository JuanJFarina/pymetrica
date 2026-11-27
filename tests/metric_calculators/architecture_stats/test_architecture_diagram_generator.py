from pathlib import Path

from pymetrica.metric_calculators.architecture_stats.diagram_generator import (
    architecture_to_mermaid,
    create_diagram,
)
from pymetrica.models import Component, Container, Dependency


def _architecture() -> Container:
    routes = Component(
        hash="a" * 64,
        name="acme.api.routes",
        depth_level=2,
        parent_container_name="acme.api",
        concrete_modules=["acme.api.routes"],
        dependencies=[],
    )
    api = Container(
        hash="api",
        name="acme.api",
        depth_level=1,
        parent_container_name="acme",
        concrete_packages=["acme.api"],
        childs=[routes],
    )
    main = Component(
        hash="b" * 64,
        name="acme.main",
        depth_level=1,
        parent_container_name="acme",
        concrete_modules=["acme.main"],
        dependencies=[
            Dependency(
                target="acme.api.routes",
                weight=5,
            ),
        ],
    )
    return Container(
        hash="acme",
        name="acme",
        depth_level=0,
        parent_container_name=None,
        concrete_packages=["acme"],
        childs=[main, api],
    )


def test_renders_components_in_nested_container_subgraphs() -> None:
    expected = (
        '%%{init: {"themeCSS": ".cluster rect { stroke-width: 4px !important;} '
        ".edgeLabel {font-size: 30px;} .cluster-label "
        '{font-size: 20px !important;}"}}%%\n\n'
        "flowchart TB\n"
        '    subgraph container_0["acme"]\n'
        "        direction TB\n"
        '        component_bbbbbbbbbbbbbbbb["main"]\n'
        '        subgraph container_1["api"]\n'
        "            direction TB\n"
        '            component_aaaaaaaaaaaaaaaa["routes"]\n'
        "        end\n"
        "    end\n"
        "    component_bbbbbbbbbbbbbbbb -->|5| component_aaaaaaaaaaaaaaaa"
    )

    assert architecture_to_mermaid(_architecture()) == expected


def test_writes_diagram_to_file(tmp_path: Path) -> None:
    output = tmp_path / "architecture.mmd"

    diagram = create_diagram(_architecture(), str(output))

    assert output.read_text(encoding="utf-8") == f"{diagram}\n"


def test_renders_dependency_on_container_subgraph() -> None:
    architecture = _architecture()
    main = next(child for child in architecture.childs if isinstance(child, Component))
    main.dependencies = [
        Dependency(target="acme.api", weight=2),
    ]

    assert (
        "    component_bbbbbbbbbbbbbbbb -->|2| container_1"
        in architecture_to_mermaid(architecture)
    )
