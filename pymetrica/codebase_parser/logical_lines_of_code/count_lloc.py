import os

from pymetrica.utils.is_lloc import is_logical_line_of_code


def count_logical_lines_of_code(root: str, file_name: str) -> int:
    path = os.path.join(root, file_name)
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    return sum(1 for line in lines if is_logical_line_of_code(line))
