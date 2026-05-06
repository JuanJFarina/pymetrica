from typing import Any

from pydantic import BaseModel, Field

from pymetrica.models import Code, Metric, Results
from pymetrica.utils.settings import Config


class LayerCC(BaseModel):
    name: str
    cc_number: int
    lloc_per_cc: float


class CCResults(Results):
    cc_number: int
    lloc_per_cc: float
    cc_result_per_layer: list[LayerCC]
    top_findings: list[Code] = Field(default_factory=list[Code])

    @property
    def dict_(self) -> dict[str, Any]:
        return self.model_dump(exclude={"cc_result_per_layer", "top_findings"})

    @property
    def json_(self) -> str:
        return self.json_


class CCMetric(Metric[CCResults]):
    exit_code: int = 2

    @property
    def summary(self) -> str:
        summary = (
            f"\nTotal CC: {self.results.cc_number} "
            f"({self.results.lloc_per_cc:0.2f} LLOC per CC)\n"
        )
        for layer in self.results.cc_result_per_layer:
            summary += (
                f"  Layer {layer.name} CC: "
                f"{layer.cc_number} ({layer.lloc_per_cc:0.2f} LLOC per CC)\n"
            )
        return summary

    @property
    def exceeds_threshold(self) -> bool:
        return (
            Config.cc_fail_threshold != 0
            and self.results.lloc_per_cc < Config.cc_fail_threshold
        )

    @property
    def fail_message(self) -> str:
        message = ("-" * 40) + " CC DETAILS " + ("-" * 40) + "\n\n"
        message += (
            f"LLOC per CC {self.results.lloc_per_cc:.2f} is below "
            f"the fail threshold of {Config.cc_fail_threshold}. "
            "Reduce the number of logic branches and decision points by "
            "simplifying logic, using strict typing, and use multiple "
            "lines of code to simplify complex expressions.\n"
        )
        if self.results.top_findings:
            message += "Top findings for CC:\n"
            for finding in self.results.top_findings:
                message += f"  {finding.filepath} -> {finding.cc_number}\n"
        return message
