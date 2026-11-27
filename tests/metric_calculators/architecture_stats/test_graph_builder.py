from hashlib import sha256
from pathlib import Path

from pymetrica.codebase_parser import parse_codebase
from pymetrica.metric_calculators.architecture_stats.graph_builder import create_graph
from pymetrica.models import Codebase


def test_creates_deterministic_internal_dependency_graph(
    big_codebase: Codebase,
) -> None:
    graph = create_graph(big_codebase)

    assert [node.name for node in graph.nodes] == [
        "big_codebase.exception_handlers.codebase_exception",
        "big_codebase.main",
        "big_codebase.middlewares.logging_middleware",
        "big_codebase.routes.routes",
    ]
    assert {node.name: node.dependencies for node in graph.nodes}[
        "big_codebase.main"
    ] == [
        "big_codebase.exception_handlers.codebase_exception",
        "big_codebase.middlewares.logging_middleware",
        "big_codebase.routes.routes",
    ]
    assert [(edge.source, edge.target, edge.weight) for edge in graph.edges] == [
        (
            "big_codebase.main",
            "big_codebase.exception_handlers.codebase_exception",
            1,
        ),
        (
            "big_codebase.main",
            "big_codebase.middlewares.logging_middleware",
            1,
        ),
        ("big_codebase.main", "big_codebase.routes.routes", 1),
    ]


def test_creates_graph_from_src_layout(tmp_path: Path) -> None:
    source_root = tmp_path / "src"
    package = source_root / "acme"
    api = package / "api"
    api.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (api / "__init__.py").write_text("", encoding="utf-8")
    (api / "routes.py").write_text(
        "def create_router(): ...\n",
        encoding="utf-8",
    )
    (package / "main.py").write_text(
        "from acme.api.routes import create_router\n",
        encoding="utf-8",
    )

    graph = create_graph(parse_codebase(str(source_root)))

    assert [node.name for node in graph.nodes] == [
        "acme.api.routes",
        "acme.main",
    ]
    assert [(edge.source, edge.target) for edge in graph.edges] == [
        ("acme.main", "acme.api.routes"),
    ]
    node_hashes = {node.name: node.code_hash for node in graph.nodes}
    assert (
        node_hashes["acme.api.routes"]
        == sha256(
            b"def create_router(): ...\n",
        ).hexdigest()
    )


def test_preserves_dependency_on_symbol_defined_in_package_init(
    tmp_path: Path,
) -> None:
    package = tmp_path / "acme"
    api = package / "api"
    api.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "__main__.py").write_text(
        "from .api import run_backend\n",
        encoding="utf-8",
    )
    (api / "__init__.py").write_text(
        "def run_backend(): ...\n",
        encoding="utf-8",
    )
    (api / "app.py").write_text("app = object()\n", encoding="utf-8")

    graph = create_graph(parse_codebase(str(package)))

    assert {node.name: node.dependencies for node in graph.nodes}["acme.__main__"] == [
        "acme.api"
    ]
    assert [(edge.source, edge.target) for edge in graph.edges] == [
        ("acme.__main__", "acme.api"),
    ]
