from pydantic import BaseModel

from .code import Code
from .value_objects import NonNegativeInt, StrPath, StrRatio


class CodebaseStats(BaseModel):
    root_folder_path: StrPath
    root_folder_name: str
    folders_number: NonNegativeInt
    files_number: NonNegativeInt
    lloc_number: NonNegativeInt
    lloc_file_ratio: StrRatio
    comments_number: NonNegativeInt
    comment_lloc_ratio: StrRatio
    classes_number: NonNegativeInt
    functions_number: NonNegativeInt


class Codebase(CodebaseStats):
    layers: dict[StrPath, list[Code]]
    root_files: list[Code]

    @property
    def files(self) -> list[Code]:
        return self.root_files + [
            file for layer in self.layers.values() for file in layer
        ]
