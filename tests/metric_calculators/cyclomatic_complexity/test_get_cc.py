from pymetrica.metric_calculators import CCCalculator
from pymetrica.models import Codebase


def test_get_cc(
    cc_calculator: CCCalculator,
    codebase: Codebase,
    cc_result: int,
) -> None:
    metric = cc_calculator.calculate_metric(codebase)
    assert metric.results.cc_number == cc_result


def test_get_cc_big(
    cc_calculator: CCCalculator,
    big_codebase: Codebase,
    big_codebase_cc_result: int,
) -> None:
    metric = cc_calculator.calculate_metric(big_codebase)
    assert metric.results.cc_number == big_codebase_cc_result
