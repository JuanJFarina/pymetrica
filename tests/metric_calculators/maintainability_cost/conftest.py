import pytest

from pymetrica.metric_calculators import MaintainabilityCostCalculator
from pymetrica.metric_calculators.maintainability_cost.mc_metric import (
    LayerMC,
    MaintainabilityCostResults,
)


@pytest.fixture
def mc_calculator() -> MaintainabilityCostCalculator:
    return MaintainabilityCostCalculator()


@pytest.fixture(name="small_layer_mc")
def _small_layer_mc() -> list[LayerMC]:
    return [
        LayerMC(
            name="root",
            maintainability_cost=48.47672734390006,
            raw_line_cost=48.43672734390006,
        ),
    ]


@pytest.fixture
def mc_result(small_layer_mc: list[LayerMC]) -> MaintainabilityCostResults:
    return MaintainabilityCostResults(
        maintainability_cost=50.678396768622775,
        raw_line_cost=50.638396768622776,
        mc_per_layer=small_layer_mc,
    )


@pytest.fixture(name="big_layer_mc")
def _big_layer_mc() -> list[LayerMC]:
    return [
        LayerMC(
            name="exception_handlers",
            maintainability_cost=0.4048594761554029,
            raw_line_cost=0.3988594761554029,
        ),
        LayerMC(
            name="middlewares",
            maintainability_cost=0.3108496250072116,
            raw_line_cost=0.29584962500721157,
        ),
        LayerMC(
            name="routes",
            maintainability_cost=0.2900290179859208,
            raw_line_cost=0.2830290179859208,
        ),
        LayerMC(
            name="root",
            maintainability_cost=3.316785123966943,
            raw_line_cost=3.3057851239669427,
        ),
    ]


@pytest.fixture
def big_codebase_mc_result(big_layer_mc: list[LayerMC]) -> MaintainabilityCostResults:
    return MaintainabilityCostResults(
        maintainability_cost=2.770680003054079,
        raw_line_cost=2.7316800030540787,
        mc_per_layer=big_layer_mc,
    )
