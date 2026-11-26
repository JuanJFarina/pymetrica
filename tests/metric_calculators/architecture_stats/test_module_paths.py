from pathlib import Path

from pymetrica.metric_calculators.architecture_stats.module_paths import (
    filepath_to_module_name,
)


def test_creates_full_module_name_from_package_root(tmp_path: Path) -> None:
    root = tmp_path / "acme"
    module = root / "api" / "routes.py"
    module.parent.mkdir(parents=True)
    (root / "__init__.py").write_text("", encoding="utf-8")
    module.write_text("", encoding="utf-8")

    assert filepath_to_module_name(module, root) == "acme.api.routes"


def test_creates_module_name_from_source_root(tmp_path: Path) -> None:
    root = tmp_path / "src"
    module = root / "acme" / "api" / "routes.py"
    module.parent.mkdir(parents=True)
    module.write_text("", encoding="utf-8")

    assert filepath_to_module_name(module, root) == "acme.api.routes"


def test_maps_init_file_to_its_package_name(tmp_path: Path) -> None:
    root = tmp_path / "acme"
    module = root / "api" / "__init__.py"
    module.parent.mkdir(parents=True)
    (root / "__init__.py").write_text("", encoding="utf-8")
    module.write_text("", encoding="utf-8")

    assert filepath_to_module_name(module, root) == "acme.api"
