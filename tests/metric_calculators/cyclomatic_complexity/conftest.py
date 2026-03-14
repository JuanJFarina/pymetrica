import pytest

from pymetrica.metric_calculators import CCCalculator
from pymetrica.metric_calculators.cyclomatic_complexity.cc_metric import (
    CCResults,
    LayerCC,
)


@pytest.fixture
def cc_calculator() -> CCCalculator:
    return CCCalculator()


@pytest.fixture
def small_codebase_layer_cc() -> list[LayerCC]:
    return [
        LayerCC(
            name="root",
            cc_number=22,
            cc_lloc_ratio=55.00000000000001,
        )
    ]


@pytest.fixture
def cc_result(small_codebase_layer_cc: list[LayerCC]) -> CCResults:
    return CCResults(
        cc_number=23,
        cc_lloc_ratio=57.49999999999999,
        cc_result_per_layer=small_codebase_layer_cc,
    )


@pytest.fixture
def big_codebase_layer_cc() -> list[LayerCC]:
    return [
        LayerCC(name="exception_handlers", cc_number=0, cc_lloc_ratio=0.0),
        LayerCC(name="middlewares", cc_number=0, cc_lloc_ratio=0.0),
        LayerCC(name="routes", cc_number=0, cc_lloc_ratio=0.0),
        LayerCC(name="root", cc_number=1, cc_lloc_ratio=9.090909090909092),
    ]


@pytest.fixture
def big_codebase_cc_result(big_codebase_layer_cc: list[LayerCC]) -> CCResults:
    return CCResults(
        cc_number=2,
        cc_lloc_ratio=5.128205128205128,
        cc_result_per_layer=big_codebase_layer_cc,
    )
