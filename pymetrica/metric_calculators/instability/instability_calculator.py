from os import sep
from pathlib import Path

from pymetrica.models import Code, Codebase, Metric, MetricCalculator

from .instability_logic import calculate_instability
from .instability_metric import InstabilityResults

Layer = str
Files = list[Code]


def get_layer_name(layer_path: str) -> str:
    return layer_path.rsplit(sep)[-2] + "." + layer_path.rsplit(sep)[-1]


class InstabilityCalculator(MetricCalculator[InstabilityResults]):
    def calculate_metric(
        self: "InstabilityCalculator",
        codebase: Codebase,
    ) -> Metric[InstabilityResults]:
        layers = [
            str(dir)
            for dir in Path(codebase.root_folder_path).iterdir()
            if dir.is_dir() and dir.name != "__pycache__"
        ]

        files_by_layer: dict[Layer, Files] = {layer: [] for layer in layers}

        for file in codebase.files:
            for layer in layers:
                if layer in str(file.filepath):
                    files_by_layer.get(layer, []).append(file)
                    break

        layers_instability = dict[Layer, float]()

        for layer in files_by_layer.keys():
            layers_instability[get_layer_name(layer)] = calculate_instability(
                layer,
                files_by_layer,
            )

        print(f"{layers_instability = }")

        return Metric(
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
