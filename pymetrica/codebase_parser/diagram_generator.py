import ast
from collections.abc import Callable, Generator
from datetime import datetime
from pathlib import Path
from typing import TypeAlias

from os import sep

from pymetrica.models import Codebase
from pymetrica.utils import log


LayerName: TypeAlias = str
ComponentName: TypeAlias = str
Dependency: TypeAlias = str
Dependencies: TypeAlias = list[Dependency]
Components: TypeAlias = dict[ComponentName, Dependencies]
Layers: TypeAlias = dict[LayerName, Components]


def create_diagram(codebase: Codebase, write: bool = True) -> None:
    layers: Layers = {
        str(dir): Components() for dir in iterdir_generator(codebase.root_folder_path)
    }

    if len(layers) == 0:
        log.warning(f"create_diagram.{codebase.root_folder_path = }")
        layers = {codebase.root_folder_path: Components()}

    for layer_name in layers.keys():
        layers[layer_name].update({
            str(dir): [] for dir in iterdir_generator(layer_name)
        })

    dependencies_visitor = DependenciesVisitor(layers)

    for file in codebase.files:
        if is_root_file(file.filepath, codebase.root_folder_path):
            continue
        for layer in layers.keys():
            if is_component(file.filepath, layer):
                layers[layer][file.filepath] = list()
        dependencies_visitor.current_layer = sep.join(
            file.filepath.replace(codebase.root_folder_path + sep, "").split(sep)[:1],
        )
        dependencies_visitor.current_component = file.filepath
        dependencies_visitor.visit(ast.parse(file.code))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if write:
        with open(f"architecture_diagram_{timestamp}.mmd", "w") as f:  # pylint: disable=unspecified-encoding
            write_diagram(codebase, layers, f.write)
    else:
        write_diagram(codebase, layers, print)


def write_diagram(
    codebase: Codebase,
    layers: Layers,
    write_function: Callable[..., None | int],
) -> None:
    write_function('%%{init: {"themeCSS": ".edgeLabel {font-size: 30px;}"}}%%\n\n')
    write_function("graph TD\n")
    for layer_name, components in layers.items():
        write_function(
            f"  subgraph {layer_name.replace(codebase.root_folder_path + sep, '')}\n",
        )
        for component_name, dependencies in components.items():
            write_function(
                f"    {component_name.replace(codebase.root_folder_path + sep, '')}\n",
            )
        write_function("  end\n")
    for layer_name, components in layers.items():
        for component_name, dependencies in components.items():
            dependencies_count = count_dependencies(dependencies)
            for dep, count in dependencies_count.items():
                write_function(
                    f"  {component_name.replace(codebase.root_folder_path + sep, '')} -- {count} --> {dep.replace(codebase.root_folder_path + sep, '')}\n",  # pylint: disable=line-too-long
                )


def count_dependencies(dependencies: Dependencies) -> dict[str, int]:
    dependencies_count = dict[str, int]()
    for dep in dependencies:
        dependencies_count[dep] = dependencies_count.get(dep, 0) + 1
    return dependencies_count


def iterdir_generator(path: str) -> Generator[str, None, None]:
    for directory in Path(path).iterdir():
        if (
            directory.is_dir()
            and directory.name != "__pycache__"
            and directory.name.startswith(".") is False
        ):
            yield str(directory)


def is_root_file(file_path: str, root_folder_path: str) -> bool:
    relative_path = file_path.replace(root_folder_path, "")
    if relative_path.count(sep) == 1:
        return True
    return False


def is_component(file_path: str, layer_name: str) -> bool:
    relative_path = file_path.replace(layer_name, "")
    if relative_path.count(sep) == 1 and is_python_file_not_dunder(file_path):
        return True
    return False


def is_python_file_not_dunder(file_path: str) -> bool:
    return not file_path.endswith("__.py") and file_path.endswith(".py")


class DependenciesVisitor(ast.NodeVisitor):
    def __init__(self, layers: Layers) -> None:
        self.layers = layers
        self.layers_names = [layer.rsplit(sep)[-1] for layer in layers.keys()]
        self.root_folder = list(layers.keys())[0].rsplit(sep, 1)[0]
        self.current_layer: str = ""
        self.current_component: str = ""

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pylint: disable=invalid-name
        module_name = node.module if node.module else "relative import"
        split_module_name = module_name.rsplit(".")
        if len(split_module_name) >= 2:
            imported_layer = split_module_name[1]
        else:
            imported_layer = split_module_name[0]
        if (
            split_module_name[0] in self.layers_names
            and split_module_name[0] != self.current_layer
        ):
            imported_layer = split_module_name[0]
        if imported_layer in self.layers_names and imported_layer != self.current_layer:
            full_layer_name_list = [
                layer
                for layer in self.layers.keys()
                if layer.rsplit(sep)[-1] == self.current_layer
            ]
            if not full_layer_name_list:
                return
            full_layer_name = full_layer_name_list[0]
            full_imported_layer_name = [
                layer
                for layer in self.layers.keys()
                if layer.rsplit(sep)[-1] == imported_layer
            ][0]
            subdirectory_path = self.current_component.replace(
                self.root_folder,
                "",
            ).split(sep, 1)[-1]
            if subdirectory_path.count(sep) == 1:
                clean_current_component = self.root_folder + sep + subdirectory_path
            else:
                clean_subdirectory_path = sep.join(subdirectory_path.split(sep, 2)[:2])
                clean_current_component = (
                    self.root_folder + sep + clean_subdirectory_path
                )
            try:
                if self.layers[full_layer_name].get(clean_current_component):
                    self.layers[full_layer_name][clean_current_component].append(
                        full_imported_layer_name,
                    )
                else:
                    self.layers[full_layer_name].update({
                        clean_current_component: [full_imported_layer_name],
                    })
            except KeyError as e:
                log.warning(
                    f"DependenciesVisitor.visit_ImportFrom.KeyError.{clean_current_component = }",
                )
                log.warning(f"DependenciesVisitor.visit_ImportFrom.KeyError: {e = }")
