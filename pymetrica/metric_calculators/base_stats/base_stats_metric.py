import json

from pymetrica.models import CodebaseStats, Metric, NonNegativeInt, Results


class BaseStatsResults(Results, CodebaseStats):
    @property
    def dict_(self) -> dict[str, object]:
        return {
            "root_folder_path": self.root_folder_path,
            "root_folder_name": self.root_folder_name,
            "folders_number": self.folders_number,
            "files_number": self.files_number,
            "lloc_number": self.lloc_number,
            "lloc_file_ratio": self.lloc_file_ratio,
            "comments_number": self.comments_number,
            "comment_lloc_ratio": self.comment_lloc_ratio,
            "classes_number": self.classes_number,
            "functions_number": self.functions_number,
        }

    @property
    def json_(self) -> str:
        return json.dumps(self.dict_)


class BaseStatsMetric(Metric[BaseStatsResults]):
    exit_code: NonNegativeInt = 0

    @property
    def summary(self) -> str:
        summary = "\nBase Stats:\n"
        for name, value in self.results_dict.items():
            summary += f"  {name}: {value}\n"
        return summary

    @property
    def fail_message(self) -> str:
        return ""

    def exceeds_threshold(self, audit: bool = False) -> bool:
        return False
