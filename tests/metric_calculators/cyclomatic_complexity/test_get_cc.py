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
    assert (
        metric.results.cc_result_per_layer[0].name
        == cc_result.cc_result_per_layer[0].name
    )
    assert (
        metric.results.cc_result_per_layer[0].cc_number
        == cc_result.cc_result_per_layer[0].cc_number
    )
    assert (
        metric.results.cc_result_per_layer[0].cc_lloc_ratio
        == cc_result.cc_result_per_layer[0].cc_lloc_ratio
    )


def test_get_cc_big(
    cc_calculator: CCCalculator,
    big_codebase: Codebase,
    big_codebase_cc_result: CCResults,
) -> None:
    metric = cc_calculator.calculate_metric(big_codebase)
    assert metric.results == big_codebase_cc_result
    assert len(metric.results.cc_result_per_layer) == 4
    assert (
        metric.results.cc_result_per_layer[0].name
        == big_codebase_cc_result.cc_result_per_layer[0].name
    )
    assert (
        metric.results.cc_result_per_layer[0].cc_number
        == big_codebase_cc_result.cc_result_per_layer[0].cc_number
    )
    assert (
        metric.results.cc_result_per_layer[0].cc_lloc_ratio
        == big_codebase_cc_result.cc_result_per_layer[0].cc_lloc_ratio
    )
    assert (
        metric.results.cc_result_per_layer[1].name
        == big_codebase_cc_result.cc_result_per_layer[1].name
    )
    assert (
        metric.results.cc_result_per_layer[1].cc_number
        == big_codebase_cc_result.cc_result_per_layer[1].cc_number
    )
    assert (
        metric.results.cc_result_per_layer[1].cc_lloc_ratio
        == big_codebase_cc_result.cc_result_per_layer[1].cc_lloc_ratio
    )
    assert (
        metric.results.cc_result_per_layer[2].name
        == big_codebase_cc_result.cc_result_per_layer[2].name
    )
    assert (
        metric.results.cc_result_per_layer[2].cc_number
        == big_codebase_cc_result.cc_result_per_layer[2].cc_number
    )
    assert (
        metric.results.cc_result_per_layer[2].cc_lloc_ratio
        == big_codebase_cc_result.cc_result_per_layer[2].cc_lloc_ratio
    )
    assert (
        metric.results.cc_result_per_layer[3].name
        == big_codebase_cc_result.cc_result_per_layer[3].name
    )
    assert (
        metric.results.cc_result_per_layer[3].cc_number
        == big_codebase_cc_result.cc_result_per_layer[3].cc_number
    )
    assert (
        metric.results.cc_result_per_layer[3].cc_lloc_ratio
        == big_codebase_cc_result.cc_result_per_layer[3].cc_lloc_ratio
    )
