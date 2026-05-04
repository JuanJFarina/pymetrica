from collections.abc import Sequence
from typing import TypeVar

from pymetrica.models import Metric, ReportGenerator, Results

T = TypeVar("T", bound=Results)


class BasicHookReport(ReportGenerator):
    def generate_report(self, metrics: Sequence[Metric[T]]) -> str:
        failed_metrics = [metric for metric in metrics if metric.failed]
        if not failed_metrics:
            return "All metrics passed their thresholds. No issues found."
        report = ""
        for metric in failed_metrics:
            report += f"Metric: {metric.name}\n FAILED"
            report += f"Description: {metric.description}\n"
            report += f"Summary: {metric.results.summary}\n"
            report += "-" * 100
            report += "\n"
        return report

    def generate_short_report(self, metrics: Sequence[Metric[T]]) -> str:
        failed_metrics = [metric for metric in metrics if metric.failed]
        if not failed_metrics:
            return "All metrics passed their thresholds. No issues found."
        report = "-" * 100
        report += "\nShort Report\n"
        report += "-" * 100
        for metric in failed_metrics:
            report += f"\nMetric: {metric.name} FAILED\n"
            results = metric.results.dict_
            for key, value in results.items():
                report += f"{key}: {value}\n"
            report += "-" * 100
        return report
