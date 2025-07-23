def is_logical_line_of_code(line: str) -> bool:
    """Check whether a line is blank or a comment."""
    stripped = line.strip()
    return False if stripped.startswith("#") or not stripped else True
