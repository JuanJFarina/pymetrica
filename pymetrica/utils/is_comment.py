from __future__ import annotations


def is_comment_line(line: str) -> bool:
    stripped = line.strip()
    return True if stripped.startswith('#') else False
