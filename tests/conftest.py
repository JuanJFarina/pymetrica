from pymetrica.codebase_parser import parse_codebase
from pymetrica.models import Codebase
import pytest


@pytest.fixture
def codebase() -> Codebase:
    return parse_codebase("./tests/sample_codebase")
