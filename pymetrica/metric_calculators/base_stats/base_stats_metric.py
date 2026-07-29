import json

from pymetrica.models import Metric, Results

StatisticText = str
StatisticCount = int
AuditEnabled = bool
BaseStatsMapping = dict[StatisticText, StatisticCount | StatisticText]


class BaseStatsResults(Results):
    root_folder_path: StatisticText
    root_folder_name: StatisticText
    folders_number: StatisticCount
    files_number: StatisticCount
    lloc_number: StatisticCount
    lloc_file_ratio: StatisticText
    comments_number: StatisticCount
    comment_line_ratio: StatisticText
    classes_number: StatisticCount
    functions_number: StatisticCount

    @property
    def dict_(self) -> BaseStatsMapping:
        return {
            "root_folder_path": self.root_folder_path,
            "root_folder_name": self.root_folder_name,
            "folders_number": self.folders_number,
            "files_number": self.files_number,
            "lloc_number": self.lloc_number,
            "lloc_file_ratio": self.lloc_file_ratio,
            "comments_number": self.comments_number,
            "comment_line_ratio": self.comment_line_ratio,
            "classes_number": self.classes_number,
            "functions_number": self.functions_number,
        }

    @property
    def json_(self) -> StatisticText:
        return json.dumps(self.dict_)


class BaseStatsMetric(Metric[BaseStatsResults]):
    exit_code: StatisticCount = 0

    @property
    def summary(self) -> StatisticText:
        return "\n".join(
            f"{name}: {value}" for name, value in self.results_dict.items()
        )

    @property
    def fail_message(self) -> StatisticText:
        return ""

    def exceeds_threshold(self, audit: AuditEnabled = False) -> AuditEnabled:
        return False
