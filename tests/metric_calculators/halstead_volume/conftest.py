import pytest

from pymetrica.metric_calculators import HalsteadVolumeCalculator
from pymetrica.metric_calculators.halstead_volume.hv_metric import (
    HalsteadVolumeResults,
    LayerHV,
)


@pytest.fixture
def hv_calculator() -> HalsteadVolumeCalculator:
    return HalsteadVolumeCalculator()


@pytest.fixture
def small_codebase_layer_hv() -> list[LayerHV]:
    return [
        LayerHV(
            name="root",
            hv_number=704.5342159112735,
        )
    ]


@pytest.fixture
def hv_result(small_codebase_layer_hv: list[LayerHV]) -> HalsteadVolumeResults:
    return HalsteadVolumeResults(
        hv_number=704.5342159112735,
        hv_per_layer=small_codebase_layer_hv,
    )


@pytest.fixture
def big_codebase_layer_hv() -> list[LayerHV]:
    return [
        LayerHV(name="exception_handlers", hv_number=47.86313713864835),
        LayerHV(name="middlewares", hv_number=88.75488750216347),
        LayerHV(name="routes", hv_number=39.62406251802891),
        LayerHV(name="root", hv_number=80.0),
    ]


@pytest.fixture
def big_codebase_hv_result(
    big_codebase_layer_hv: list[LayerHV],
) -> HalsteadVolumeResults:
    return HalsteadVolumeResults(
        hv_number=415.4885284645254,
        hv_per_layer=big_codebase_layer_hv,
    )
