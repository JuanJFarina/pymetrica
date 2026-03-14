from pydantic import BaseModel

from .code import Code


class Codebase(BaseModel):
    root_folder_path: str
    root_folder_name: str
    folders_number: int
    files_number: int
    lloc_number: int
    lloc_file_ratio: str
    comments_number: int
    comment_lloc_ratio: str
    classes_number: int
    functions_number: int
    layers: dict[str, list[Code]]
    root_files: list[Code]

    @property
    def files(self) -> list[Code]:
        return self.root_files + [
            file for layer in self.layers.values() for file in layer
        ]
