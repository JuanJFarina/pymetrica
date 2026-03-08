import pytest

from pymetrica.metric_calculators import AlocCalculator


@pytest.fixture
def aloc_calculator() -> AlocCalculator:
    return AlocCalculator()


@pytest.fixture
def aloc_result() -> tuple[int, float]:
    return (6, 15.0)


@pytest.fixture
def big_codebase_aloc_result() -> tuple[int, float]:
    return (31, 79.48717948717949)
