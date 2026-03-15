import json

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerMC(BaseModel):
    name: str
    maintainability_cost: float
    raw_line_cost: float


class MaintainabilityCostResults(Results):
    maintainability_cost: float
    raw_line_cost: float
    mc_per_layer: list[LayerMC]

    def get_dict(self) -> dict[str, int]:
        return self.model_dump(exclude={"mc_per_layer"})

    def get_json(self) -> str:
        return json.dumps(self.get_dict())

    def get_summary(self) -> str:
        summary = (
            f"\nCodebase MC: {self.maintainability_cost:.2f} "
            f"({self.raw_line_cost:.2f} raw MC, without size penalty)\n"
        )
        for layer in self.mc_per_layer:
            summary += (
                f"  Layer {layer.name}: "
                f"{layer.maintainability_cost:.2f} ({layer.raw_line_cost:.2f} raw)\n"
            )
        return summary


class MaintainabilityCostMetric(Metric[MaintainabilityCostResults]): ...
