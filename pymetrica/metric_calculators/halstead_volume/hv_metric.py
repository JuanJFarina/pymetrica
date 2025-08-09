from typing import Any

from pymetrica.models import Metric, Results


class HalsteadVolumeResults(Results):
    hv_number: float

    def get_dict(self) -> dict[str, Any]:
        return self.get_dict()

    def get_json(self) -> str:
        return self.get_json()

    def get_summary(self) -> str:
        return f"\nHalstead Volume: {self.hv_number}"


class HalsteadVolumeMetric(Metric[HalsteadVolumeResults]): ...
