import os
import ast


def count_uninstantiated_loc(dir_path: str, classes: dict[str, int]) -> int:
    """
    Second pass:
      - Detect instantiation by:
        * Direct calls: ClassName()
        * Class method calls: ClassName.method(...)
      - Any class appearing as ast.Name in call.func or ast.Attribute.value qualifies.
    Returns sum of LOC for classes never instantiated.
    """
    instantiated: set[str] = set()
    for root, _, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                print(f"Node: {node}\nFrom: {fname}")
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
    print(
        f"Classes never instantiated with their respective LOC: {[{cls: loc} for cls, loc in classes.items() if cls not in instantiated]}"
    )
    return sum(loc for cls, loc in classes.items() if cls not in instantiated)
