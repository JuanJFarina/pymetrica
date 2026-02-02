import pytest

from pymetrica.metric_calculators import MaintainabilityIndexCalculator


@pytest.fixture
def mi_calculator() -> MaintainabilityIndexCalculator:
    return MaintainabilityIndexCalculator()


@pytest.fixture
def mi_result() -> tuple[float, float]:
    return 142.24524024368299, 83.18435101969766


@pytest.fixture
def big_codebase_mi_result() -> tuple[float, float]:
    return 147.86428382677366, 86.47034141916589
