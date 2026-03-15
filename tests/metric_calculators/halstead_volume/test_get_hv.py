from pymetrica.metric_calculators import HalsteadVolumeCalculator
from pymetrica.metric_calculators.halstead_volume.hv_metric import HalsteadVolumeResults
from pymetrica.models import Codebase


def test_get_hv(
    hv_calculator: HalsteadVolumeCalculator,
    codebase: Codebase,
    hv_result: HalsteadVolumeResults,
) -> None:
    metric = hv_calculator.calculate_metric(codebase)
    assert metric.results.hv_number == hv_result.hv_number
    assert len(metric.results.hv_per_layer) == 1
    assert metric.results.hv_per_layer[0].name == hv_result.hv_per_layer[0].name
    assert (
        metric.results.hv_per_layer[0].hv_number == hv_result.hv_per_layer[0].hv_number
    )


def test_get_hv_big(
    hv_calculator: HalsteadVolumeCalculator,
    big_codebase: Codebase,
    big_codebase_hv_result: HalsteadVolumeResults,
) -> None:
    metric = hv_calculator.calculate_metric(big_codebase)
    assert metric.results.hv_number == big_codebase_hv_result.hv_number
    assert len(metric.results.hv_per_layer) == 4
    metric.results.hv_per_layer.sort(key=lambda x: x.name)
    big_codebase_hv_result.hv_per_layer.sort(key=lambda x: x.name)
    assert (
        metric.results.hv_per_layer[0].name
        == big_codebase_hv_result.hv_per_layer[0].name
    )
    assert (
        metric.results.hv_per_layer[0].hv_number
        == big_codebase_hv_result.hv_per_layer[0].hv_number
    )
    assert (
        metric.results.hv_per_layer[1].name
        == big_codebase_hv_result.hv_per_layer[1].name
    )
    assert (
        metric.results.hv_per_layer[1].hv_number
        == big_codebase_hv_result.hv_per_layer[1].hv_number
    )
    assert (
        metric.results.hv_per_layer[2].name
        == big_codebase_hv_result.hv_per_layer[2].name
    )
    assert (
        metric.results.hv_per_layer[2].hv_number
        == big_codebase_hv_result.hv_per_layer[2].hv_number
    )
    assert (
        metric.results.hv_per_layer[3].name
        == big_codebase_hv_result.hv_per_layer[3].name
    )
    assert (
        metric.results.hv_per_layer[3].hv_number
        == big_codebase_hv_result.hv_per_layer[3].hv_number
    )
