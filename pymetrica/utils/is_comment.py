def is_comment_line(line: str) -> bool:
    stripped = line.strip()
    if stripped.startswith("#"):
        return True
    return False
