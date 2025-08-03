import ast

from pymetrica.models.codebase import Codebase
from pymetrica.models.metric_calculator import MetricCalculator

from .cc_metric import CCMetric, CCResults
from .cc_visitor import CCVisitor


class CCCalculator(MetricCalculator[CCResults]):
    def calculate_metric(self: "CCCalculator", codebase: Codebase) -> CCMetric:
        total_complexity = 1

        for code_file in codebase.files:
            tree = ast.parse(code_file.code)
            visitor = CCVisitor()
            visitor.visit(tree)
            total_complexity += visitor.complexity

        return CCMetric(
            name="Cyclomatic Complexity",
            description=(
                "Cyclomatic Complexity (CC) is a software metric used to "
                "measure the complexity of a program. It is calculated based "
                "on the control flow graph of the program, where nodes "
                "represent code blocks and edges represent control flow paths."
            ),
            results=CCResults(
                cc_number=total_complexity,
                cc_lloc_ratio=total_complexity / codebase.lloc_number * 100,
            ),
        )
