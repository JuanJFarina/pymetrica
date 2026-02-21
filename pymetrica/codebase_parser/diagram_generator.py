import ast
from collections.abc import Generator
from datetime import datetime
import logging
from pathlib import Path
from typing import TypeAlias

from pymetrica.models import Codebase


LayerName: TypeAlias = str
ComponentName: TypeAlias = str
Dependency: TypeAlias = str
Dependencies: TypeAlias = set[Dependency]
Components: TypeAlias = dict[ComponentName, Dependencies]
Layers: TypeAlias = dict[LayerName, Components]


def create_diagram(codebase: Codebase) -> None:
    layers: Layers = {
        str(dir): Components() for dir in iterdir_generator(codebase.root_folder_path)
    }

    for layer_name in layers.keys():
        layers[layer_name].update({
            str(dir): set() for dir in iterdir_generator(layer_name)
        })

    dependencies_visitor = DependenciesVisitor(layers)

    for file in codebase.files:
        if is_root_file(file.filepath, codebase.root_folder_path):
            continue
        for layer in layers.keys():
            if is_component(file.filepath, layer):
                layers[layer][file.filepath] = set()
        dependencies_visitor.current_layer = file.filepath.rsplit("/")[-2]
        dependencies_visitor.current_component = file.filepath
        dependencies_visitor.visit(ast.parse(file.code))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"architecture_diagram_{timestamp}.mmd"
    with open(filename, "w") as f:  # pylint: disable=unspecified-encoding
        f.write("graph TD\n")
        for layer_name, components in layers.items():
            f.write(
                f"  subgraph {layer_name.replace(codebase.root_folder_path + '/', '')}\n",
            )
            for component_name, dependencies in components.items():
                f.write(
                    f"    {component_name.replace(codebase.root_folder_path + '/', '')}\n",
                )
            f.write("  end\n")
        for layer_name, components in layers.items():
            for component_name, dependencies in components.items():
                for dep in dependencies:
                    f.write(
                        f"  {component_name.replace(codebase.root_folder_path + '/', '')} --> {dep.replace(codebase.root_folder_path + '/', '')}\n",  # pylint: disable=line-too-long
                    )


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
    if relative_path.count("/") == 1:
        return True
    return False


def is_component(file_path: str, layer_name: str) -> bool:
    relative_path = file_path.replace(layer_name, "")
    if relative_path.count("/") == 1 and is_python_file_not_dunder(file_path):
        return True
    return False


def is_python_file_not_dunder(file_path: str) -> bool:
    return not file_path.endswith("__.py") and file_path.endswith(".py")


class DependenciesVisitor(ast.NodeVisitor):
    def __init__(self, layers: Layers) -> None:
        self.layers = layers
        self.layers_names = [layer.rsplit("/")[-1] for layer in layers.keys()]
        self.root_folder = list(layers.keys())[0].rsplit("/", 1)[0]
        self.current_layer: str = ""
        self.current_component: str = ""

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pylint: disable=invalid-name
        module_name = node.module if node.module else "relative import"
        print(f"DependenciesVisitor.visit_ImportFrom.{module_name = }")
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
                if layer.rsplit("/")[-1] == self.current_layer
            ]
            if not full_layer_name_list:
                return
            full_layer_name = full_layer_name_list[0]
            full_imported_layer_name = [
                layer
                for layer in self.layers.keys()
                if layer.rsplit("/")[-1] == imported_layer
            ][0]
            subdirectory_path = self.current_component.replace(
                self.root_folder,
                "",
            ).split("/", 1)[-1]
            if subdirectory_path.count("/") == 1:
                clean_current_component = self.root_folder + "/" + subdirectory_path
            else:
                clean_subdirectory_path = subdirectory_path.rsplit("/", 1)[0]
                clean_current_component = (
                    self.root_folder + "/" + clean_subdirectory_path
                )
            try:
                if self.layers[full_layer_name].get(clean_current_component):
                    self.layers[full_layer_name][clean_current_component].add(
                        full_imported_layer_name,
                    )
                else:
                    self.layers[full_layer_name].update({
                        clean_current_component: {full_imported_layer_name},
                    })
            except KeyError as e:
                logging.info(
                    f"DependenciesVisitor.visit_ImportFrom.KeyError.{clean_current_component = }",
                )
                logging.info(f"DependenciesVisitor.visit_ImportFrom.KeyError: {e = }")
