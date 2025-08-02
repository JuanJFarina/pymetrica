from __future__ import annotations

from .aloc_metric import AlocMetric
from .aloc_metric import AlocResults
from .first_pass import gather_loc_and_classes
from .second_pass import count_uninstantiated_loc
from pymetrica.models import Codebase
from pymetrica.models import MetricCalculator


class AlocCalculator(MetricCalculator[AlocResults]):
    def calculate_metric(self: AlocCalculator, codebase: Codebase) -> AlocMetric:
        preliminary_results = gather_loc_and_classes(codebase)
        uninstantiated_loc = count_uninstantiated_loc(
            codebase, preliminary_results.classes,
        )
        total_aloc: int = preliminary_results.aloc + uninstantiated_loc
        return AlocMetric(
            name='Abstract Lines of Code',
            description='Abstract Lines of Code (ALOC) is a software metric that measures the number of lines of code in a program that are not concrete operations but rather indirections or abstract constructs and definitions.',
            results=AlocResults(
                aloc_number=total_aloc,
                aloc_percentage=total_aloc / codebase.lloc_number * 100,
            ),
        )
