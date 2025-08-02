from __future__ import annotations

import pytest

from pymetrica.metric_calculators import CCCalculator


@pytest.fixture
def cc_calculator() -> CCCalculator:
    return CCCalculator()


@pytest.fixture
def cc_result() -> int:
    return 23
