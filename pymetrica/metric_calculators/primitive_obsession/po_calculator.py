import os

# the following imports need to be more specific to avoid cyclic imports
from pymetrica.metric_calculators.cyclomatic_complexity import (
    CCCalculator,
)
from pymetrica.metric_calculators.halstead_volume import (
    HalsteadVolumeCalculator,
)
from pymetrica.models import Codebase, Metric, MetricCalculator
from pymetrica.utils import log

from .po_metric import LayerPO, PrimitiveObsessionMetric, PrimitiveObsessionResults


class PrimitiveObsessionCalculator(MetricCalculator[PrimitiveObsessionResults]):
    def calculate_metric(  # pylint: disable=too-many-locals
        self: "PrimitiveObsessionCalculator",
        codebase: Codebase,
    ) -> Metric[PrimitiveObsessionResults]:
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})

        layers_results = list[LayerPO]()
        for layer_name, layer_files in layers.items():
            layer_name = layer_name.rsplit(os.sep, 1)[-1]
            layer_lloc = sum(file.lloc_number for file in layer_files)
            layer_cc = [  # noqa: RUF015
                result.cc_number
                for result in cc_metric.results.cc_result_per_layer
                if result.name == layer_name
            ][0]
            layer_hv = [  # noqa: RUF015
                result.hv_number
                for result in hv_metric.results.hv_per_layer
                if result.name == layer_name
            ][0]

        return PrimitiveObsessionMetric(
            name="Primitive Obsession",
            description=(
                "PO is a software metric that measures the extent to which "
                "primitive types are used excessively in the code, based on "
                "various factors such as Cyclomatic Complexity, Logical Lines "
                "Of Code, and Halstead Volume. Lower scores indicate better "
                "code quality, with scores above 20 suggesting moderate "
                "primitive obsession and scores above 50 indicating severe "
                "primitive obsession."
            ),
            results=PrimitiveObsessionResults(
                primitive_obsession=codebase_po,
                raw_line_cost=codebase_average_lloc_po,
                po_per_layer=sorted(
                    layers_results,
                    key=lambda x: x.primitive_obsession,
                    reverse=True,
                ),
            ),
        )
