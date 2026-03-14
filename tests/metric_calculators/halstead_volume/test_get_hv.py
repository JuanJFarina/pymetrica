from pymetrica.metric_calculators import HalsteadVolumeCalculator
from pymetrica.metric_calculators.halstead_volume.hv_metric import HalsteadVolumeResults
from pymetrica.models import Codebase


def test_get_hv(
    hv_calculator: HalsteadVolumeCalculator,
    codebase: Codebase,
    hv_result: HalsteadVolumeResults,
) -> None:
    metric = hv_calculator.calculate_metric(codebase)
    print(metric.results)
    assert metric.results == hv_result
    assert len(metric.results.hv_per_layer) == 1
    for layer_result, expected_layer_result in zip(
        metric.results.hv_per_layer,
        hv_result.hv_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert layer_result.hv_number == expected_layer_result.hv_number


def test_get_hv_big(
    hv_calculator: HalsteadVolumeCalculator,
    big_codebase: Codebase,
    big_codebase_hv_result: HalsteadVolumeResults,
) -> None:
    metric = hv_calculator.calculate_metric(big_codebase)
    print(metric.results)
    assert metric.results == big_codebase_hv_result
    assert len(metric.results.hv_per_layer) == 4
    for layer_result, expected_layer_result in zip(
        metric.results.hv_per_layer,
        big_codebase_hv_result.hv_per_layer,
    ):
        assert layer_result.name == expected_layer_result.name
        assert layer_result.hv_number == expected_layer_result.hv_number
