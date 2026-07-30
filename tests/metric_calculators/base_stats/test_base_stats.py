import json

from pymetrica.metric_calculators import BaseStatsCalculator
from pymetrica.models import Codebase


def test_calculate_base_stats(codebase: Codebase) -> None:
    metric = BaseStatsCalculator().calculate_metric(codebase)

    assert metric.results.dict_ == {
        "root_folder_path": codebase.root_folder_path,
        "root_folder_name": codebase.root_folder_name,
        "folders_number": codebase.folders_number,
        "files_number": codebase.files_number,
        "lloc_number": codebase.lloc_number,
        "lloc_file_ratio": codebase.lloc_file_ratio,
        "comments_number": codebase.comments_number,
        "comment_line_ratio": codebase.comment_lloc_ratio,
        "classes_number": codebase.classes_number,
        "functions_number": codebase.functions_number,
    }
    assert json.loads(metric.results.json_) == metric.results.dict_
    assert metric.exit_code == 0
    assert not metric.exceeds_threshold()
