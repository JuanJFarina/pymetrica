import ast

from pymetrica.models.codebase import Codebase
from pymetrica.models.metric_calculator import MetricCalculator

from .hv_metric import HalsteadVolumeMetric, HalsteadVolumeResults
from .hv_visitor import HalsteadVolumeVisitor


class HalsteadVolumeCalculator(MetricCalculator[HalsteadVolumeResults]):
    def calculate_metric(
        self: "HalsteadVolumeCalculator",
        codebase: Codebase,
    ) -> HalsteadVolumeMetric:
        for code_file in codebase.files:
            tree = ast.parse(code_file.code)
            visitor = HalsteadVolumeVisitor()
            visitor.visit(tree)
            # halstead_volume += visitor.complexity

        return HalsteadVolumeMetric(
            name="Halstead Volume",
            description=(""),
            results=HalsteadVolumeResults(hv_number=0),
        )
