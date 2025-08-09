from typing import Any

from pymetrica.models import Metric, Results


class AlocResults(Results):
    aloc_number: int
    aloc_percentage: float

    def get_dict(self) -> dict[str, Any]:
        return self.get_dict()

    def get_json(self) -> str:
        return self.get_json()

    def get_summary(self) -> str:
        return "Unimplemented summary"


class AlocMetric(Metric[AlocResults]): ...
