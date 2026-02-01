import pytest

from pymetrica.metric_calculators import HalsteadVolumeCalculator


@pytest.fixture
def hv_calculator() -> HalsteadVolumeCalculator:
    return HalsteadVolumeCalculator()


@pytest.fixture
def hv_result() -> float:
    return 704.5342159112735


@pytest.fixture
def big_codebase_hv_result() -> float:
    return 415.4885284645254
