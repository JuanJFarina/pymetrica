from pymetrica.models import Codebase, MetricCalculator
from .aloc_metric import AlocMetric, AlocResults
from .first_pass import gather_loc_and_classes
from .second_pass import count_uninstantiated_loc


class AlocCalculator(MetricCalculator[AlocResults]):
    def calculate_metric(self: "AlocCalculator", codebase: Codebase) -> AlocMetric:
        preliminary_results = gather_loc_and_classes(codebase)
        uninstantiated_loc = count_uninstantiated_loc(
            codebase, preliminary_results.classes
        )
        total_aloc: int = preliminary_results.aloc + uninstantiated_loc
        return AlocMetric(
            name="aloc",
            description="aloc",
            results=AlocResults(
                aloc=total_aloc,
                aloc_percentage=total_aloc / codebase.lloc_number * 100,
            ),
        )
