from pymetrica.metric_calculators import HalsteadVolumeCalculator
from pymetrica.models import Codebase


def test_get_hv(
    hv_calculator: HalsteadVolumeCalculator,
    codebase: Codebase,
    hv_result: int,
) -> None:
    metric = hv_calculator.calculate_metric(codebase)
    assert metric.results.hv_number == hv_result


def test_get_hv_big(
    hv_calculator: HalsteadVolumeCalculator,
    big_codebase: Codebase,
    big_codebase_hv_result: int,
) -> None:
    metric = hv_calculator.calculate_metric(big_codebase)
    assert metric.results.hv_number == big_codebase_hv_result
