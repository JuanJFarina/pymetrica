from __future__ import annotations

from .mi_results import MIResults
from pymetrica.models import Codebase
from pymetrica.models import Metric
from pymetrica.models import MetricCalculator


class MaintainabilityIndexCalculator(MetricCalculator[MIResults]):
    def __init__(self):
        self.metric_name = 'Maintainability Index'
        self.metric_description = 'The Maintainability Index is a software metric that measures how maintainable the code is, based on various factors such as cyclomatic complexity, lines of code, and Halstead volume.'

    def calculate_metric(self, codebase: Codebase) -> Metric[MIResults]:
        return Metric(
            name=self.metric_name,
            description=self.metric_description,
            results=MIResults(
                maintainability_index=1.0,  # TODO replace with actual calculation logic
            ),
        )
