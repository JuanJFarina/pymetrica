import ast
import os

from pymetrica.models import Codebase, Code
from pymetrica.utils import is_comment_line, is_logical_line_of_code
from pathlib import Path


def parse_codebase(dir_path: str) -> Codebase:
    total_lloc = 0
    total_comments = 0
    total_classes_definitions = 0
    total_functions_definitions = 0
    total_files: list[Code] = []

    for root, _, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            source = "".join(lines)
            tree = ast.parse(source)
            classes_definitions = 0
            functions_definitions = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes_definitions += 1
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions_definitions += 1

            file_lloc = sum(1 for l in lines if is_logical_line_of_code(l))
            total_lloc += file_lloc
            file_comments = sum(1 for l in lines if is_comment_line(l))
            total_comments += file_comments
            total_classes_definitions += classes_definitions
            total_functions_definitions += functions_definitions
            total_files.append(
                Code(
                    filepath=os.path.join(root, fname),
                    filename=fname,
                    lloc_number=file_lloc,
                    comments_number=file_comments,
                    code_lines=lines,
                    code=source,
                )
            )

    comment_line_ratio = (
        f"{1 if total_comments else 0}:{total_lloc / (total_comments or 1):.1f}"
    )

    return Codebase(
        root_folder_path=str(Path(dir_path).absolute()),
        root_folder_name=os.path.basename(dir_path),
        folders_number=len(
            [
                d
                for d in os.listdir(dir_path)
                if os.path.isdir(os.path.join(dir_path, d))
            ]
        ),
        files_number=len(total_files),
        lloc_number=total_lloc,
        comments_number=total_comments,
        comment_line_ratio=comment_line_ratio,
        classes_number=total_classes_definitions,
        functions_number=total_functions_definitions,
        files=total_files,
    )
