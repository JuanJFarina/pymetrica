import json

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerMI(BaseModel):
    name: str
    maintainability_index: float
    normalized_mi: float


class MaintainabilityIndexResults(Results):
    maintainability_index: float
    normalized_mi: float
    mi_per_layer: list[LayerMI]

    def get_dict(self) -> dict[str, int]:
        return self.get_dict()

    def get_json(self) -> str:
        return json.dumps(self.get_dict())

    def get_summary(self) -> str:
        summary = (
            f"\nMaintainability Index: {self.maintainability_index:.2f}\n "
            f"({self.normalized_mi:.2f} normalized)\n"
        )
        for layer in self.mi_per_layer:
            summary += f"  Layer {layer.name}: {layer.maintainability_index:.2f} ({layer.normalized_mi:.2f} normalized)\n"
        return summary


class MaintainabilityIndexMetric(Metric[MaintainabilityIndexResults]): ...
