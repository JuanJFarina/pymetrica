import ast
import os
from pathlib import Path

from pymetrica.models import Code, Codebase
from pymetrica.utils import is_comment_line, is_logical_line_of_code

# TODO ignore folders inside .gitignore


def parse_codebase(dir_path: str) -> Codebase:
    base = Path(dir_path).absolute()
    total_lloc = 0
    total_comments = 0
    total_classes_definitions = 0
    total_functions_definitions = 0
    total_files: list[Code] = []

    for path in base.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines(keepends=True)
        tree = ast.parse(source)
        total_classes_definitions += sum(
            isinstance(n, ast.ClassDef) for n in ast.walk(tree)
        )
        total_functions_definitions += sum(
            isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            for n in ast.walk(tree)
        )

        total_lloc += (
            file_lloc := sum(1 for line in lines if is_logical_line_of_code(line))
        )
        total_comments += (
            file_comments := sum(1 for line in lines if is_comment_line(line))
        )
        total_files.append(
            Code(
                filepath=str(path),
                filename=path.name,
                lloc_number=file_lloc,
                comments_number=file_comments,
                code_lines=lines,
                code=source,
            ),
        )

    return Codebase(
        root_folder_path=str(Path(dir_path).absolute()),
        root_folder_name=os.path.basename(dir_path),
        folders_number=sum(1 for p in base.rglob("*") if p.is_dir()),
        files_number=len(total_files),
        lloc_number=total_lloc,
        lloc_file_ratio=(
            f"{total_lloc / (len(total_files) or 1):.1f}:{1 if total_files else 0}"
        ),
        comments_number=total_comments,
        comment_lloc_ratio=(
            f"{1 if total_comments else 0}:{total_lloc / (total_comments or 1):.1f}"
        ),
        classes_number=total_classes_definitions,
        functions_number=total_functions_definitions,
        files=total_files,
    )
