import ast

from pymetrica.models import Code


def called_classes(files: list[Code], classes: dict[str, int]) -> set[str]:
    """
    Second pass:
      - Detect instantiation by:
        * Direct calls: ClassName()
        * Class method calls: ClassName.method(...)
      - Any class appearing as ast.Name in call.func or ast.Attribute.value qualifies.
    Returns sum of LOC for classes never instantiated.
    """
    called: set[str] = set()
    for file in files:
        tree = ast.parse(file.code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                # Direct instantiation
                if isinstance(func, ast.Name) and func.id in classes:
                    called.add(func.id)
                # Method call on class (ClassName.method(...))
                elif isinstance(func, ast.Attribute):
                    val = func.value
                    if isinstance(val, ast.Name) and val.id in classes:
                        called.add(val.id)
                for arg in node.args:
                    if isinstance(arg, ast.Name) and arg.id in classes:
                        called.add(arg.id)
    return called
