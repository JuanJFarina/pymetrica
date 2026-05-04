import json

from pydantic import BaseModel

from pymetrica.models import Metric, Results
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

    all_primitives_failed: bool = False
    targeted_primitives_failed: bool = False

    @property
    def dict_(self) -> dict[str, int]:
        return self.model_dump(exclude={"po_per_layer"})

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
        message = ""
        if self.all_primitives_failed:
            message += (
                "Primitives found are "
                f"{self.all_primitives_percent:.2f}% of codebase "
                f"exceeding the fail threshold of {Config.po_all_fail_threshold}%. "
            )
        if self.targeted_primitives_failed:
            if message:
                message += "\n"
            message += (
                "Critical primitives found are "
                f"{self.targeted_primitives_percent:.2f}% of codebase "
                f"exceeding the fail threshold of {Config.po_targeted_fail_threshold}%. "
            )
        return message

    @property
    def exceeds_threshold(self) -> bool:
        self.all_primitives_failed = (
            Config.po_all_fails
            and self.all_primitives_percent > Config.po_all_fail_threshold
        )
        self.targeted_primitives_failed = (
            Config.po_targeted_fails
            and self.targeted_primitives_percent > Config.po_targeted_fail_threshold
        )
        return self.all_primitives_failed or self.targeted_primitives_failed


class PrimitiveObsessionMetric(Metric[PrimitiveObsessionResults]): ...
