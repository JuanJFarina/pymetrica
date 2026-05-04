from typing import Any

from pydantic import BaseModel

from pymetrica.models import Metric, Results
from pymetrica.utils.settings import Config


class LayerAloc(BaseModel):
    name: str
    aloc_number: int
    aloc_percentage: float


class AlocResults(Results):
    aloc_number: int
    aloc_percentage: float
    aloc_result_per_layer: list[LayerAloc]

    @property
    def dict_(self) -> dict[str, Any]:
        return self.model_dump(exclude={"aloc_result_per_layer"})

    @property
    def json_(self) -> str:
        return self.json_

    @property
    def summary(self) -> str:
        summary = (
            "\nTotal ALOC: "
            f"{self.aloc_number} ({self.aloc_percentage:0.2f}% of total LLOC)\n"
        )
        for layer in self.aloc_result_per_layer:
            summary += (
                f"  Layer {layer.name} ALOC: "
                f"{layer.aloc_number} ({layer.aloc_percentage:0.2f}%)\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = (
            f"ALOC percentage {self.aloc_percentage:.2f}% exceeds "
            f"the fail threshold of {Config.aloc_fail_threshold}%. "
            "Reduce the number of functions and classes to improve this "
            "metric."
        )
        return message

    @property
    def exceeds_threshold(self) -> bool:
        return Config.aloc_fails and self.aloc_percentage > Config.aloc_fail_threshold


class AlocMetric(Metric[AlocResults]): ...
