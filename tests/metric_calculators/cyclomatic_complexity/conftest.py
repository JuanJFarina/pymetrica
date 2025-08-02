import pytest
from pymetrica.metric_calculators import CCCalculator


@pytest.fixture
def cc_calculator():
    return CCCalculator()
