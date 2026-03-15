from pymetrica.metric_calculators import MaintainabilityCostCalculator
from pymetrica.metric_calculators.maintainability_cost.mc_metric import (
    MaintainabilityCostResults,
)
from pymetrica.models import Codebase


def test_get_mc(
    mc_calculator: MaintainabilityCostCalculator,
    codebase: Codebase,
    mc_result: MaintainabilityCostResults,
) -> None:
    metric = mc_calculator.calculate_metric(codebase)
    assert metric.results.maintainability_cost == mc_result.maintainability_cost
    assert len(metric.results.mc_per_layer) == 1
    for idx, file in enumerate(metric.results.mc_per_layer):
        assert file.name == mc_result.mc_per_layer[idx].name
        assert (
            file.maintainability_cost
            == mc_result.mc_per_layer[idx].maintainability_cost
        )


def test_get_mc_big(
    mc_calculator: MaintainabilityCostCalculator,
    big_codebase: Codebase,
    big_codebase_mc_result: MaintainabilityCostResults,
) -> None:
    metric = mc_calculator.calculate_metric(big_codebase)
    assert (
        metric.results.maintainability_cost
        == big_codebase_mc_result.maintainability_cost
    )
    assert len(metric.results.mc_per_layer) == 4
    metric.results.mc_per_layer.sort(key=lambda x: x.name)
    big_codebase_mc_result.mc_per_layer.sort(key=lambda x: x.name)
    metric.results.mc_per_layer.sort(key=lambda x: x.name)
    big_codebase_mc_result.mc_per_layer.sort(key=lambda x: x.name)
    for idx, file in enumerate(metric.results.mc_per_layer):
        assert file.name == big_codebase_mc_result.mc_per_layer[idx].name
        assert (
            file.maintainability_cost
            == big_codebase_mc_result.mc_per_layer[idx].maintainability_cost
        )
