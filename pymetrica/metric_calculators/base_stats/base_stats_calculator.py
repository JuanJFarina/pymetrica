from pymetrica.models import Codebase, MetricCalculator

from .base_stats_metric import BaseStatsMetric, BaseStatsResults


class BaseStatsCalculator(MetricCalculator[BaseStatsResults]):
    def calculate_metric(self, codebase: Codebase) -> BaseStatsMetric:
        return BaseStatsMetric(
            name="Base Stats",
            description=(
                "Base Stats summarizes the analyzed codebase structure and "
                "parser-level source counts."
            ),
            results=BaseStatsResults(
                root_folder_path=codebase.root_folder_path,
                root_folder_name=codebase.root_folder_name,
                folders_number=codebase.folders_number,
                files_number=codebase.files_number,
                lloc_number=codebase.lloc_number,
                lloc_file_ratio=codebase.lloc_file_ratio,
                comments_number=codebase.comments_number,
                comment_line_ratio=codebase.comment_lloc_ratio,
                classes_number=codebase.classes_number,
                functions_number=codebase.functions_number,
            ),
        )
