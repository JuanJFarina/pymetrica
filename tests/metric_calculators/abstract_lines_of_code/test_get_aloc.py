from pymetrica.metric_calculators import AlocCalculator
from pymetrica.models import Codebase


def test_get_aloc(
    aloc_calculator: AlocCalculator,
    codebase: Codebase,
    aloc_result: tuple[int, float],
) -> None:
    metric = aloc_calculator.calculate_metric(codebase)
    assert metric.results.aloc_number == aloc_result[0]
    assert metric.results.aloc_percentage == aloc_result[1]


def test_get_aloc_big(
    aloc_calculator: AlocCalculator,
    big_codebase: Codebase,
    big_codebase_aloc_result: tuple[int, float],
) -> None:
    metric = aloc_calculator.calculate_metric(big_codebase)
    assert metric.results.aloc_number == big_codebase_aloc_result[0]
    assert metric.results.aloc_percentage == big_codebase_aloc_result[1]
