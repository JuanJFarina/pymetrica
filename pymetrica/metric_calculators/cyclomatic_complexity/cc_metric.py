from __future__ import annotations

from typing import Any

from pymetrica.models import Metric
from pymetrica.models import Results


class CCResults(Results):
    cc_number: int
    cc_lloc_ratio: float

    def get_dict(self) -> dict[str, Any]:
        return super().get_dict()

    def get_json(self) -> str:
        return super().get_json()

    def get_summary(self) -> str:
        return super().get_summary()


class CCMetric(Metric[CCResults]):
    ...
