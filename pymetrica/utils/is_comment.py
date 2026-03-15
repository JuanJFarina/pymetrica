def is_comment_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped.startswith("#"))
