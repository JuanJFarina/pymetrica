import pytest

from pymetrica.metric_calculators import MaintainabilityIndexCalculator


@pytest.fixture
def mi_calculator() -> MaintainabilityIndexCalculator:
    return MaintainabilityIndexCalculator()


@pytest.fixture
def mi_result() -> tuple[float, float]:
    return 146.212740243683, 85.50452645829414


@pytest.fixture
def big_codebase_mi_result() -> tuple[float, float]:
    return 148.20928382677366, 86.6720958051308
