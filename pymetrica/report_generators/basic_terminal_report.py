from typing import TypeVar

from pymetrica.models import Report, ReportGenerator, Results

T = TypeVar("T", bound=Results)


class BasicTerminalReport(ReportGenerator):
    def short_report(self, audit: bool = False) -> Report:
        content = "-" * 100
        content += "\nShort Report\n"
        content += "-" * 100
        for metric in self.metrics:
            content += f"\nMetric: {metric.name}\n"
            results = metric.results_dict
            for key, value in results.items():
                content += f"{key}: {value}\n"
            content += "-" * 100
        content = content[:-100] + self.fail_messages(audit) if audit else content
        return Report(content=content)

    def long_report(self, audit: bool = False) -> Report:
        content = ""
        for metric in self.metrics:
            content += f"Metric: {metric.name}\n"
            content += f"Description: {metric.description}\n"
            content += f"Summary: {metric.summary}\n"
            content += "-" * 100
            content += "\n"
        content = content[:-100] + self.fail_messages(audit) if audit else content
        return Report(content=content)
