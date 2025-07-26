from pymetrica.models import ReportGenerator
from pymetrica.models import Metric


class BasicTerminalReport(ReportGenerator):
    def generate_report(self, metrics: list[Metric]) -> None:
        for metric in metrics:
            print(f"Metric: {metric.name}")
            print(f"Description: {metric.description}")
            print(f"Value: {metric.value}")
            print("-" * 20)
