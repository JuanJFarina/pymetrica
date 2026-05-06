from typing import Any

from pydantic import BaseModel, Field

from pymetrica.models import Code, Metric, Results
from pymetrica.utils.settings import Config


class LayerHV(BaseModel):
    name: str
    hv_number: float
    hv_per_lloc: float


class HalsteadVolumeResults(Results):
    hv_number: float
    hv_per_lloc: float
    hv_per_layer: list[LayerHV]
    top_findings: list[Code] = Field(default_factory=list[Code])

    @property
    def dict_(self) -> dict[str, Any]:
        return self.model_dump(exclude={"hv_per_layer", "top_findings"})

    @property
    def json_(self) -> str:
        return self.json_


class HalsteadVolumeMetric(Metric[HalsteadVolumeResults]):
    exit_code: int = 4

    @property
    def summary(self) -> str:
        summary = (
            f"\nHalstead Volume: {self.results.hv_number:.2f} "
            f"({self.results.hv_per_lloc:.2f} per LLOC)\n"
        )
        for layer in self.results.hv_per_layer:
            summary += (
                f"  Layer {layer.name}: {layer.hv_number:.2f} "
                f"({layer.hv_per_lloc:.2f} per LLOC)\n"
            )
        return summary

    @property
    def exceeds_threshold(self) -> bool:
        return (
            Config.hv_fail_threshold != 0
            and self.results.hv_per_lloc > Config.hv_fail_threshold
        )

    @property
    def fail_message(self) -> str:
        message = ("-" * 40) + " HV DETAILS " + ("-" * 40) + "\n\n"
        message += (
            f"Halstead Volume per LLOC {self.results.hv_per_lloc:.2f} exceeds "
            f"the fail threshold of {Config.hv_fail_threshold}. "
            "Reduce the number of unique operators and operands, and the "
            "overall size of the program.\n"
        )
        if self.results.top_findings:
            message += "Top findings for HV:\n"
            for finding in self.results.top_findings:
                message += f"  {finding.filepath} -> {finding.hv_number:.2f}\n"
        return message
