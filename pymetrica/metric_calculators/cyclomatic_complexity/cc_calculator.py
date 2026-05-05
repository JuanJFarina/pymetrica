import ast
import os

from pymetrica.models import Code, Codebase, MetricCalculator
from pymetrica.utils.settings import Config

from .cc_metric import CCMetric, CCResults, LayerCC
from .cc_visitor import CCVisitor


class CCCalculator(MetricCalculator[CCResults]):
    def calculate_metric(self, codebase: Codebase) -> CCMetric:
        layer_results = list[LayerCC]()
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})
        top_findings = list[Code]()

        codebase_complexity = 1

        for layer_name, layer_files in layers.items():
            layer_complexity = 0
            layer_lloc = 0

            for code_file in layer_files:
                tree = ast.parse(code_file.code)
                visitor = CCVisitor()
                visitor.visit(tree)
                layer_complexity += visitor.complexity
                code_file.cc_number = visitor.complexity
                layer_lloc += code_file.lloc_number

            layer_results.append(
                LayerCC(
                    name=layer_name.rsplit(os.sep, 1)[-1],
                    cc_number=layer_complexity,
                    lloc_per_cc=layer_lloc / layer_complexity
                    if layer_complexity > 0
                    else 0,
                ),
            )
            codebase_complexity += layer_complexity

        if Config.find_top_flaws:
            top_findings = sorted(
                codebase.files,
                key=lambda f: f.cc_number or 0,
                reverse=True,
            )[: Config.top_findings]

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
                lloc_per_cc=codebase.lloc_number / codebase_complexity
                if codebase_complexity > 0
                else 0,
                cc_result_per_layer=sorted(
                    layer_results,
                    key=lambda x: x.lloc_per_cc if x.lloc_per_cc > 0 else float("inf"),
                ),
                top_findings=top_findings,
            ),
        )
