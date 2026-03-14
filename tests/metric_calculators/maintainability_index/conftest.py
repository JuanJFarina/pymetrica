import pytest

from pymetrica.metric_calculators import MaintainabilityIndexCalculator
from pymetrica.metric_calculators.maintainability_index.mi_metric import (
    LayerMI,
    MaintainabilityIndexResults,
)


@pytest.fixture
def mi_calculator() -> MaintainabilityIndexCalculator:
    return MaintainabilityIndexCalculator()


@pytest.fixture
def small_layer_mi() -> list[LayerMI]:
    return [
        LayerMI(
            name="root",
            maintainability_index=163.22011763251447,
            normalized_mi=95.45036118860496,
        )
    ]


@pytest.fixture
def mi_result(small_layer_mi: list[LayerMI]) -> MaintainabilityIndexResults:
    return MaintainabilityIndexResults(
        maintainability_index=163.14511763251448,
        normalized_mi=95.40650153948216,
        mi_per_layer=[],
    )


@pytest.fixture
def big_layer_mi() -> list[LayerMI]:
    return [
        LayerMI(
            name="root",
            maintainability_index=168.26668760482232,
            normalized_mi=98.40157169872651,
        )
    ]


@pytest.fixture
def big_codebase_mi_result() -> MaintainabilityIndexResults:
    return MaintainabilityIndexResults(
        maintainability_index=165.44855242617115,
        normalized_mi=96.75353943050943,
        mi_per_layer=[],
    )
