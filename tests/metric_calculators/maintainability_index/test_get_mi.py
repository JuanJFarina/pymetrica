from pymetrica.metric_calculators import MaintainabilityIndexCalculator
from pymetrica.models import Codebase


def test_get_mi(
    mi_calculator: MaintainabilityIndexCalculator,
    codebase: Codebase,
    mi_result: tuple[float, float],
) -> None:
    metric = mi_calculator.calculate_metric(codebase)
    assert metric.results.maintainability_index == mi_result[0]
    assert metric.results.normalized_mi == mi_result[1]


def test_get_mi_big(
    mi_calculator: MaintainabilityIndexCalculator,
    big_codebase: Codebase,
    big_codebase_mi_result: tuple[float, float],
) -> None:
    metric = mi_calculator.calculate_metric(big_codebase)
    assert metric.results.maintainability_index == big_codebase_mi_result[0]
    assert metric.results.normalized_mi == big_codebase_mi_result[1]
