import json

from pymetrica.models import Metric, Results
from pymetrica.utils import log


class InstabilityResults(Results):
    instability: dict[str, float]

    @property
    def dict_(self) -> dict[str, float]:
        return self.instability

    @property
    def json_(self) -> str:
        return json.dumps(self.dict_)

    @property
    def summary(self) -> str:
        summary = "\nInstability for:\n"
        for layer, instability in self.instability.items():
            summary += f"  {layer}: {instability}\n"
        return summary

    @property
    def fail_message(self) -> str:
        raise NotImplementedError("Instability metric does not have a fail threshold.")

    @property
    def exceeds_threshold(self) -> bool:
        log.warning("Instability metric does not have a fail threshold.")
        return False


class InstabilityMetric(Metric[InstabilityResults]): ...
