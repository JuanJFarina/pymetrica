from typing import Any

from pymetrica.models import Metric, Results


class CCResults(Results):
    cc_number: int
    cc_lloc_ratio: float

    def get_dict(self) -> dict[str, Any]:
        return self.get_dict()

    def get_json(self) -> str:
        return self.get_json()

    def get_summary(self) -> str:
        return self.get_summary()


class CCMetric(Metric[CCResults]): ...
