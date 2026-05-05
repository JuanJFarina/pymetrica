import ast

from pydantic import BaseModel

from pymetrica.utils import log

PRIMITIVES = {"Any", "bool", "float", "int", "str"}
TARGETS = {"dict", "list", "tuple", "set"}


def get_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr  # ignore module (typing.Any → Any)
    raise ValueError(f"Unsupported annotation node: {ast.dump(node, indent=2)}")


class TypeAnnotation(BaseModel):
    type: str
    args: list["TypeAnnotation"] | None = None
    is_primitive: bool = False
    is_targeted: bool = False

    def __str__(self) -> str:
        if self.type == "Union" and self.args:
            return " | ".join(str(arg) for arg in self.args)  # pylint: disable=not-an-iterable
        str_repr = self.type
        if self.args:
            str_repr += "[" + ", ".join(str(arg) for arg in self.args) + "]"
        return str_repr

    def __repr__(self) -> str:
        return str(self)


def parse_type(
    node: ast.AST,
) -> TypeAnnotation:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        left = parse_type(node.left)
        right = parse_type(node.right)
        return TypeAnnotation(type="Union", args=[left, right])
    if isinstance(node, (ast.Name, ast.Attribute)) and (
        get_name(node) in PRIMITIVES or get_name(node) in TARGETS
    ):
        return TypeAnnotation(type=get_name(node))

    if isinstance(node, ast.Subscript):
        base = get_name(node.value)

        slice_node = node.slice
        if isinstance(slice_node, ast.Tuple):
            args = [parse_type(elt) for elt in slice_node.elts]
        else:
            args = [parse_type(slice_node)]

        return TypeAnnotation(type=base, args=args)

    raise ValueError(f"Unsupported annotation node: {ast.dump(node, indent=2)}")


class Analysis(BaseModel):
    is_valid: bool
    is_primitive: bool
    is_targeted: bool


def analyze_type(parsed_type: TypeAnnotation) -> Analysis:
    if parsed_type.type == "Union" and all(
        analyze_type(arg) for arg in parsed_type.args or []
    ):
        parsed_type.is_primitive = all(
            arg.is_primitive for arg in parsed_type.args or []
        )
        parsed_type.is_targeted = any(arg.is_targeted for arg in parsed_type.args or [])
        return Analysis(
            is_valid=True,
            is_primitive=parsed_type.is_primitive,
            is_targeted=parsed_type.is_targeted,
        )
    if parsed_type.type == "Any":
        parsed_type.is_primitive = True
        parsed_type.is_targeted = True
        return Analysis(is_valid=True, is_primitive=True, is_targeted=True)
    if parsed_type.type in PRIMITIVES:
        parsed_type.is_primitive = True
        return Analysis(is_valid=True, is_primitive=True, is_targeted=False)
    if parsed_type.type in TARGETS and (
        not parsed_type.args or all(analyze_type(arg) for arg in parsed_type.args)
    ):
        parsed_type.is_primitive = True
        parsed_type.is_targeted = True
        return Analysis(is_valid=True, is_primitive=True, is_targeted=True)
    return Analysis(is_valid=False, is_primitive=False, is_targeted=False)


class POVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.targeted_primitives = list[TypeAnnotation]()
        self.all_primitives = list[TypeAnnotation]()

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:  # pylint: disable=invalid-name
        self._handle(node.annotation)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        if node.annotation:
            self._handle(node.annotation)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # pylint: disable=invalid-name
        if node.returns:
            self._handle(node.returns)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # pylint: disable=invalid-name
        if node.returns:
            self._handle(node.returns)
        self.generic_visit(node)

    def _handle(self, annotation: ast.AST) -> None:
        try:
            parsed = parse_type(annotation)
        except ValueError as e:
            log.debug(f"Error parsing annotation: {e}")
            return
        analyze_type(parsed)
        if parsed.is_primitive:
            self.all_primitives.append(parsed)
        if parsed.is_targeted:
            self.targeted_primitives.append(parsed)
