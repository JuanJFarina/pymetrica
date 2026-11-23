import json
from collections.abc import Mapping, Sequence

from pymetrica.models import Report, ReportGenerator


class JsonReport(ReportGenerator):
    def short_report(self, audit: bool = False) -> Report:
        metrics = [
            {
                "name": metric.name,
                "results": metric.results_dict,
            }
            for metric in self.metrics
        ]
        return self._report(metrics, audit)

    def long_report(self, audit: bool = False) -> Report:
        metrics = [
            {
                "name": metric.name,
                "description": metric.description,
                "summary": metric.summary,
                "results": metric.results_dict,
            }
            for metric in self.metrics
        ]
        return self._report(metrics, audit)

    def _report(
        self,
        metrics: Sequence[Mapping[str, object]],
        audit: bool,
    ) -> Report:
        return Report(
            content=json.dumps(
                {
                    "metrics": metrics,
                    "threshold_exit_status": self.exit_status,
                    "failures": self.fail_messages(audit),
                },
                indent=2,
            ),
        )
