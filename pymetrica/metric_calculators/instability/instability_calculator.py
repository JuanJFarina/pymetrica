from os import sep

from pymetrica.models import Code, Codebase, Metric, MetricCalculator

from .instability_logic import calculate_instability
from .instability_metric import InstabilityMetric, InstabilityResults

Layer = str
Files = list[Code]


def get_layer_name(layer_path: str) -> str:
    return layer_path.rsplit(sep)[-1]


class InstabilityCalculator(MetricCalculator[InstabilityResults]):
    def calculate_metric(
        self: "InstabilityCalculator",
        codebase: Codebase,
    ) -> Metric[InstabilityResults]:
        codebase.layers.update({codebase.root_folder_path: codebase.root_files})
        files_by_layer: dict[Layer, Files] = codebase.layers.copy()

        layers_instability = dict[Layer, float]()

        for layer in files_by_layer:
            if layer == codebase.root_folder_path:
                layers_instability["root"] = calculate_instability(
                    layer,
                    files_by_layer,
                )
                continue
            layers_instability[get_layer_name(layer)] = calculate_instability(
                layer,
                files_by_layer,
            )

        return InstabilityMetric(
            name="Instability",
            description=(
                "The Instability metric measures the coupling and stability of each layer. "
                "It is calculated based on the ratio of outgoing dependencies to the total "
                "number of dependencies (incoming + outgoing). A higher value indicates "
                "greater instability."
            ),
            results=InstabilityResults(
                instability=layers_instability,
            ),
        )
