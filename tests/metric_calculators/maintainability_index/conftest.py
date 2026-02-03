import pytest

from pymetrica.metric_calculators import MaintainabilityIndexCalculator


@pytest.fixture
def mi_calculator() -> MaintainabilityIndexCalculator:
    return MaintainabilityIndexCalculator()


@pytest.fixture
def mi_result() -> tuple[float, float]:
    return 163.14511763251448, 95.40650153948216


@pytest.fixture
def big_codebase_mi_result() -> tuple[float, float]:
    return 165.44855242617115, 96.75353943050943
