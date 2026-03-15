from pymetrica.metric_calculators import CCCalculator
from pymetrica.metric_calculators.cyclomatic_complexity.cc_metric import CCResults
from pymetrica.models import Codebase


def test_get_cc(
    cc_calculator: CCCalculator,
    codebase: Codebase,
    cc_result: CCResults,
) -> None:
    metric = cc_calculator.calculate_metric(codebase)
    assert metric.results.cc_number == cc_result.cc_number
    assert metric.results.lloc_per_cc == cc_result.lloc_per_cc
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
        metric.results.cc_result_per_layer[0].lloc_per_cc
        == cc_result.cc_result_per_layer[0].lloc_per_cc
    )


def test_get_cc_big(
    cc_calculator: CCCalculator,
    big_codebase: Codebase,
    big_codebase_cc_result: CCResults,
) -> None:
    metric = cc_calculator.calculate_metric(big_codebase)
    assert metric.results.cc_number == big_codebase_cc_result.cc_number
    assert metric.results.lloc_per_cc == big_codebase_cc_result.lloc_per_cc
    assert len(metric.results.cc_result_per_layer) == 4
    metric.results.cc_result_per_layer.sort(key=lambda x: x.name)
    big_codebase_cc_result.cc_result_per_layer.sort(key=lambda x: x.name)
    assert (
        metric.results.cc_result_per_layer[0].name
        == big_codebase_cc_result.cc_result_per_layer[0].name
    )
    assert (
        metric.results.cc_result_per_layer[0].cc_number
        == big_codebase_cc_result.cc_result_per_layer[0].cc_number
    )
    assert (
        metric.results.cc_result_per_layer[0].lloc_per_cc
        == big_codebase_cc_result.cc_result_per_layer[0].lloc_per_cc
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
        metric.results.cc_result_per_layer[1].lloc_per_cc
        == big_codebase_cc_result.cc_result_per_layer[1].lloc_per_cc
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
        metric.results.cc_result_per_layer[2].lloc_per_cc
        == big_codebase_cc_result.cc_result_per_layer[2].lloc_per_cc
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
        metric.results.cc_result_per_layer[3].lloc_per_cc
        == big_codebase_cc_result.cc_result_per_layer[3].lloc_per_cc
    )
