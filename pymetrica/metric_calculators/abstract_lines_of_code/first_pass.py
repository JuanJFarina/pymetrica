import ast
from typing import Any

from pymetrica.models import Codebase
from pymetrica.utils import is_logical_line_of_code

from pydantic import BaseModel


class PreliminaryResults(BaseModel):
    aloc: int
    classes: dict[str, int]


def gather_loc_and_classes(codebase: Codebase) -> PreliminaryResults:
    """
    First pass:
      - Count total logical lines ('lloc').
      - Identify all class definitions and compute their LOC spans.
      - Compute abstract LOC ('aloc').
      - Record non-abstract class LOC in 'classes'.
    """
    total_lloc = 0
    total_aloc = 0
    classes: dict[str, int] = {}

    for file in codebase.files:
        tree = ast.parse(file.code)

        # Count logical lines in file
        file_lloc = sum(1 for l in file.code_lines if is_logical_line_of_code(l))
        total_lloc += file_lloc

        # Collect abstract lines
        file_abs: set[int] = set()
        for node in ast.walk(tree):
            # Imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                file_abs.add(node.lineno)
            # __all__ assignments
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id == "__all__":
                        file_abs.add(node.lineno)
            # Function defs and decorators
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                file_abs.add(node.lineno)
                for dec in node.decorator_list:
                    file_abs.add(dec.lineno)
            # Class defs and decorators
            if isinstance(node, ast.ClassDef):
                file_abs.add(node.lineno)
                for dec in node.decorator_list:
                    file_abs.add(dec.lineno)
            # # Any call TODO this was removed because many calls may be done in one single line
            # if isinstance(node, ast.Call):
            #     file_abs.add(node.lineno)

        total_aloc += len(file_abs)

        # Measure classes
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                start, end = node.lineno, getattr(node, "end_lineno", node.lineno)
                # Check inheritance
                bases: list[str] = []
                for b in node.bases:
                    if isinstance(b, ast.Name):
                        bases.append(b.id)
                    else:
                        try:
                            bases.append(ast.unparse(b))
                        except:
                            pass
                # Treat ABC, ABCMeta, Protocol, and Enum as abstract
                is_abstract_base = any(
                    base in ("ABC", "ABCMeta", "Protocol", "Enum") for base in bases
                )
                # Count LOC
                loc = sum(
                    1
                    for i in range(start - 1, end)
                    if i < len(file.code_lines)
                    and is_logical_line_of_code(file.code_lines[i])
                )
                if not is_abstract_base:
                    classes[node.name] = loc - 1  # -1 to exclude class definition line

    return PreliminaryResults(aloc=total_aloc, classes=classes)
