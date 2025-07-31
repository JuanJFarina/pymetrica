from pymetrica.models import Codebase, MetricCalculator
from .aloc_metric import AlocMetric, AlocResults
from .first_pass import gather_loc_and_classes
from .second_pass import count_uninstantiated_loc


class AlocCalculator(MetricCalculator[AlocResults]):
    def calculate_metric(self: "AlocCalculator", codebase: Codebase) -> AlocMetric:
        first_pass_results = gather_loc_and_classes(codebase)
        print(first_pass_results)
        second_pass_results = count_uninstantiated_loc(codebase, first_pass_results["classes"])
        print(second_pass_results)
        total_aloc: int = first_pass_results["aloc"] + second_pass_results
        return AlocMetric(
            name="aloc",
            description="aloc",
            results=AlocResults(
                aloc=total_aloc,
                aloc_percentage=total_aloc / codebase.lloc_number * 100,
            ),
        )
