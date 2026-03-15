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
    assert (
        metric.results.aloc_result_per_layer[0].name
        == aloc_result.aloc_result_per_layer[0].name
    )
    assert (
        metric.results.aloc_result_per_layer[0].aloc_number
        == aloc_result.aloc_result_per_layer[0].aloc_number
    )
    assert (
        metric.results.aloc_result_per_layer[0].aloc_percentage
        == aloc_result.aloc_result_per_layer[0].aloc_percentage
    )


def test_get_aloc_big(
    aloc_calculator: AlocCalculator,
    big_codebase: Codebase,
    big_codebase_aloc_result: AlocResults,
) -> None:
    metric = aloc_calculator.calculate_metric(big_codebase)
    assert metric.results.aloc_number == big_codebase_aloc_result.aloc_number
    assert metric.results.aloc_percentage == big_codebase_aloc_result.aloc_percentage
    assert len(metric.results.aloc_result_per_layer) == 4
    metric.results.aloc_result_per_layer.sort(key=lambda x: x.name)
    big_codebase_aloc_result.aloc_result_per_layer.sort(key=lambda x: x.name)
    assert (
        metric.results.aloc_result_per_layer[0].name
        == big_codebase_aloc_result.aloc_result_per_layer[0].name
    )
    assert (
        metric.results.aloc_result_per_layer[0].aloc_number
        == big_codebase_aloc_result.aloc_result_per_layer[0].aloc_number
    )
    assert (
        metric.results.aloc_result_per_layer[0].aloc_percentage
        == big_codebase_aloc_result.aloc_result_per_layer[0].aloc_percentage
    )
    assert (
        metric.results.aloc_result_per_layer[1].name
        == big_codebase_aloc_result.aloc_result_per_layer[1].name
    )
    assert (
        metric.results.aloc_result_per_layer[1].aloc_number
        == big_codebase_aloc_result.aloc_result_per_layer[1].aloc_number
    )
    assert (
        metric.results.aloc_result_per_layer[1].aloc_percentage
        == big_codebase_aloc_result.aloc_result_per_layer[1].aloc_percentage
    )
    assert (
        metric.results.aloc_result_per_layer[2].name
        == big_codebase_aloc_result.aloc_result_per_layer[2].name
    )
    assert (
        metric.results.aloc_result_per_layer[2].aloc_number
        == big_codebase_aloc_result.aloc_result_per_layer[2].aloc_number
    )
    assert (
        metric.results.aloc_result_per_layer[2].aloc_percentage
        == big_codebase_aloc_result.aloc_result_per_layer[2].aloc_percentage
    )
    assert (
        metric.results.aloc_result_per_layer[3].name
        == big_codebase_aloc_result.aloc_result_per_layer[3].name
    )
    assert (
        metric.results.aloc_result_per_layer[3].aloc_number
        == big_codebase_aloc_result.aloc_result_per_layer[3].aloc_number
    )
    assert (
        metric.results.aloc_result_per_layer[3].aloc_percentage
        == big_codebase_aloc_result.aloc_result_per_layer[3].aloc_percentage
    )
