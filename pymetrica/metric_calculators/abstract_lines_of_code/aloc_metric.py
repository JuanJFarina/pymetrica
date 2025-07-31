from typing import Any
from pymetrica.models import Metric, Results


class AlocResults(Results):
    aloc: int
    aloc_percentage: float

    def get_dict(self) -> dict[str, Any]:
        return super().get_dict()

    def get_json(self) -> str:
        return super().get_json()

    def get_summary(self) -> str:
        return super().get_summary()


class AlocMetric(Metric[AlocResults]): ...
