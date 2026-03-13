import ast
import os

from pymetrica.models import Codebase, MetricCalculator

from .cc_metric import CCMetric, CCResults, LayerCC
from .cc_visitor import CCVisitor


class CCCalculator(MetricCalculator[CCResults]):
    def calculate_metric(self: "CCCalculator", codebase: Codebase) -> CCMetric:
        layer_results = list[LayerCC]()
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})

        codebase_complexity = 1

        for layer_name, layer_files in layers.items():
            total_complexity = 0
            total_lloc = 0

            for code_file in layer_files:
                tree = ast.parse(code_file.code)
                visitor = CCVisitor()
                visitor.visit(tree)
                total_complexity += visitor.complexity
                total_lloc += code_file.lloc_number

            layer_results.append(
                LayerCC(
                    name=layer_name.rsplit(os.sep, 1)[-1],
                    cc_number=total_complexity,
                    cc_lloc_ratio=total_complexity / total_lloc * 100
                    if total_lloc > 0
                    else 0,
                ),
            )
            codebase_complexity += total_complexity

        return CCMetric(
            name="Cyclomatic Complexity",
            description=(
                "Cyclomatic Complexity (CC) is a software metric used to "
                "measure the complexity of a program. It is calculated based "
                "on the control flow graph of the program, where nodes "
                "represent code blocks and edges represent control flow paths. "
            ),
            results=CCResults(
                cc_number=codebase_complexity,
                cc_lloc_ratio=codebase_complexity / codebase.lloc_number * 100,
                cc_result_per_layer=layer_results,
            ),
        )
