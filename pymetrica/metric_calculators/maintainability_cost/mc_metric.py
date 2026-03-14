import json

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerMC(BaseModel):
    name: str
    maintainability_cost: float


class MaintainabilityCostResults(Results):
    maintainability_cost: float
    mc_per_layer: list[LayerMC]

    def get_dict(self) -> dict[str, int]:
        return self.model_dump(exclude={"mc_per_layer"})

    def get_json(self) -> str:
        return json.dumps(self.get_dict())

    def get_summary(self) -> str:
        summary = f"\nCodebase MC: {self.maintainability_cost:.2f}\n"
        for layer in self.mc_per_layer:
            summary += f"  Layer {layer.name}: {layer.maintainability_cost:.2f}\n"
        return summary


class MaintainabilityCostMetric(Metric[MaintainabilityCostResults]): ...
