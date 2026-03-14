from pymetrica.metric_calculators import CCCalculator
from pymetrica.metric_calculators.cyclomatic_complexity.cc_metric import CCResults
from pymetrica.models import Codebase


def test_get_cc(
    cc_calculator: CCCalculator,
    codebase: Codebase,
    cc_result: CCResults,
) -> None:
    metric = cc_calculator.calculate_metric(codebase)
    assert metric.results == cc_result
    assert len(metric.results.cc_result_per_layer) == 1
    for layer_result, expected_layer_result in zip(
        metric.results.cc_result_per_layer,
        cc_result.cc_result_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert layer_result.cc_number == expected_layer_result.cc_number
        assert layer_result.cc_lloc_ratio == expected_layer_result.cc_lloc_ratio


def test_get_cc_big(
    cc_calculator: CCCalculator,
    big_codebase: Codebase,
    big_codebase_cc_result: CCResults,
) -> None:
    metric = cc_calculator.calculate_metric(big_codebase)
    assert metric.results == big_codebase_cc_result
    assert len(metric.results.cc_result_per_layer) == 4
    for layer_result, expected_layer_result in zip(
        metric.results.cc_result_per_layer,
        big_codebase_cc_result.cc_result_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert layer_result.cc_number == expected_layer_result.cc_number
        assert layer_result.cc_lloc_ratio == expected_layer_result.cc_lloc_ratio
