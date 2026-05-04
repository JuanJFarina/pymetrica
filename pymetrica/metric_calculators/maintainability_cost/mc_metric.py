import json

from pydantic import BaseModel

from pymetrica.models import Metric, Results
from pymetrica.utils.settings import Config


class LayerMC(BaseModel):
    name: str
    maintainability_cost: float
    raw_line_cost: float


class MaintainabilityCostResults(Results):
    maintainability_cost: float
    raw_line_cost: float
    mc_per_layer: list[LayerMC]

    @property
    def dict_(self) -> dict[str, int]:
        return self.model_dump(exclude={"mc_per_layer"})

    @property
    def json_(self) -> str:
        return json.dumps(self.dict_)

    @property
    def summary(self) -> str:
        summary = (
            f"\nCodebase MC: {self.maintainability_cost:.2f} "
            f"({self.raw_line_cost:.2f} raw MC, without size penalty)\n"
        )
        for layer in self.mc_per_layer:
            summary += (
                f"  Layer {layer.name}: "
                f"{layer.maintainability_cost:.2f} ({layer.raw_line_cost:.2f} raw)\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = (
            f"Maintainability Cost {self.maintainability_cost:.2f}% exceeds "
            f"the fail threshold of {Config.mc_fail_threshold}%. "
        )
        if self.raw_line_cost <= (self.maintainability_cost / 2):
            message += (
                "More than half of the maintainability cost comes from the "
                "sheer size of the codebase. This may indicate the codebase "
                "could benefit from design patterns, stricter typing, "
                "reusability of logic, etc."
            )
        else:
            message += (
                "Average line of code is too complex, split up logic among "
                "multiple lines, use more indirections, and overall simplify."
            )
        return message

    @property
    def exceeds_threshold(self) -> bool:
        return Config.mc_fails and self.maintainability_cost > Config.mc_fail_threshold


class MaintainabilityCostMetric(Metric[MaintainabilityCostResults]): ...
