from pymetrica.metric_calculators import CCCalculator
from pymetrica.models import Codebase


def test_get_cc(
    cc_calculator: CCCalculator,
    codebase: Codebase,
    cc_result: int,
) -> None:
    metric = cc_calculator.calculate_metric(codebase)
    assert metric.results.cc_number == cc_result
