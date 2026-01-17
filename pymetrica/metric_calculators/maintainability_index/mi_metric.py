import json

from pymetrica.models import Metric, Results


class MaintainabilityIndexResults(Results):
    maintainability_index: float
    normalized_mi: float

    def get_dict(self) -> dict[str, int]:
        return self.get_dict()

    def get_json(self) -> str:
        return json.dumps(self.get_dict())

    def get_summary(self) -> str:
        return (
            f"\nMaintainability Index: {self.maintainability_index:.2f}"
            f"\nNormalized MI: {self.normalized_mi:.2f}"
        )


class MaintainabilityIndexMetric(Metric[MaintainabilityIndexResults]): ...
