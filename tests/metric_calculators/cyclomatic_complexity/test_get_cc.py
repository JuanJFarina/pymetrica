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
    for idx, file in enumerate(metric.results.cc_result_per_layer):
        assert file.name == cc_result.cc_result_per_layer[idx].name
        assert file.cc_number == cc_result.cc_result_per_layer[idx].cc_number
        assert file.lloc_per_cc == cc_result.cc_result_per_layer[idx].lloc_per_cc


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
    for idx, file in enumerate(metric.results.cc_result_per_layer):
        assert file.name == big_codebase_cc_result.cc_result_per_layer[idx].name
        assert (
            file.cc_number == big_codebase_cc_result.cc_result_per_layer[idx].cc_number
        )
        assert (
            file.lloc_per_cc
            == big_codebase_cc_result.cc_result_per_layer[idx].lloc_per_cc
        )
