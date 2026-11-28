from pathlib import Path

from pymetrica.metric_calculators.architecture_stats.graph_builder import (
    get_node_dependencies,
)
from pymetrica.models import Code, Codebase


def test_resolves_symbol_reexported_by_package(tmp_path: Path) -> None:
    root = tmp_path / "sample"
    exports = root / "exports"
    exports.mkdir(parents=True)

    source = "from sample.exports import Service\n"
    module = root / "consumer.py"
    module.write_text(source, encoding="utf-8")
    (root / "__init__.py").write_text("", encoding="utf-8")
    (exports / "__init__.py").write_text(
        "from .service import Service\n",
        encoding="utf-8",
    )
    (exports / "service.py").write_text(
        "class Service:\n    pass\n",
        encoding="utf-8",
    )

    code = Code(
        filepath=str(module),
        filename=module.name,
        lloc_number=1,
        comments_number=0,
        code_lines=[source],
        code=source,
    )

    assert get_node_dependencies(code, str(root)) == {"sample.exports.service"}


def test_resolves_relative_symbols_reexported_by_packages(
    big_codebase: Codebase,
) -> None:
    main = next(code for code in big_codebase.root_files if code.filename == "main.py")

    assert get_node_dependencies(main, big_codebase.root_folder_path) == {
        "big_codebase.exception_handlers.codebase_exception",
        "big_codebase.middlewares.logging_middleware",
        "big_codebase.routes.routes",
    }
