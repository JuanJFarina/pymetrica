import os

from pymetrica.models import Codebase, MetricCalculator

from .aloc_metric import AlocMetric, AlocResults, LayerAloc
from .first_pass import gather_loc_and_classes
from .second_pass import called_classes


class AlocCalculator(MetricCalculator[AlocResults]):
    def calculate_metric(self: "AlocCalculator", codebase: Codebase) -> AlocMetric:
        layer_results = list[LayerAloc]()
        layers = codebase.layers.copy()
        layers.update({"root": codebase.root_files})
        all_called_classes = set[str]()
        classes_per_layer = dict[str, dict[str, int]]()

        for name, files in layers.items():
            preliminary_results = gather_loc_and_classes(files)
            classes_per_layer[name] = {}
            classes_per_layer[name].update(preliminary_results.classes)
            layer_results.append(
                LayerAloc(
                    name=name.rsplit(os.sep, 1)[-1],
                    aloc_number=preliminary_results.aloc,
                    aloc_percentage=preliminary_results.aloc
                    / codebase.lloc_number
                    * 100,
                ),
            )
        all_classes = dict[str, int]()
        for classes in classes_per_layer.values():
            all_classes.update(classes)
        all_called_classes = called_classes(codebase.files, all_classes)
        for layer in classes_per_layer:
            for layer_result in layer_results:
                if layer_result.name == layer:
                    layer_result.aloc_number += sum(
                        loc
                        for cls, loc in classes_per_layer[layer].items()
                        if cls not in all_called_classes
                    )
                    layer_result.aloc_percentage = (
                        layer_result.aloc_number / codebase.lloc_number * 100
                    )

        total_aloc = sum(layer.aloc_number for layer in layer_results)
        return AlocMetric(
            name="Abstract Lines of Code",
            description=(
                "Abstract Lines of Code (ALOC) is a software metric that "
                "measures the number of lines of code in a program that are "
                "not concrete operations but rather indirections or abstract "
                "constructs and definitions."
            ),
            results=AlocResults(
                aloc_number=total_aloc,
                aloc_percentage=total_aloc / codebase.lloc_number * 100,
                aloc_result_per_layer=sorted(
                    layer_results,
                    key=lambda x: x.aloc_number,
                    reverse=True,
                ),
            ),
        )
