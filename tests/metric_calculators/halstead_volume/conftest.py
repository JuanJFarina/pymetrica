import pytest

from pymetrica.metric_calculators import HalsteadVolumeCalculator
from pymetrica.metric_calculators.halstead_volume.hv_metric import (
    HalsteadVolumeResults,
    LayerHV,
)


@pytest.fixture
def hv_calculator() -> HalsteadVolumeCalculator:
    return HalsteadVolumeCalculator()


@pytest.fixture(name="small_codebase_layer_hv")
def _small_codebase_layer_hv() -> list[LayerHV]:
    return [
        LayerHV(
            name="root",
            hv_number=704.5342159112735,
            hv_per_lloc=17.613355397781838,
        ),
    ]


@pytest.fixture
def hv_result(small_codebase_layer_hv: list[LayerHV]) -> HalsteadVolumeResults:
    return HalsteadVolumeResults(
        hv_number=704.5342159112735,
        hv_per_lloc=17.613355397781838,
        hv_per_layer=small_codebase_layer_hv,
    )


@pytest.fixture(name="big_codebase_layer_hv")
def _big_codebase_layer_hv() -> list[LayerHV]:
    return [
        LayerHV(
            name="exception_handlers",
            hv_number=47.86313713864835,
            hv_per_lloc=7.977189523108058,
        ),
        LayerHV(
            name="middlewares",
            hv_number=88.75488750216347,
            hv_per_lloc=5.916992500144231,
        ),
        LayerHV(
            name="routes",
            hv_number=39.62406251802891,
            hv_per_lloc=5.6605803597184154,
        ),
        LayerHV(
            name="root",
            hv_number=80.0,
            hv_per_lloc=7.2727272727272725,
        ),
    ]


@pytest.fixture
def big_codebase_hv_result(
    big_codebase_layer_hv: list[LayerHV],
) -> HalsteadVolumeResults:
    return HalsteadVolumeResults(
        hv_number=415.4885284645254,
        hv_per_lloc=10.653552011910907,
        hv_per_layer=big_codebase_layer_hv,
    )
