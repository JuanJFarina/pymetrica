from pydantic import BaseModel

from .code import Code
from .value_objects import PositiveInt, StrPath, StrRatio


class CodebaseStats(BaseModel):
    root_folder_path: StrPath
    root_folder_name: str
    folders_number: PositiveInt
    files_number: PositiveInt
    lloc_number: PositiveInt
    lloc_file_ratio: StrRatio
    comments_number: PositiveInt
    comment_lloc_ratio: StrRatio
    classes_number: PositiveInt
    functions_number: PositiveInt


class Codebase(CodebaseStats):
    layers: dict[StrPath, list[Code]]
    root_files: list[Code]

    @property
    def files(self) -> list[Code]:
        return self.root_files + [
            file for layer in self.layers.values() for file in layer
        ]

    @property
    def non_init_files(self) -> list[Code]:
        return [
            file for file in self.files if not file.filepath.endswith("__init__.py")
        ]
