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

from .mc_metric import LayerMC, MaintainabilityCostMetric, MaintainabilityCostResults


class MaintainabilityCostCalculator(MetricCalculator[MaintainabilityCostResults]):
    def calculate_metric(  # pylint: disable=too-many-locals
        self: "MaintainabilityCostCalculator",
        codebase: Codebase,
    ) -> Metric[MaintainabilityCostResults]:
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})
        cc_calculator = CCCalculator()
        hv_calculator = HalsteadVolumeCalculator()
        cc_metric = cc_calculator.calculate_metric(codebase)
        hv_metric = hv_calculator.calculate_metric(codebase)

        layers_results = list[LayerMC]()
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

            hv_density = layer_hv / (layer_lloc or 1)
            cc_density = layer_cc / (layer_lloc or 1)
            average_lloc_mc = (hv_density * ((cc_density) * 100 or 1)) / 20
            log.debug(
                f"Layer: {layer_name}, HV Density: {hv_density}, "
                f"CC Density: {cc_density}, Average LLOC MC: {average_lloc_mc}",
            )
            mc = average_lloc_mc + layer_lloc * 0.001
            layers_results.append(
                LayerMC(
                    name=layer_name,
                    maintainability_cost=mc,
                    raw_line_cost=average_lloc_mc,
                ),
            )

        codebase_hv_density = hv_metric.results.hv_number / (codebase.lloc_number or 1)
        codebase_cc_density = cc_metric.results.cc_number / (codebase.lloc_number or 1)
        codebase_average_lloc_mc = (
            codebase_hv_density * ((codebase_cc_density) * 100 or 1)
        ) / 20
        log.debug(
            f"Codebase HV Density: {codebase_hv_density}, "
            f"CC Density {codebase_cc_density}, Average LLOC MC: {codebase_average_lloc_mc}",
        )
        codebase_mc = codebase_average_lloc_mc + codebase.lloc_number * 0.001

        return MaintainabilityCostMetric(
            name="Maintainability Cost",
            description=(
                "MC is a software metric that measures how expensive it is to "
                "maintain the code, based on various factors such as "
                "Cyclomatic Complexity, Logical Lines Of Code, and Halstead "
                "Volume. Lower scores indicate better maintainability, with "
                "scores above 20 suggesting moderate maintainability and "
                "scores above 50 indicating poor maintainability."
            ),
            results=MaintainabilityCostResults(
                maintainability_cost=codebase_mc,
                raw_line_cost=codebase_average_lloc_mc,
                mc_per_layer=layers_results,
            ),
        )
