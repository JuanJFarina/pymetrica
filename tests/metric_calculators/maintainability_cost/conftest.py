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
            maintainability_cost=19.574690937560025,
        ),
    ]


@pytest.fixture
def mc_result(small_layer_mc: list[LayerMC]) -> MaintainabilityCostResults:
    return MaintainabilityCostResults(
        maintainability_cost=20.45535870744911,
        mc_per_layer=small_layer_mc,
    )


@pytest.fixture(name="big_layer_mc")
def _big_layer_mc() -> list[LayerMC]:
    return [
        LayerMC(name="exception_handlers", maintainability_cost=0.03),
        LayerMC(name="middlewares", maintainability_cost=0.075),
        LayerMC(name="routes", maintainability_cost=0.035),
        LayerMC(name="root", maintainability_cost=1.3773140495867768),
    ]


@pytest.fixture
def big_codebase_mc_result(big_layer_mc: list[LayerMC]) -> MaintainabilityCostResults:
    return MaintainabilityCostResults(
        maintainability_cost=1.2876720012216316,
        mc_per_layer=big_layer_mc,
    )
