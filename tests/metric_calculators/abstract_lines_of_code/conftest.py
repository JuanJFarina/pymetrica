import pytest

from pymetrica.metric_calculators import AlocCalculator
from pymetrica.metric_calculators.abstract_lines_of_code.aloc_metric import (
    AlocResults,
    LayerAloc,
)


@pytest.fixture
def aloc_calculator() -> AlocCalculator:
    return AlocCalculator()


@pytest.fixture
def aloc_result() -> AlocResults:
    return AlocResults(
        aloc_number=6,
        aloc_percentage=15.0,
        aloc_result_per_layer=[
            LayerAloc(
                name="root",
                aloc_number=6,
                aloc_percentage=15.0,
            ),
        ],
    )


@pytest.fixture(name="_big_codebase_layers_result")
def _big_codebase_layers_result() -> list[LayerAloc]:
    return [
        LayerAloc(
            name="middlewares",
            aloc_number=7,
            aloc_percentage=17.94871794871795,
        ),
        LayerAloc(
            name="exception_handlers",
            aloc_number=5,
            aloc_percentage=12.82051282051282,
        ),
        LayerAloc(
            name="routes",
            aloc_number=5,
            aloc_percentage=12.82051282051282,
        ),
        LayerAloc(
            name="root",
            aloc_number=5,
            aloc_percentage=12.82051282051282,
        ),
    ]


@pytest.fixture
def big_codebase_aloc_result(
    _big_codebase_layers_result: list[LayerAloc],
) -> AlocResults:
    return AlocResults(
        aloc_number=22,
        aloc_percentage=56.41025641025641,
        aloc_result_per_layer=_big_codebase_layers_result,
    )
