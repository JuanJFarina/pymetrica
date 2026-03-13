from pymetrica.metric_calculators import MaintainabilityIndexCalculator
from pymetrica.metric_calculators.maintainability_index.mi_metric import (
    MaintainabilityIndexResults,
)
from pymetrica.models import Codebase


def test_get_mi(
    mi_calculator: MaintainabilityIndexCalculator,
    codebase: Codebase,
    mi_result: MaintainabilityIndexResults,
) -> None:
    metric = mi_calculator.calculate_metric(codebase)
    assert metric.results.maintainability_index == mi_result.maintainability_index
    assert metric.results.normalized_mi == mi_result.normalized_mi
    assert len(metric.results.mi_per_layer) == 1
    for layer_result, expected_layer_result in zip(
        metric.results.mi_per_layer,
        mi_result.mi_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert (
            layer_result.maintainability_index
            == expected_layer_result.maintainability_index
        )
        assert layer_result.normalized_mi == expected_layer_result.normalized_mi


def test_get_mi_big(
    mi_calculator: MaintainabilityIndexCalculator,
    big_codebase: Codebase,
    big_codebase_mi_result: MaintainabilityIndexResults,
) -> None:
    metric = mi_calculator.calculate_metric(big_codebase)
    print(metric.results)
    assert (
        metric.results.maintainability_index
        == big_codebase_mi_result.maintainability_index
    )
    assert metric.results.normalized_mi == big_codebase_mi_result.normalized_mi
    assert len(metric.results.mi_per_layer) == 4
    for layer_result, expected_layer_result in zip(
        metric.results.mi_per_layer,
        big_codebase_mi_result.mi_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert (
            layer_result.maintainability_index
            == expected_layer_result.maintainability_index
        )
        assert layer_result.normalized_mi == expected_layer_result.normalized_mi
