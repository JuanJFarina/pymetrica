from typing import Any

from pydantic import BaseModel, Field

from pymetrica.models import Code, Metric, Results
from pymetrica.utils.settings import Config


class LayerAloc(BaseModel):
    name: str
    aloc_number: int
    aloc_percentage: float


class AlocResults(Results):
    aloc_number: int
    aloc_percentage: float
    aloc_result_per_layer: list[LayerAloc]
    top_findings: list[Code] = Field(default_factory=list[Code])

    @property
    def dict_(self) -> dict[str, Any]:
        return self.model_dump(exclude={"aloc_result_per_layer", "top_findings"})

    @property
    def json_(self) -> str:
        return self.json_


class AlocMetric(Metric[AlocResults]):
    exit_code: int = 1

    @property
    def summary(self) -> str:
        summary = (
            "\nTotal ALOC: "
            f"{self.results.aloc_number} ({self.results.aloc_percentage:0.2f}% of total LLOC)\n"
        )
        for layer in self.results.aloc_result_per_layer:
            summary += (
                f"  Layer {layer.name} ALOC: "
                f"{layer.aloc_number} ({layer.aloc_percentage:0.2f}%)\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = ("-" * 40) + " ALOC DETAILS " + ("-" * 40) + "\n\n"
        message += (
            f"ALOC percentage {self.results.aloc_percentage:.2f}% exceeds "
            f"the fail threshold of {Config.aloc_fail_threshold}%. "
            "Reduce the number of functions and classes to improve this "
            "metric.\n"
        )
        if self.results.top_findings:
            message += "Top findings for ALOC:\n"
            for finding in self.results.top_findings:
                message += f"  {finding.filepath} -> {finding.aloc_number}\n"
        return message

    def exceeds_threshold(self, audit: bool = False) -> bool:
        return audit or (
            Config.aloc_fail_threshold != 0
            and self.results.aloc_percentage > Config.aloc_fail_threshold
        )
