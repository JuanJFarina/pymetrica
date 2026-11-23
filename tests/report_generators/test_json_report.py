import json

from pymetrica.metric_calculators import BaseStatsCalculator
from pymetrica.models import Codebase
from pymetrica.report_generators import REPORTS_MAPPING, JsonReport


def test_short_report_is_valid_json(codebase: Codebase) -> None:
    metric = BaseStatsCalculator().calculate_metric(codebase)

    report = JsonReport([metric]).short_report()
    content = json.loads(report.content)

    assert content["metrics"] == [
        {
            "name": metric.name,
            "results": metric.results.dict_,
        },
    ]
    assert content["threshold_exit_status"] == 0
    assert content["failures"] == ""
    assert report.exit_status == 0


def test_long_report_includes_metric_details(codebase: Codebase) -> None:
    metric = BaseStatsCalculator().calculate_metric(codebase)

    report = JsonReport([metric]).long_report()
    content = json.loads(report.content)

    assert content["metrics"][0] == {
        "name": metric.name,
        "description": metric.description,
        "summary": metric.summary,
        "results": metric.results.dict_,
    }


def test_json_report_is_registered() -> None:
    assert REPORTS_MAPPING["JSON"] is JsonReport
