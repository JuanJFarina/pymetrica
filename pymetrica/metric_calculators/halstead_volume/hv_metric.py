from typing import Any

from pydantic import BaseModel

from pymetrica.models import Metric, Results
from pymetrica.utils.settings import Config


class LayerHV(BaseModel):
    name: str
    hv_number: float
    hv_per_lloc: float


class HalsteadVolumeResults(Results):
    hv_number: float
    hv_per_lloc: float
    hv_per_layer: list[LayerHV]

    @property
    def dict_(self) -> dict[str, Any]:
        return self.model_dump(exclude={"hv_per_layer"})

    @property
    def json_(self) -> str:
        return self.json_

    @property
    def summary(self) -> str:
        summary = f"\nHalstead Volume: {self.hv_number:.2f} ({self.hv_per_lloc:.2f} per LLOC)\n"
        for layer in self.hv_per_layer:
            summary += (
                f"  Layer {layer.name}: {layer.hv_number:.2f} "
                f"({layer.hv_per_lloc:.2f} per LLOC)\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = (
            f"Halstead Volume per LLOC {self.hv_per_lloc:.2f} exceeds "
            f"the fail threshold of {Config.hv_fail_threshold}. "
            "Reduce the number of unique operators and operands, and the "
            "overall size of the program."
        )
        return message

    @property
    def exceeds_threshold(self) -> bool:
        return Config.hv_fails and self.hv_per_lloc > Config.hv_fail_threshold


class HalsteadVolumeMetric(Metric[HalsteadVolumeResults]): ...
