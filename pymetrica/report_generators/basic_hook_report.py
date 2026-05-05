from collections.abc import Sequence
from typing import TypeVar

from pymetrica.models import Metric, ReportGenerator, Results

T = TypeVar("T", bound=Results)


class BasicHookReport(ReportGenerator):
    def generate_report(self, metrics: Sequence[Metric[T]]) -> str:
        failed_metrics = [
            metric for metric in metrics if metric.results.exceeds_threshold
        ]
        if not failed_metrics:
            return "All metrics passed their thresholds. No issues found."
        report = ("-" * 40) + " LONG REPORT " + ("-" * 40) + "\n\n"
        for metric in failed_metrics:
            report += f"Metric: {metric.name} FAILED \n"
            report += f"Description: {metric.description}\n"
            report += f"Summary: {metric.results.summary}\n"
            report += "-" * 100
            report += "\n\n"
        return report[:-103]

    def generate_short_report(self, metrics: Sequence[Metric[T]]) -> str:
        failed_metrics = [
            metric for metric in metrics if metric.results.exceeds_threshold
        ]
        if not failed_metrics:
            return "All metrics passed their thresholds. No issues found."
        report = ("-" * 40) + " SHORT REPORT " + ("-" * 40)
        for metric in failed_metrics:
            report += f"\nMetric: {metric.name} FAILED\n"
            results = metric.results.dict_
            for key, value in results.items():
                report += f"{key}: {value}\n"
            report += "-" * 100
        return report[:-100]
