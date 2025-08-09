import math
from pymetrica.models import Codebase, Metric, MetricCalculator
from pymetrica.metric_calculators.cyclomatic_complexity.cc_calculator import (
    CCCalculator,
)
from pymetrica.metric_calculators.halstead_volume.hv_calculator import (
    HalsteadVolumeCalculator,
)

from .mi_results import MaintainabilityIndexResults


class MaintainabilityIndexCalculator(MetricCalculator[MaintainabilityIndexResults]):
    def calculate_metric(
        self: "MaintainabilityIndexCalculator",
        codebase: Codebase,
    ) -> Metric[MaintainabilityIndexResults]:
        cc_calculator = CCCalculator()
        hv_calculator = HalsteadVolumeCalculator()
        cc_metric = cc_calculator.calculate_metric(codebase)
        hv_metric = hv_calculator.calculate_metric(codebase)

        mi_classic = (
            171
            - 5.2 * math.log(hv_metric.results.hv_number)
            - 0.23 * cc_metric.results.cc_number
            - 16.2 * math.log(codebase.lloc_number)
        )

        mi_scaled = max(0, (mi_classic / 171) * 100)

        return Metric(
            name="Maintainability Index",
            description=(
                "The Maintainability Index is a software metric that measures how "
                "maintainable the code is, based on various factors such as "
                "cyclomatic complexity, lines of code, and Halstead volume."
            ),
            results=MaintainabilityIndexResults(
                maintainability_index=mi_classic,
                normalized_mi=mi_scaled,
            ),
        )
