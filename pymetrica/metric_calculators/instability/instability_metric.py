import json

from pymetrica.models import Metric, Results


class InstabilityResults(Results):
    instability: dict[str, float]

    def get_dict(self) -> dict[str, float]:
        return self.get_dict()

    def get_json(self) -> str:
        return json.dumps(self.get_dict())

    def get_summary(self) -> str:
        summary = "\nInstability for:\n"
        for layer, instability in self.instability.items():
            summary += f"{layer}: {instability}\n"
        return summary


class InstabilityMetric(Metric[InstabilityResults]): ...
