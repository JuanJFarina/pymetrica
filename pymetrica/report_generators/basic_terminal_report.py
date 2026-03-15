from collections.abc import Sequence
from typing import TypeVar

from pymetrica.models import Metric, ReportGenerator, Results

T = TypeVar("T", bound=Results)


class BasicTerminalReport(ReportGenerator):
    def generate_report(self, metrics: Sequence[Metric[T]]) -> str:
        report = ""
        for metric in metrics:
            report += f"Metric: {metric.name}\n"
            report += f"Description: {metric.description}\n"
            report += f"Summary: {metric.results.get_summary()}\n"
            report += "-" * 100
            report += "\n"
        return report

    def generate_short_report(self, metrics: Sequence[Metric[T]]) -> str:
        report = "-" * 100
        report += "\nShort Report\n"
        report += "-" * 100
        for metric in metrics:
            report += f"\nMetric: {metric.name}\n"
            results = metric.results.get_dict()
            for key, value in results.items():
                report += f"{key}: {value}\n"
            report += "-" * 100
        return report
