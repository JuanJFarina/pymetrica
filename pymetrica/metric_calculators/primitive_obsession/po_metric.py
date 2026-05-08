import json

from pydantic import BaseModel, Field

from pymetrica.models import Code, Metric, Results
from pymetrica.utils.settings import Config

Percent = float


class LayerPO(BaseModel):
    name: str
    all_primitives: int
    targeted_primitives: int


class PrimitiveObsessionResults(Results):
    all_primitives: int
    targeted_primitives: int
    all_primitives_percent: Percent
    targeted_primitives_percent: Percent
    po_per_layer: list[LayerPO]
    top_findings_all: list[Code] = Field(default_factory=list[Code])
    top_findings_targeted: list[Code] = Field(default_factory=list[Code])

    all_primitives_failed: bool = False
    targeted_primitives_failed: bool = False

    @property
    def dict_(self) -> dict[str, Percent]:
        return self.model_dump(
            exclude={
                "all_primitives",
                "targeted_primitives",
                "po_per_layer",
                "top_findings_all",
                "top_findings_targeted",
                "all_primitives_failed",
                "targeted_primitives_failed",
            },
        )

    @property
    def json_(self) -> str:
        return json.dumps(self.json_)


class PrimitiveObsessionMetric(Metric[PrimitiveObsessionResults]):
    exit_code: int = 16

    @property
    def summary(self) -> str:
        summary = (
            f"\nTotal codebase primitives: {self.results.all_primitives} "
            f"({self.results.all_primitives_percent:.2f}%) "
            f"with {self.results.targeted_primitives} critically loose "
            f"({self.results.targeted_primitives_percent:.2f}%)\n"
        )
        for layer in self.results.po_per_layer:
            summary += (
                f"  Layer {layer.name}: "
                f"{layer.all_primitives} ({layer.targeted_primitives})\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = ("-" * 40) + " PO DETAILS " + ("-" * 40) + "\n\n"
        if self.results.all_primitives_failed:
            message += (
                "Primitives found are "
                f"{self.results.all_primitives_percent:.2f}% of codebase "
                f"exceeding the fail threshold of {Config.po_all_fail_threshold}%. "
                "Consider using type aliases or other data structures.\n"
            )
            if self.results.top_findings_all:
                message += "Top findings for ALL:\n"
                for finding in self.results.top_findings_all:
                    message += f"  {finding.filepath} -> {finding.all_primitives}\n"
        if self.results.targeted_primitives_failed:
            if message:
                message += "\n"
            message += (
                "Critical primitives found are "
                f"{self.results.targeted_primitives_percent:.2f}% of codebase "
                f"exceeding the fail threshold of {Config.po_targeted_fail_threshold}%. "
                "Consider using more classes.\n"
            )
            if self.results.top_findings_targeted:
                message += "Top findings for CRITICAL:\n"
                for finding in self.results.top_findings_targeted:
                    message += (
                        f"  {finding.filepath} -> {finding.targeted_primitives}\n"
                    )
        return message

    def exceeds_threshold(self, audit: bool = False) -> bool:
        self.results.all_primitives_failed = audit or (
            Config.po_all_fail_threshold != 0
            and self.results.all_primitives_percent > Config.po_all_fail_threshold
        )
        self.results.targeted_primitives_failed = audit or (
            Config.po_targeted_fail_threshold != 0
            and self.results.targeted_primitives_percent
            > Config.po_targeted_fail_threshold
        )
        return (
            self.results.all_primitives_failed
            or self.results.targeted_primitives_failed
        )
