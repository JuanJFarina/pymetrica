import json

from pydantic import BaseModel, Field

from pymetrica.models import Code, Metric, Results
from pymetrica.utils.settings import Config


class LayerPO(BaseModel):
    name: str
    all_primitives: int
    targeted_primitives: int


class PrimitiveObsessionResults(Results):
    all_primitives: int
    targeted_primitives: int
    all_primitives_percent: float
    targeted_primitives_percent: float
    po_per_layer: list[LayerPO]
    top_findings_all: list[Code] = Field(default_factory=list[Code])
    top_findings_targeted: list[Code] = Field(default_factory=list[Code])

    all_primitives_failed: bool = False
    targeted_primitives_failed: bool = False

    @property
    def dict_(self) -> dict[str, int]:
        return self.model_dump(
            exclude={
                "all_primitives",
                "targeted_primitives",
                "all_primitives_failed",
                "targeted_primitives_failed",
                "po_per_layer",
                "top_findings_all",
                "top_findings_targeted",
            },
        )

    @property
    def json_(self) -> str:
        return json.dumps(self.json_)

    @property
    def summary(self) -> str:
        summary = (
            f"\nTotal codebase primitives: {self.all_primitives} "
            f"({self.all_primitives_percent:.2f}%) "
            f"with {self.targeted_primitives} critically loose "
            f"({self.targeted_primitives_percent:.2f}%)\n"
        )
        for layer in self.po_per_layer:
            summary += (
                f"  Layer {layer.name}: "
                f"{layer.all_primitives} ({layer.targeted_primitives})\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = ("-" * 40) + " PO DETAILS " + ("-" * 40) + "\n\n"
        if self.all_primitives_failed:
            message += (
                "Primitives found are "
                f"{self.all_primitives_percent:.2f}% of codebase "
                f"exceeding the fail threshold of {Config.po_all_fail_threshold}%."
                "Consider using type aliases or other data structures.\n"
            )
            if self.top_findings_all:
                message += "Top findings for ALL:\n"
                for finding in self.top_findings_all:
                    message += f"  {finding.filepath} -> {finding.all_primitives}\n"
        if self.targeted_primitives_failed:
            if message:
                message += "\n"
            message += (
                "Critical primitives found are "
                f"{self.targeted_primitives_percent:.2f}% of codebase "
                f"exceeding the fail threshold of {Config.po_targeted_fail_threshold}%. "
                "Consider using more classes.\n"
            )
            if self.top_findings_targeted:
                message += "Top findings for CRITICAL:\n"
                for finding in self.top_findings_targeted:
                    message += (
                        f"  {finding.filepath} -> {finding.targeted_primitives}\n"
                    )
        return message

    @property
    def exceeds_threshold(self) -> bool:
        self.all_primitives_failed = (
            Config.po_all_fail_threshold != 0
            and self.all_primitives_percent > Config.po_all_fail_threshold
        )
        self.targeted_primitives_failed = (
            Config.po_targeted_fail_threshold != 0
            and self.targeted_primitives_percent > Config.po_targeted_fail_threshold
        )
        return self.all_primitives_failed or self.targeted_primitives_failed


class PrimitiveObsessionMetric(Metric[PrimitiveObsessionResults]):
    exit_code: int = 16
