from typing import Any

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerAloc(BaseModel):
    name: str
    aloc_number: int
    aloc_percentage: float


class AlocResults(Results):
    aloc_number: int
    aloc_percentage: float
    aloc_result_per_layer: list[LayerAloc]

    def get_dict(self) -> dict[str, Any]:
        return self.get_dict()

    def get_json(self) -> str:
        return self.get_json()

    def get_summary(self) -> str:
        summary = (
            f"\nTotal ALOC: "
            f"{self.aloc_number} ({self.aloc_percentage:0.2f}% of total LLOC)\n"
        )
        for layer in self.aloc_result_per_layer:
            summary += (
                f"  Layer {layer.name} ALOC: "
                f"{layer.aloc_number} ({layer.aloc_percentage:0.2f}%)\n"
            )
        return summary


class AlocMetric(Metric[AlocResults]): ...
