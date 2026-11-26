from pathlib import Path

from pymetrica.metric_calculators.architecture_stats.diagram_generator import (
    create_diagram,
    graph_to_mermaid,
)
from pymetrica.models import Edge, Graph, Node


def test_renders_modules_in_nested_package_subgraphs() -> None:
    graph = Graph(
        nodes=[
            Node(name="acme.main", dependencies=["acme.api.routes"]),
            Node(name="acme.api.routes", dependencies=[]),
        ],
        edges=[
            Edge(
                source="acme.main",
                target="acme.api.routes",
                weight=1,
            ),
        ],
    )
    expected = (
        "flowchart LR\n"
        '    subgraph package_0["acme"]\n'
        "        direction TB\n"
        '        module_1["main"]\n'
        '        subgraph package_1["api"]\n'
        "            direction TB\n"
        '            module_0["routes"]\n'
        "        end\n"
        "    end\n"
        "    module_1 --> module_0"
    )

    assert graph_to_mermaid(graph) == expected


def test_writes_diagram_to_file(tmp_path: Path) -> None:
    output = tmp_path / "architecture.mmd"

    diagram = create_diagram(Graph(nodes=[], edges=[]), str(output))

    assert diagram == "flowchart LR"
    assert output.read_text(encoding="utf-8") == "flowchart LR\n"


def test_renders_dependency_on_package_subgraph() -> None:
    graph = Graph(
        nodes=[
            Node(name="acme.__main__", dependencies=["acme.api"]),
            Node(name="acme.api.app", dependencies=[]),
        ],
        edges=[
            Edge(source="acme.__main__", target="acme.api", weight=1),
        ],
    )

    assert "    module_0 --> package_1" in graph_to_mermaid(graph)
