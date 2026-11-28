import ast
from pathlib import Path

from pymetrica.utils import log

from .module_paths import filepath_to_module_name

ImportReference = tuple[str | None, int, str | None]


def import_path_to_file_path(import_path: Path) -> Path | None:
    log.debug(f"import_path_to_file_path.{import_path = }")
    package = import_path / "__init__.py"
    if package.is_file():
        return package
    module = import_path.with_suffix(".py")
    if module.is_file():
        return module
    return None


def get_module_path(
    root: Path,
    current_module: Path,
    module: str | None,
    level: int,
) -> Path | None:
    log.debug(f"get_module_path.{current_module = }")
    log.debug(f"get_module_path.{module = }")
    module_parts = module.split(".") if module else []
    if level:
        base = current_module.parent
        for _ in range(level - 1):
            base = base.parent
    else:
        base = root
        if (
            (root / "__init__.py").is_file()
            and module_parts
            and module_parts[0] == root.name
        ):
            module_parts = module_parts[1:]

    resolved = import_path_to_file_path(base.joinpath(*module_parts))
    if resolved is None:
        return None
    try:
        resolved.relative_to(root)
    except ValueError:
        return None
    return resolved


class TraceSymbolVisitor(ast.NodeVisitor):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.import_reference: ImportReference | None = None

    def visit_Module(self, node: ast.Module) -> None:  # pylint: disable=invalid-name
        for statement in node.body:
            if isinstance(statement, (ast.Import, ast.ImportFrom)):
                self.visit(statement)

    def visit_ImportFrom(  # pylint: disable=invalid-name
        self,
        node: ast.ImportFrom,
    ) -> None:
        for alias in node.names:
            if (alias.asname or alias.name) == self.symbol:
                self.import_reference = (node.module, node.level, alias.name)

    def visit_Import(self, node: ast.Import) -> None:  # pylint: disable=invalid-name
        for alias in node.names:
            local_name = alias.asname or alias.name.split(".", maxsplit=1)[0]
            if local_name == self.symbol:
                module = alias.name if alias.asname else local_name
                self.import_reference = (module, 0, None)


class DependenciesVisitor(ast.NodeVisitor):
    def __init__(
        self,
        root_folder_path: str,
        module_filepath: str,
    ) -> None:
        self.root_folder = Path(root_folder_path).resolve()
        self.module_filepath = Path(module_filepath).resolve()
        self.dependencies = set[str]()
        self.parsed_modules = dict[Path, ast.Module]()
        self.resolved_symbols = dict[tuple[Path, str], Path]()

    def parse_module(self, module: Path) -> ast.Module | None:
        log.debug(f"parse_module.{module = }")
        if module in self.parsed_modules:
            return self.parsed_modules[module]
        try:
            abstract_syntax_tree = ast.parse(module.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeDecodeError):
            return None
        self.parsed_modules[module] = abstract_syntax_tree
        log.debug(f"parse_module.{abstract_syntax_tree = }")
        return abstract_syntax_tree

    def get_symbol_file_path(
        self,
        module: Path,
        symbol: str,
        visited: set[tuple[Path, str]],
    ) -> Path | None:
        log.debug(f"get_symbol_file_path.{symbol = }")
        key = (module, symbol)
        if key in self.resolved_symbols:
            return self.resolved_symbols[key]
        if key in visited:
            return None

        tree = self.parse_module(module)
        if tree is None:
            return module

        visited.add(key)
        visitor = TraceSymbolVisitor(symbol)
        visitor.visit(tree)

        symbol_file_path = module
        if visitor.import_reference is not None:
            imported_module, level, imported_name = visitor.import_reference
            source = get_module_path(
                self.root_folder,
                module,
                imported_module,
                level,
            )
            if source is not None:
                if imported_name is None:
                    symbol_file_path = source
                else:
                    traced = self.get_symbol_file_path(source, imported_name, visited)
                    symbol_file_path = traced or source
                    if traced is None and source.name == "__init__.py":
                        symbol_file_path = (
                            import_path_to_file_path(source.parent / imported_name)
                            or source
                        )
        elif module.name == "__init__.py":
            symbol_file_path = (
                import_path_to_file_path(module.parent / symbol) or module
            )

        visited.remove(key)
        self.resolved_symbols[key] = symbol_file_path
        log.debug(f"get_symbol_file_path.{symbol_file_path = }")
        return symbol_file_path

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pylint: disable=invalid-name
        source = get_module_path(
            self.root_folder,
            self.module_filepath,
            node.module,
            node.level,
        )
        if source is None:
            return

        for alias in node.names:
            dependency = (
                source
                if alias.name == "*"
                else self.get_symbol_file_path(source, alias.name, set()) or source
            )
            self.dependencies.add(
                filepath_to_module_name(dependency, self.root_folder),
            )

    def visit_Import(self, node: ast.Import) -> None:  # pylint: disable=invalid-name
        for alias in node.names:
            dependency = get_module_path(
                self.root_folder,
                self.module_filepath,
                alias.name,
                level=0,
            )
            if dependency is not None:
                self.dependencies.add(
                    filepath_to_module_name(dependency, self.root_folder),
                )
