from __future__ import annotations

import ast


# This has been based on Radon's implementation and updated to support
# modern python features.


class CCVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.complexity = 0  # no CC will be counted per file, only per application

    # Selection statements

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_Elif(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        self.complexity += 1 + len(node.cases)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        if isinstance(node.op, (ast.And, ast.Or)):
            self.complexity += len(node.values) - 1
        self.generic_visit(node)

    # Iteration statements

    def visit_For(self, node: ast.For) -> None:
        self.complexity += 1 + bool(node.orelse)
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.complexity += 1 + bool(node.orelse)
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.complexity += 1 + bool(node.orelse)
        self.generic_visit(node)

    # Contexts and exceptions branching

    def visit_Try(self, node: ast.Try) -> None:
        self.complexity += len(node.handlers) + bool(node.orelse)
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        self.complexity += len(node.items)
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.complexity += len(node.items)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self.complexity += 1
        self.generic_visit(node)

    # Comprehensions

    def _visit_comprehensions(self, generators: list[ast.comprehension]) -> None:
        self.complexity += len(generators)
        for gen in generators:
            if gen.ifs:
                self.complexity += len(gen.ifs)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehensions(node.generators)
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehensions(node.generators)
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehensions(node.generators)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehensions(node.generators)
        self.generic_visit(node)
