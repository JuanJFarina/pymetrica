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
    assert metric.results.hv_per_lloc == hv_result.hv_per_lloc
    assert len(metric.results.hv_per_layer) == 1
    for idx, file in enumerate(metric.results.hv_per_layer):
        assert file.name == hv_result.hv_per_layer[idx].name
        assert file.hv_number == hv_result.hv_per_layer[idx].hv_number
        assert file.hv_per_lloc == hv_result.hv_per_layer[idx].hv_per_lloc


def test_get_hv_big(
    hv_calculator: HalsteadVolumeCalculator,
    big_codebase: Codebase,
    big_codebase_hv_result: HalsteadVolumeResults,
) -> None:
    metric = hv_calculator.calculate_metric(big_codebase)
    assert metric.results.hv_number == big_codebase_hv_result.hv_number
    assert metric.results.hv_per_lloc == big_codebase_hv_result.hv_per_lloc
    assert len(metric.results.hv_per_layer) == 4
    metric.results.hv_per_layer.sort(key=lambda x: x.name)
    big_codebase_hv_result.hv_per_layer.sort(key=lambda x: x.name)
    for idx, file in enumerate(metric.results.hv_per_layer):
        assert file.name == big_codebase_hv_result.hv_per_layer[idx].name
        assert file.hv_number == big_codebase_hv_result.hv_per_layer[idx].hv_number
        assert file.hv_per_lloc == big_codebase_hv_result.hv_per_layer[idx].hv_per_lloc
