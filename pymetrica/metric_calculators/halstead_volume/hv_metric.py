from typing import Any

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerHV(BaseModel):
    name: str
    hv_number: float


class HalsteadVolumeResults(Results):
    hv_number: float
    hv_per_layer: list[LayerHV]

    def get_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude={"hv_per_layer"})

    def get_json(self) -> str:
        return self.get_json()

    def get_summary(self) -> str:
        summary = f"\nHalstead Volume: {self.hv_number:.2f}\n"
        for layer in self.hv_per_layer:
            summary += f"  Layer {layer.name}: {layer.hv_number:.2f}\n"
        return summary


class HalsteadVolumeMetric(Metric[HalsteadVolumeResults]): ...
