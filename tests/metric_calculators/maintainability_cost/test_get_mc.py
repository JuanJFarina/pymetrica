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
    assert metric.results.mc_per_layer[0].name == mc_result.mc_per_layer[0].name
    assert (
        metric.results.mc_per_layer[0].maintainability_cost
        == mc_result.mc_per_layer[0].maintainability_cost
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
    result_layers = metric.results.mc_per_layer
    expected_layers = big_codebase_mc_result.mc_per_layer
    assert result_layers[0].name == expected_layers[0].name
    assert (
        result_layers[0].maintainability_cost == expected_layers[0].maintainability_cost
    )
    assert result_layers[1].name == expected_layers[1].name
    assert (
        result_layers[1].maintainability_cost == expected_layers[1].maintainability_cost
    )
    assert result_layers[2].name == expected_layers[2].name
    assert (
        result_layers[2].maintainability_cost == expected_layers[2].maintainability_cost
    )
    assert result_layers[3].name == expected_layers[3].name
    assert (
        result_layers[3].maintainability_cost == expected_layers[3].maintainability_cost
    )
