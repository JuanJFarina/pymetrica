import json

from pymetrica.models import Results


class MIResults(Results):
    maintainability_index: float

    def get_dict(self) -> dict[str, float]:
        return {
            "maintainability_index": self.maintainability_index,
        }

    def get_json(self) -> str:
        return json.dumps(self.get_dict())

    def get_summary(self) -> str:
        return f"Maintainability Index: {self.maintainability_index:.2f}"
