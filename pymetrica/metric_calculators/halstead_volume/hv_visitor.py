# pylint: disable=invalid-name

import ast

# This has been based on Radon's implementation and updated to support
# modern python features.


class HalsteadVolumeVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.operators: list[str] = []
        self.operands: list[str] = []

    def visit_BinOp(self, node: ast.BinOp) -> None:
        # Binary operators (+, -, *, etc.)
        self.operators.append(type(node.op).__name__)
        self.generic_visit(node)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        # Unary operators (+x, -x, not x)
        self.operators.append(type(node.op).__name__)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        # Boolean operators (and, or)
        self.operators.append(type(node.op).__name__)
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        # Comparison operators (<, >, ==, etc.)
        for op in node.ops:
            self.operators.append(type(op).__name__)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        # Assignment
        self.operators.append("Assign")
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        # Augmented assignment (+=, -=, etc.)
        self.operators.append(f"AugAssign_{type(node.op).__name__}")
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.operators.append("if")
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.operators.append("for")
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.operators.append("while")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.operators.append("def")
        self.operands.append(node.name)  # function name is an operand
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.operators.append("class")
        self.operands.append(node.name)  # class name is an operand
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        # Variable name
        self.operands.append(node.id)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Object attribute
        self.operands.append(node.attr)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        # Literals
        self.operands.append(repr(node.value))
