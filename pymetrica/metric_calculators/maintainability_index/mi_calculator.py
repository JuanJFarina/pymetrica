import math
import logging
from pymetrica.models import Codebase, Metric, MetricCalculator

# the following imports need to be more specific to avoid cyclic imports
from pymetrica.metric_calculators.cyclomatic_complexity import (
    CCCalculator,
)
from pymetrica.metric_calculators.halstead_volume import (
    HalsteadVolumeCalculator,
)

from .mi_metric import MaintainabilityIndexResults


class MaintainabilityIndexCalculator(MetricCalculator[MaintainabilityIndexResults]):
    def calculate_metric(
        self: "MaintainabilityIndexCalculator",
        codebase: Codebase,
    ) -> Metric[MaintainabilityIndexResults]:
        cc_calculator = CCCalculator()
        hv_calculator = HalsteadVolumeCalculator()
        cc_metric = cc_calculator.calculate_metric(codebase)
        hv_metric = hv_calculator.calculate_metric(codebase)

        print(
            f"MaintainabilityIndexCalculator.calculate_metric.{hv_metric.results.hv_number = }"
        )
        print(
            f"MaintainabilityIndexCalculator.calculate_metric.{cc_metric.results.cc_number = }"
        )
        print(
            f"MaintainabilityIndexCalculator.calculate_metric.{codebase.lloc_number = }"
        )

        print(
            "MaintainabilityIndexCalculator.calculate_metric.mi_classic = 171 "
            f"- {1.3 * math.log(hv_metric.results.hv_number)} "
            f"- {0.0575 * cc_metric.results.cc_number} "
            f"- {4.05 * math.log(codebase.lloc_number)}"
        )

        mi_classic = (
            171
            - 1.3
            * math.log(
                hv_metric.results.hv_number
            )  # softened to 1/4 of traditional weight
            - 0.0575
            * cc_metric.results.cc_number  # softened to 1/4 of traditional weight
            - 4.05
            * math.log(codebase.lloc_number)  # softened to 1/4 of traditional weight
        )

        mi_scaled = max(0, (mi_classic / 171) * 100)

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
                maintainability_index=mi_classic,
                normalized_mi=mi_scaled,
            ),
        )
