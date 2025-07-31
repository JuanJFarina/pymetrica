PARENS = ["(", ")", "{", "}", "[", "]", ","]


def is_logical_line_of_code(line: str) -> bool:
    """Check whether a line is blank or a comment."""
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False
    for char in stripped:
        if char not in PARENS:
            break
    else:
        return False
    return True
