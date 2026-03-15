import io
from contextlib import redirect_stdout

import pytest

from pymetrica.codebase_parser.diagram_generator import create_diagram
from pymetrica.models import Codebase


@pytest.mark.xfail(reason="Diagram generation without layers differs per environment")
def test_small_create_diagram(codebase: Codebase, small_codebase_diagram: str) -> None:
    output = io.StringIO()
    with redirect_stdout(output):
        create_diagram(codebase, write=False)
    diagram = output.getvalue()
    assert diagram == small_codebase_diagram


def test_big_create_diagram(big_codebase: Codebase, big_codebase_diagram: str) -> None:
    output = io.StringIO()
    with redirect_stdout(output):
        create_diagram(big_codebase, write=False)
    diagram = output.getvalue()
    assert diagram == big_codebase_diagram
