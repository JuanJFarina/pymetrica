from typing import Any

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerCC(BaseModel):
    name: str
    cc_number: int
    cc_lloc_ratio: float


class CCResults(Results):
    cc_number: int
    cc_lloc_ratio: float
    cc_result_per_layer: list[LayerCC]

    def get_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude={"cc_result_per_layer"})

    def get_json(self) -> str:
        return self.get_json()

    def get_summary(self) -> str:
        summary = (
            f"\nTotal CC: {self.cc_number} ({self.cc_lloc_ratio:0.2f} LLOC per CC)\n"
        )
        for layer in self.cc_result_per_layer:
            summary += (
                f"  Layer {layer.name} CC: "
                f"{layer.cc_number} ({layer.cc_lloc_ratio:0.2f} LLOC per CC)\n"
            )
        return summary


class CCMetric(Metric[CCResults]): ...
