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
    files: list[Code]
