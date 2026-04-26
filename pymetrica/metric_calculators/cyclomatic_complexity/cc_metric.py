from typing import Any

from pydantic import BaseModel

from pymetrica.models import Metric, Results


class LayerCC(BaseModel):
    name: str
    cc_number: int
    lloc_per_cc: float


class CCResults(Results):
    cc_number: int
    lloc_per_cc: float
    cc_result_per_layer: list[LayerCC]

    def get_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude={"cc_result_per_layer"})

    def get_json(self) -> str:
        return self.get_json()

    def get_summary(self) -> str:
        summary = (
            f"\nTotal CC: {self.cc_number} ({self.lloc_per_cc:0.2f} LLOC per CC)\n"
        )
        for layer in self.cc_result_per_layer:
            summary += (
                f"  Layer {layer.name} CC: "
                f"{layer.cc_number} ({layer.lloc_per_cc:0.2f} LLOC per CC)\n"
            )
        return summary

    def get_fail_message(self, fail_threshold: int) -> str:
        message = (
            f"LLOC per CC {self.lloc_per_cc:.2f} is below "
            f"the fail threshold of {fail_threshold}. "
            "Reduce the number of logic branches and decision points by "
            "simplifying logic, using strict typing, and use multiple "
            "lines of code to simplify complex expressions."
        )
        return message


class CCMetric(Metric[CCResults]): ...
