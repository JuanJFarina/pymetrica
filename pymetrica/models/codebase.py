from pydantic import BaseModel
from .code import Code


class Codebase(BaseModel):
    root_folder_path: str
    root_folder_name: str
    folders_number: int
    files_number: int
    lloc_number: int
    comments_number: int
    comment_line_ratio: str
    classes_number: int
    functions_number: int
    files: list[Code]
