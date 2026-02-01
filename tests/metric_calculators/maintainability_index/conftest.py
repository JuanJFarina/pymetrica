import pytest

from pymetrica.metric_calculators import MaintainabilityIndexCalculator


@pytest.fixture
def mi_calculator() -> MaintainabilityIndexCalculator:
    return MaintainabilityIndexCalculator()


@pytest.fixture
def mi_result() -> tuple[float, float]:
    return 71.8509609747319, 42.01810583317655


@pytest.fixture
def big_codebase_mi_result() -> tuple[float, float]:
    return 79.83713530709466, 46.688383220523185
