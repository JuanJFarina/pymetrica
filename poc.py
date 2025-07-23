import os
import ast
import argparse
from typing import Dict, Any, List, Set


def is_blank_or_comment(line: str) -> bool:
    """Check whether a line is blank or a comment."""
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def gather_loc_and_classes(dir_path: str) -> Dict[str, Any]:
    """
    First pass:
      - Count total logical lines ('lloc').
      - Identify all class definitions and compute their LOC spans.
      - Compute abstract LOC ('aloc').
      - Record non-abstract class LOC in 'classes'.
    """
    total_lloc = 0
    total_aloc = 0
    classes: Dict[str, int] = {}

    for root, _, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            source = "".join(lines)
            tree = ast.parse(source)

            # Count logical lines in file
            file_lloc = sum(1 for l in lines if not is_blank_or_comment(l))
            total_lloc += file_lloc

            # Collect abstract lines
            file_abs: Set[int] = set()
            for node in ast.walk(tree):
                # Imports
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    file_abs.add(node.lineno)
                # __all__ assignments
                if isinstance(node, ast.Assign):
                    for tgt in node.targets:
                        if isinstance(tgt, ast.Name) and tgt.id == "__all__":
                            file_abs.add(node.lineno)
                # Function defs and decorators
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    file_abs.add(node.lineno)
                    for dec in node.decorator_list:
                        file_abs.add(dec.lineno)
                # Class defs and decorators
                if isinstance(node, ast.ClassDef):
                    file_abs.add(node.lineno)
                    for dec in node.decorator_list:
                        file_abs.add(dec.lineno)
                # Any call
                if isinstance(node, ast.Call):
                    file_abs.add(node.lineno)

            total_aloc += len(file_abs)

            # Measure classes
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    start, end = node.lineno, getattr(node, "end_lineno", node.lineno)
                    # Check inheritance
                    bases: List[str] = []
                    for b in node.bases:
                        if isinstance(b, ast.Name):
                            bases.append(b.id)
                        else:
                            try:
                                bases.append(ast.unparse(b))
                            except:
                                pass
                    # Treat ABC, ABCMeta, Protocol, and Enum as abstract
                    is_abstract_base = any(
                        base in ("ABC", "ABCMeta", "Protocol", "Enum") for base in bases
                    )
                    # Count LOC
                    loc = sum(
                        1
                        for i in range(start - 1, end)
                        if i < len(lines) and not is_blank_or_comment(lines[i])
                    )
                    if not is_abstract_base:
                        classes[node.name] = loc

    return {"lloc": total_lloc, "aloc": total_aloc, "classes": classes}


def count_uninstantiated_loc(dir_path: str, classes: Dict[str, int]) -> int:
    """
    Second pass:
      - Detect instantiation by:
        * Direct calls: ClassName()
        * Class method calls: ClassName.method(...)
      - Any class appearing as ast.Name in call.func or ast.Attribute.value qualifies.
    Returns sum of LOC for classes never instantiated.
    """
    instantiated: Set[str] = set()
    for root, _, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func = node.func
                    # Direct instantiation
                    if isinstance(func, ast.Name) and func.id in classes:
                        instantiated.add(func.id)
                    # Method call on class (ClassName.method(...))
                    elif isinstance(func, ast.Attribute):
                        val = func.value
                        if isinstance(val, ast.Name) and val.id in classes:
                            instantiated.add(val.id)
    print(f"Classes never instantiated with their respective LOC: {[{cls: loc} for cls, loc in classes.items() if cls not in instantiated]}")
    return sum(loc for cls, loc in classes.items() if cls not in instantiated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze Python code for LOC, abstraction, and uninstantiated class LOC."
    )
    parser.add_argument("dir_path", type=str, help="Path to analyze")
    args = parser.parse_args()

    summary = gather_loc_and_classes(args.dir_path)
    uninst = count_uninstantiated_loc(args.dir_path, summary["classes"])
    print("Total logical LOC:", summary["lloc"])
    print("Total abstract LOC:", summary["aloc"] + uninst)
    print(
        "Abstraction percentage:",
        f"{(summary['aloc'] + uninst) / summary['lloc'] * 100:.2f}%",
    )
