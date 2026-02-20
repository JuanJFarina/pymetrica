import ast
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

from pymetrica.models import Codebase


LayerName, ComponentName, Dependency = str, str, str
Dependencies = list[Dependency]
Components = dict[ComponentName, Dependencies]
Layers = dict[LayerName, Components]


def create_diagram(codebase: Codebase) -> None:
    layers: Layers = {
        str(dir): Components() for dir in iterdir_generator(codebase.root_folder_path)
    }

    for layer_name in layers.keys():
        layers[layer_name].update({
            str(dir): [] for dir in iterdir_generator(layer_name)
        })

    dependencies_visitor = DependenciesVisitor(layers)

    for file in codebase.files:
        print(f"create_diagram.{file.filepath = }")
        if is_root_file(file.filepath, codebase.root_folder_path):
            continue
        for layer in layers.keys():
            if is_component(file.filepath, layer):  # type: ignore
                layers[layer][file.filepath] = []
        dependencies_visitor.current_layer = file.filepath.rsplit("/")[-2]
        dependencies_visitor.current_component = file.filepath
        dependencies_visitor.visit(ast.parse(file.code))

    print(f"create_diagram.{layers = }")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"architecture_diagram_{timestamp}.mmd"
    with open(filename, "w") as f:
        f.write("graph TD\n")
        for layer_name, components in layers.items():
            f.write(f"  subgraph {layer_name}\n")
            for component_name, dependencies in components.items():
                f.write(f"    {component_name}\n")
            f.write("  end\n")
        for layer_name, components in layers.items():
            for component_name, dependencies in components.items():
                for dep in dependencies:
                    f.write(f"  {component_name} --> {dep}\n")


def iterdir_generator(path: str) -> Generator[str, None, None]:
    for dir in Path(path).iterdir():
        if dir.is_dir() and dir.name != "__pycache__":
            yield str(dir)


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
        self.current_layer: str = ""
        self.current_component: str = ""

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pylint: disable=invalid-name
        module_name = node.module if node.module else "relative import"
        imported_layer = module_name.rsplit(".")[-1]
        if imported_layer in self.layers_names and imported_layer != self.current_layer:
            full_layer_name = [
                layer
                for layer in self.layers.keys()
                if layer.rsplit("/")[-1] == self.current_layer
            ]
            if not full_layer_name:
                return
            full_layer_name = full_layer_name[0]
            full_imported_layer_name = [
                layer
                for layer in self.layers.keys()
                if layer.rsplit("/")[-1] == imported_layer
            ][0]
            self.layers[full_layer_name][self.current_component].extend([
                full_imported_layer_name
            ])
