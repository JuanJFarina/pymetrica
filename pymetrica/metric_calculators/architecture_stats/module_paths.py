from pathlib import Path


def filepath_to_module_name(
    filepath: str | Path,
    root_folder_path: str | Path,
) -> str:
    root = Path(root_folder_path).resolve()
    module = Path(filepath).resolve()
    import_root = root.parent if (root / "__init__.py").is_file() else root

    try:
        module.relative_to(root)
        relative = module.relative_to(import_root)
    except ValueError as error:
        raise ValueError(f"{module} is outside the codebase root {root}") from error

    if relative.name == "__init__.py":
        relative = relative.parent
    else:
        relative = relative.with_suffix("")

    return ".".join(relative.parts)
