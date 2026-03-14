import math
import os
from pymetrica.models import Codebase, Metric, MetricCalculator

# the following imports need to be more specific to avoid cyclic imports
from pymetrica.metric_calculators.cyclomatic_complexity import (
    CCCalculator,
)
from pymetrica.metric_calculators.halstead_volume import (
    HalsteadVolumeCalculator,
)


from .mi_metric import LayerMI, MaintainabilityIndexResults


class MaintainabilityIndexCalculator(MetricCalculator[MaintainabilityIndexResults]):
    def calculate_metric(
        self: "MaintainabilityIndexCalculator",
        codebase: Codebase,
    ) -> Metric[MaintainabilityIndexResults]:
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})
        cc_calculator = CCCalculator()
        hv_calculator = HalsteadVolumeCalculator()
        cc_metric = cc_calculator.calculate_metric(codebase)
        hv_metric = hv_calculator.calculate_metric(codebase)

        layers_results = list[LayerMI]()
        for layer_name, layer_files in layers.items():
            layer_name = layer_name.rsplit(os.sep, 1)[-1]
            layer_lloc = sum(file.lloc_number for file in layer_files)
            layer_cc = [
                result.cc_number
                for result in cc_metric.results.cc_result_per_layer
                if result.name == layer_name
            ][0]
            layer_hv = [
                result.hv_number
                for result in hv_metric.results.hv_per_layer
                if result.name == layer_name
            ][0]
            mi_classic = (
                171
                - 0.5 * math.sqrt(layer_hv * 0.05)
                - 0.075 * layer_cc
                - 0.5 * math.sqrt(layer_lloc)
            )
            mi_scaled = max(0, (mi_classic / 171) * 100)
            layers_results.append(
                LayerMI(
                    name=layer_name,
                    maintainability_index=mi_classic,
                    normalized_mi=mi_scaled,
                )
            )

        codebase_mi_classic = (
            171
            - 0.5 * math.sqrt(hv_metric.results.hv_number * 0.05)
            - 0.075 * cc_metric.results.cc_number
            - 0.5 * math.sqrt(codebase.lloc_number)
        )

        codebase_mi_scaled = max(0, (codebase_mi_classic / 171) * 100)

        return Metric(
            name="Maintainability Index",
            description=(
                "The Maintainability Index is a software metric that measures how "
                "maintainable the code is, based on various factors such as "
                "cyclomatic complexity, lines of code, and Halstead volume."
                "Higher scores indicate better maintainability, with scores "
                "below 20 suggesting very low maintainability."
            ),
            results=MaintainabilityIndexResults(
                maintainability_index=codebase_mi_classic,
                normalized_mi=codebase_mi_scaled,
                mi_per_layer=layers_results,
            ),
        )
