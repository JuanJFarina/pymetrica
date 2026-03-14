import pytest

from pymetrica.metric_calculators import CCCalculator
from pymetrica.metric_calculators.cyclomatic_complexity.cc_metric import (
    CCResults,
    LayerCC,
)


@pytest.fixture
def cc_calculator() -> CCCalculator:
    return CCCalculator()


@pytest.fixture(name="small_codebase_layer_cc")
def _small_codebase_layer_cc() -> list[LayerCC]:
    return [
        LayerCC(
            name="root",
            cc_number=22,
            lloc_per_cc=1.8181818181818181,
        ),
    ]


@pytest.fixture
def cc_result(small_codebase_layer_cc: list[LayerCC]) -> CCResults:
    return CCResults(
        cc_number=23,
        lloc_per_cc=1.7391304347826086,
        cc_result_per_layer=small_codebase_layer_cc,
    )


@pytest.fixture(name="big_codebase_layer_cc")
def _big_codebase_layer_cc() -> list[LayerCC]:
    return [
        LayerCC(name="exception_handlers", cc_number=0, lloc_per_cc=0.0),
        LayerCC(name="middlewares", cc_number=0, lloc_per_cc=0.0),
        LayerCC(name="routes", cc_number=0, lloc_per_cc=0.0),
        LayerCC(name="root", cc_number=1, lloc_per_cc=11.0),
    ]


@pytest.fixture
def big_codebase_cc_result(big_codebase_layer_cc: list[LayerCC]) -> CCResults:
    return CCResults(
        cc_number=2,
        lloc_per_cc=19.5,
        cc_result_per_layer=big_codebase_layer_cc,
    )
