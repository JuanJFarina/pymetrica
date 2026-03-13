from pymetrica.metric_calculators import AlocCalculator
from pymetrica.metric_calculators.abstract_lines_of_code.aloc_metric import AlocResults
from pymetrica.models import Codebase


def test_get_aloc(
    aloc_calculator: AlocCalculator,
    codebase: Codebase,
    aloc_result: AlocResults,
) -> None:
    metric = aloc_calculator.calculate_metric(codebase)
    assert metric.results.aloc_number == aloc_result.aloc_number
    assert metric.results.aloc_percentage == aloc_result.aloc_percentage
    assert len(metric.results.aloc_result_per_layer) == 1
    for layer_result, expected_layer_result in zip(
        metric.results.aloc_result_per_layer,
        aloc_result.aloc_result_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert layer_result.aloc_number == expected_layer_result.aloc_number
        assert layer_result.aloc_percentage == expected_layer_result.aloc_percentage


def test_get_aloc_big(
    aloc_calculator: AlocCalculator,
    big_codebase: Codebase,
    big_codebase_aloc_result: AlocResults,
) -> None:
    metric = aloc_calculator.calculate_metric(big_codebase)
    assert metric.results.aloc_number == big_codebase_aloc_result.aloc_number
    assert metric.results.aloc_percentage == big_codebase_aloc_result.aloc_percentage
    assert len(metric.results.aloc_result_per_layer) == 4
    for layer_result, expected_layer_result in zip(
        metric.results.aloc_result_per_layer,
        big_codebase_aloc_result.aloc_result_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert layer_result.aloc_number == expected_layer_result.aloc_number
        assert layer_result.aloc_percentage == expected_layer_result.aloc_percentage
