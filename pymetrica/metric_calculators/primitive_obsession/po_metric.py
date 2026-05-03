import json

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerPO(BaseModel):
    name: str
    total_primitives: int
    targeted_primitives: int


class PrimitiveObsessionResults(Results):
    total_primitives: int
    targeted_primitives: int
    po_per_layer: list[LayerPO]

    def get_dict(self) -> dict[str, int]:
        return self.model_dump(exclude={"po_per_layer"})

    def get_json(self) -> str:
        return json.dumps(self.get_dict())

    def get_summary(self) -> str:
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

    def get_fail_message(self, fail_threshold: int) -> str:
        message = (
            f"Primitive Obsession {self.primitive_obsession}% exceeds "
            f"the fail threshold of {fail_threshold}%. "
        )
        return message


class PrimitiveObsessionMetric(Metric[PrimitiveObsessionResults]): ...
