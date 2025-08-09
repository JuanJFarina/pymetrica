from typing import TypeVar

from pymetrica.models import Metric, ReportGenerator, Results


T = TypeVar("T", bound=Results)


class BasicTerminalReport(ReportGenerator):
    def generate_report(self, metrics: list[Metric[T]]) -> str:
        report = ""
        for metric in metrics:
            report += f"Metric: {metric.name}\n"
            report += f"Description: {metric.description}\n"
            report += f"Summary: {metric.results.get_summary()}\n"
            report += "-" * 100
            report += "\n"
        return report
