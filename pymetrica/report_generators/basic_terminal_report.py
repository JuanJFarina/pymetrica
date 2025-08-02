from __future__ import annotations

from pymetrica.models import Metric
from pymetrica.models import ReportGenerator


class BasicTerminalReport(ReportGenerator):
    def generate_report(self, metrics: list[Metric]) -> None:
        for metric in metrics:
            print(f'Metric: {metric.name}')
            print(f'Description: {metric.description}')
            print(f'Value: {metric.value}')
            print('-' * 20)
