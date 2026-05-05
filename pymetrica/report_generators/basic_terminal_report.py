from typing import TypeVar

from pymetrica.models import Report, ReportGenerator, Results

T = TypeVar("T", bound=Results)


class BasicTerminalReport(ReportGenerator):
    @property
    def short_report(self) -> Report:
        content = "-" * 100
        content += "\nShort Report\n"
        content += "-" * 100
        for metric in self.metrics:
            content += f"\nMetric: {metric.name}\n"
            results = metric.results.dict_
            for key, value in results.items():
                content += f"{key}: {value}\n"
            content += "-" * 100
        return Report(content=content)

    @property
    def long_report(self) -> Report:
        content = ""
        for metric in self.metrics:
            content += f"Metric: {metric.name}\n"
            content += f"Description: {metric.description}\n"
            content += f"Summary: {metric.results.summary}\n"
            content += "-" * 100
            content += "\n"
        return Report(content=content)
