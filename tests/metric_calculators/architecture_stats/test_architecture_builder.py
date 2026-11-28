import pytest

from pymetrica.metric_calculators.architecture_stats.architecture_builder import (
    from_graph_to_architecture,
)
from pymetrica.models import Component, Container, Dependency, Edge, Graph, Node


def _child(container: Container, name: str) -> Component | Container:
    return next(child for child in container.childs if child.name == name)


def test_builds_depth_limited_architecture_and_projects_dependencies() -> None:
    graph = Graph(
        nodes=[
            Node(
                name="acme.main",
                dependencies=["acme.api.routes.healthcheck"],
            ),
            Node(
                name="acme.api.routes.healthcheck",
                dependencies=["acme.domain.service"],
            ),
            Node(
                name="acme.api.routes.salary",
                dependencies=["acme.domain.service"],
            ),
            Node(name="acme.domain.service", dependencies=[]),
        ],
        edges=[
            Edge(
                source="acme.main",
                target="acme.api.routes.healthcheck",
                weight=1,
            ),
            Edge(
                source="acme.api.routes.healthcheck",
                target="acme.domain.service",
                weight=2,
            ),
            Edge(
                source="acme.api.routes.salary",
                target="acme.domain.service",
                weight=3,
            ),
        ],
    )

    architecture = from_graph_to_architecture(
        graph,
        max_container_levels=2,
    )

    assert architecture.name == "acme"
    assert architecture.depth_level == 0
    assert architecture.parent_container_name is None
    assert architecture.concrete_packages == ["acme"]

    api = _child(architecture, "acme.api")
    domain = _child(architecture, "acme.domain")
    main = _child(architecture, "acme.main")
    assert isinstance(api, Container)
    assert isinstance(domain, Container)
    assert isinstance(main, Component)

    routes = _child(api, "acme.api.routes")
    service = _child(domain, "acme.domain.service")
    assert isinstance(routes, Component)
    assert isinstance(service, Component)
    assert routes.concrete_modules == [
        "acme.api.routes.healthcheck",
        "acme.api.routes.salary",
    ]
    assert routes.dependencies == [
        Dependency(target="acme.domain.service", weight=5),
    ]
    assert main.dependencies == [
        Dependency(target="acme.api.routes", weight=1),
    ]
    serialized_routes = next(
        child
        for child in next(
            child
            for child in architecture.model_dump()["childs"]
            if child["name"] == "acme.api"
        )["childs"]
        if child["name"] == "acme.api.routes"
    )
    assert serialized_routes["concrete_modules"] == routes.concrete_modules


def test_projects_dependencies_targeting_package_initializers() -> None:
    graph = Graph(
        nodes=[
            Node(name="acme.__main__", dependencies=["acme.api"]),
            Node(name="acme.api.app", dependencies=["acme"]),
        ],
        edges=[
            Edge(source="acme.__main__", target="acme.api", weight=1),
            Edge(source="acme.api.app", target="acme", weight=1),
        ],
    )

    architecture = from_graph_to_architecture(
        graph,
        max_container_levels=2,
    )

    api = _child(architecture, "acme.api")
    main = _child(architecture, "acme.__main__")
    assert isinstance(api, Container)
    assert isinstance(main, Component)
    app = _child(api, "acme.api.app")
    assert isinstance(app, Component)
    assert main.dependencies == [Dependency(target="acme.api", weight=1)]
    assert app.dependencies == []


def test_groups_dependencies_by_target_container_and_sums_weights() -> None:
    graph = Graph(
        nodes=[
            Node(
                name="acme.api.source",
                dependencies=[
                    "acme.api.sibling",
                    "acme.domain.first",
                    "acme.domain.second",
                ],
            ),
            Node(name="acme.api.sibling", dependencies=[]),
            Node(name="acme.domain.first", dependencies=[]),
            Node(name="acme.domain.second", dependencies=[]),
        ],
        edges=[
            Edge(
                source="acme.api.source",
                target="acme.api.sibling",
                weight=4,
            ),
            Edge(
                source="acme.api.source",
                target="acme.domain.first",
                weight=2,
            ),
            Edge(
                source="acme.api.source",
                target="acme.domain.second",
                weight=3,
            ),
        ],
    )

    architecture = from_graph_to_architecture(
        graph,
        max_container_levels=2,
        group_deps_to_container=True,
    )

    api = _child(architecture, "acme.api")
    assert isinstance(api, Container)
    source = _child(api, "acme.api.source")
    assert isinstance(source, Component)
    assert source.dependencies == [
        Dependency(target="acme.domain", weight=5),
    ]


def test_preserves_dependency_targeting_root_component_when_grouping() -> None:
    graph = Graph(
        nodes=[
            Node(
                name="acme.api.source",
                dependencies=["acme.settings"],
            ),
            Node(name="acme.settings", dependencies=[]),
        ],
        edges=[
            Edge(
                source="acme.api.source",
                target="acme.settings",
                weight=2,
            ),
        ],
    )

    architecture = from_graph_to_architecture(
        graph,
        max_container_levels=1,
        group_deps_to_container=True,
    )

    source = _child(architecture, "acme.api")
    assert isinstance(source, Component)
    assert source.dependencies == [
        Dependency(target="acme.settings", weight=2),
    ]


def test_omits_dependency_targeting_root_container_without_grouping() -> None:
    graph = Graph(
        nodes=[
            Node(name="acme.api.app", dependencies=["acme"]),
        ],
        edges=[
            Edge(
                source="acme.api.app",
                target="acme",
                weight=1,
            ),
        ],
    )

    architecture = from_graph_to_architecture(
        graph,
        max_container_levels=1,
        group_deps_to_container=False,
    )

    api = _child(architecture, "acme.api")
    assert isinstance(api, Component)
    assert api.dependencies == []


def test_component_hash_tracks_grouped_module_content_deterministically() -> None:
    def build_hash(
        second_module_hash: str,
        *,
        reverse_nodes: bool = False,
    ) -> str:
        nodes = [
            Node(
                name="acme.routes.first",
                dependencies=[],
                code_hash="a" * 64,
            ),
            Node(
                name="acme.routes.second",
                dependencies=[],
                code_hash=second_module_hash,
            ),
        ]
        architecture = from_graph_to_architecture(
            Graph(
                nodes=list(reversed(nodes)) if reverse_nodes else nodes,
                edges=[],
            ),
            max_container_levels=1,
        )
        routes = _child(architecture, "acme.routes")
        assert isinstance(routes, Component)
        return routes.hash

    original_hash = build_hash("b" * 64)

    assert original_hash == build_hash("b" * 64, reverse_nodes=True)
    assert original_hash != build_hash("c" * 64)


def test_rejects_container_depth_below_one() -> None:
    with pytest.raises(ValueError):
        from_graph_to_architecture(
            Graph(nodes=[], edges=[]),
            max_container_levels=0,
        )
