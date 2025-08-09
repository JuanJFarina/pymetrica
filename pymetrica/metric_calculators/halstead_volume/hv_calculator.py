import ast
import math

from pymetrica.models import Codebase, MetricCalculator

from .hv_metric import HalsteadVolumeMetric, HalsteadVolumeResults
from .hv_visitor import HalsteadVolumeVisitor


class HalsteadVolumeCalculator(MetricCalculator[HalsteadVolumeResults]):
    def calculate_metric(
        self: "HalsteadVolumeCalculator",
        codebase: Codebase,
    ) -> HalsteadVolumeMetric:
        visitor = HalsteadVolumeVisitor()

        for code_file in codebase.files:
            tree = ast.parse(code_file.code)
            visitor.visit(tree)

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

        return HalsteadVolumeMetric(
            name="Halstead Volume",
            description=(""),
            results=HalsteadVolumeResults(hv_number=halstead_volume),
        )
