import ast
import os

from pymetrica.models import Code, Codebase, Metric, MetricCalculator
from pymetrica.utils.settings import Config

from .po_metric import LayerPO, PrimitiveObsessionMetric, PrimitiveObsessionResults
from .po_visitor import POVisitor


class PrimitiveObsessionCalculator(MetricCalculator[PrimitiveObsessionResults]):
    def calculate_metric(self, codebase: Codebase) -> Metric[PrimitiveObsessionResults]:
        layers_results = list[LayerPO]()
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})
        top_findings_all = list[Code]()
        top_findings_targeted = list[Code]()

        codebase_all_primitives = 0
        codebase_targeted_primitives = 0

        for layer_name, layer_files in layers.items():
            layer_all_primitives = 0
            layer_targeted_primitives = 0

            for code_file in layer_files:
                tree = ast.parse(code_file.code)
                visitor = POVisitor()
                visitor.visit(tree)
                code_file.all_primitives = len(visitor.all_primitives)
                code_file.targeted_primitives = len(visitor.targeted_primitives)
                layer_all_primitives += code_file.all_primitives
                layer_targeted_primitives += code_file.targeted_primitives

            layers_results.append(
                LayerPO(
                    name=layer_name.rsplit(os.sep, 1)[-1],
                    all_primitives=layer_all_primitives,
                    targeted_primitives=layer_targeted_primitives,
                ),
            )
            codebase_all_primitives += layer_all_primitives
            codebase_targeted_primitives += layer_targeted_primitives

        if Config.find_top_flaws:
            top_findings_all = sorted(
                codebase.files,
                key=lambda f: f.all_primitives or 0,
                reverse=True,
            )[: Config.top_findings]
            top_findings_targeted = sorted(
                codebase.files,
                key=lambda f: f.targeted_primitives or 0,
                reverse=True,
            )[: Config.top_findings]

        return PrimitiveObsessionMetric(
            name="Primitive Obsession",
            description=(
                "PO is a software metric that measures the extent to which "
                "primitive types are used excessively in the code."
            ),
            results=PrimitiveObsessionResults(
                all_primitives=codebase_all_primitives,
                targeted_primitives=codebase_targeted_primitives,
                all_primitives_percent=(
                    codebase_all_primitives / codebase.lloc_number * 100
                    if codebase.lloc_number > 0
                    else 0.0
                ),
                targeted_primitives_percent=(
                    codebase_targeted_primitives / codebase.lloc_number * 100
                    if codebase.lloc_number > 0
                    else 0.0
                ),
                po_per_layer=sorted(
                    layers_results,
                    key=lambda x: x.targeted_primitives,
                    reverse=True,
                ),
                top_findings_all=top_findings_all,
                top_findings_targeted=top_findings_targeted,
            ),
        )
