from typing import TypeVar

from pymetrica.models import Report, ReportGenerator, Results

T = TypeVar("T", bound=Results)


class BasicHookReport(ReportGenerator):
    def short_report(self, audit: bool = False) -> Report:
        failed_metrics = [
            metric for metric in self.metrics if metric.exceeds_threshold(audit)
        ]
        if not failed_metrics:
            return Report(
                content="All metrics passed their thresholds. No issues found.",
            )
        report = ("-" * 40) + " SHORT REPORT " + ("-" * 40)
        for metric in failed_metrics:
            report += f"\nMetric: {metric.name} FAILED\n"
            results = metric.results_dict
            for key, value in results.items():
                report += f"{key}: {value}\n"
        report += self.fail_messages(audit)
        return Report(content=report, exit_status=self.exit_status)

    def long_report(self, audit: bool = False) -> Report:
        failed_metrics = [
            metric for metric in self.metrics if metric.exceeds_threshold(audit)
        ]
        if not failed_metrics:
            return Report(
                content="All metrics passed their thresholds. No issues found.",
            )
        report = ("-" * 40) + " LONG REPORT " + ("-" * 40) + "\n\n"
        for metric in failed_metrics:
            report += f"Metric: {metric.name} FAILED \n"
            report += f"Description: {metric.description}\n"
            report += f"Summary: {metric.summary}\n"
            report += "-" * 100
            report += "\n\n"
        report = report[0:-100]
        report += self.fail_messages(audit)
        return Report(content=report, exit_status=self.exit_status)
