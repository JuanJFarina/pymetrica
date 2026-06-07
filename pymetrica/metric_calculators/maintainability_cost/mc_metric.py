import json

from pydantic import BaseModel, Field

from pymetrica.models import Code, Metric, Results
from pymetrica.utils.settings import Config


class LayerMC(BaseModel):
    name: str
    maintainability_cost: float
    raw_line_cost: float


class MaintainabilityCostResults(Results):
    maintainability_cost: float
    raw_line_cost: float
    mc_per_layer: list[LayerMC]
    top_findings: list[Code] = Field(default_factory=list[Code])

    @property
    def dict_(self) -> dict[str, int]:
        return self.model_dump(exclude={"mc_per_layer", "top_findings"})

    @property
    def json_(self) -> str:
        return json.dumps(self.dict_)


class MaintainabilityCostMetric(Metric[MaintainabilityCostResults]):
    exit_code: int = 8

    @property
    def summary(self) -> str:
        summary = (
            f"\nCodebase MC: {self.results.maintainability_cost:.2f} "
            f"({self.results.raw_line_cost:.2f} raw MC, without size penalty)\n"
        )
        for layer in self.results.mc_per_layer:
            summary += (
                f"  Layer {layer.name}: "
                f"{layer.maintainability_cost:.2f} ({layer.raw_line_cost:.2f} raw)\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = ("-" * 40) + " MC DETAILS " + ("-" * 40) + "\n\n"
        message += (
            f"Maintainability Cost {self.results.maintainability_cost:.2f} exceeds "
            f"the fail threshold of {Config.mc_fail_threshold}. "
        )
        if self.results.raw_line_cost <= (self.results.maintainability_cost / 2):
            message += (
                "More than half of the maintainability cost comes from the "
                "sheer size of the codebase. This may indicate the codebase "
                "could benefit from design patterns, stricter typing, "
                "reusability of logic, etc.\n"
            )
        else:
            message += (
                "Average line of code is too complex, split up logic among "
                "multiple lines, use more indirections, and overall simplify.\n"
            )
        if self.results.top_findings:
            message += "Top findings for MC:\n"
            for finding in self.results.top_findings:
                message += (
                    f"  {finding.filepath} -> {finding.maintainability_cost:.2f}\n"
                )
        return message

    def exceeds_threshold(self, audit: bool = False) -> bool:
        return audit or (
            Config.mc_fail_threshold != 0
            and self.results.maintainability_cost > Config.mc_fail_threshold
        )
