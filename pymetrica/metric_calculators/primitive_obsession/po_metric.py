import json

from pydantic import BaseModel

from pymetrica.models import Metric, Results
from pymetrica.utils.settings import Config


class LayerPO(BaseModel):
    name: str
    total_primitives: int
    targeted_primitives: int


class PrimitiveObsessionResults(Results):
    total_primitives: int
    targeted_primitives: int
    po_per_layer: list[LayerPO]

    @property
    def dict_(self) -> dict[str, int]:
        return self.model_dump(exclude={"po_per_layer"})

    @property
    def json_(self) -> str:
        return json.dumps(self.dict_)

    @property
    def summary(self) -> str:
        summary = (
            f"\nTotal Codebase Primitives: {self.total_primitives} "
            f"({self.targeted_primitives} critically loose types)\n"
        )
        for layer in self.po_per_layer:
            summary += (
                f"  Layer {layer.name}: "
                f"{layer.total_primitives} ({layer.targeted_primitives} targeted)\n"
            )
        return summary

    @property
    def fail_message(self) -> str:
        message = (
            f"Primitive Obsession {self.primitive_obsession}% exceeds "
            f"the fail threshold of {Config.po_fail_threshold}%. "
        )
        return message

    @property
    def exceeds_threshold(self) -> bool:
        return super().exceeds_threshold


class PrimitiveObsessionMetric(Metric[PrimitiveObsessionResults]): ...
