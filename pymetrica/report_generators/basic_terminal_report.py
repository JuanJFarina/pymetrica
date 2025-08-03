from typing import TypeVar

from pymetrica.models import Metric, ReportGenerator, Results


T = TypeVar("T", bound=Results)


class BasicTerminalReport(ReportGenerator):
    def generate_report(self, metrics: list[Metric[T]]) -> None:
        for metric in metrics:
            print(f"Metric: {metric.name}")
            print(f"Description: {metric.description}")
            print(f"Summary: {metric.results.get_summary()}")
            print("-" * 20)
