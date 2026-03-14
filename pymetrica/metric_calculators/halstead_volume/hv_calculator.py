import ast
import math
import os

from pymetrica.models import Codebase, MetricCalculator

from .hv_metric import HalsteadVolumeMetric, HalsteadVolumeResults, LayerHV
from .hv_visitor import HalsteadVolumeVisitor


class HalsteadVolumeCalculator(MetricCalculator[HalsteadVolumeResults]):
    def calculate_metric(
        self: "HalsteadVolumeCalculator",
        codebase: Codebase,
    ) -> HalsteadVolumeMetric:
        layer_results = list[LayerHV]()
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})

        codebase_unique_operators = set()
        codebase_unique_operands = set()
        codebase_operators = 0
        codebase_operands = 0

        for layer_name, layer_files in layers.items():
            total_hv = 0

            for code_file in layer_files:
                tree = ast.parse(code_file.code)
                visitor = HalsteadVolumeVisitor()
                visitor.visit(tree)

                codebase_unique_operators.update(set(visitor.operators))
                codebase_unique_operands.update(set(visitor.operands))
                codebase_operators += len(visitor.operators)
                codebase_operands += len(visitor.operands)
                unique_operators = len(set(visitor.operators))
                unique_operands = len(set(visitor.operands))
                operators = len(visitor.operators)
                operands = len(visitor.operands)

                if unique_operators + unique_operands == 0:
                    halstead_volume = 0.0
                else:
                    vocabulary = unique_operators + unique_operands
                    length = operators + operands
                    halstead_volume = length * math.log2(vocabulary)

                total_hv += halstead_volume

            layer_results.append(
                LayerHV(
                    name=layer_name.rsplit(os.sep, 1)[-1],
                    hv_number=total_hv,
                ),
            )

        codebase_unique_operators = len(codebase_unique_operators)
        codebase_unique_operands = len(codebase_unique_operands)

        if codebase_unique_operators + codebase_unique_operands == 0:
            codebase_halstead_volume = 0.0
        else:
            vocabulary = codebase_unique_operators + codebase_unique_operands
            length = codebase_operators + codebase_operands
            codebase_halstead_volume = length * math.log2(vocabulary)

        return HalsteadVolumeMetric(
            name="Halstead Volume",
            description=(""),
            results=HalsteadVolumeResults(
                hv_number=codebase_halstead_volume,
                hv_per_layer=layer_results,
            ),
        )
