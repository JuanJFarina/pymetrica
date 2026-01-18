import ast
from os import sep
from pymetrica.models.code import Code


Layer = str
Files = list[Code]


def clean_layer_name(layer_path: str) -> str:
    return " " + layer_path.rsplit(sep)[-2] + "." + layer_path.rsplit(sep)[-1]


def calculate_instability(
    analyzed_layer: Layer,
    files_by_layer: dict[Layer, Files],
) -> float:
    analyzed_layer = clean_layer_name(analyzed_layer)
    all_layers = [clean_layer_name(layer) for layer in files_by_layer.keys()]
    efferent_coupling = 0
    afferent_coupling = 0
    for layer in files_by_layer.keys():
        instability_visitor = InstabilityVisitor(
            analyzed_layer,
            clean_layer_name(layer),
            all_layers,
        )
        for file in files_by_layer[layer]:
            instability_visitor.visit(ast.parse(file.code))

        efferent_coupling += instability_visitor.efferent_imports
        afferent_coupling += instability_visitor.afferent_imports

    if efferent_coupling == 0:
        return 0.0

    return efferent_coupling / (efferent_coupling + afferent_coupling)


class InstabilityVisitor(ast.NodeVisitor):
    def __init__(
        self,
        analyzed_layer: Layer,
        traversing_layer: Layer,
        all_layers: list[Layer],
    ) -> None:
        self.analyzed_layer = analyzed_layer
        self.all_layers = all_layers
        self.efferent_imports = 0
        self.afferent_imports = 0

        if analyzed_layer == traversing_layer:
            self.look_for_efferent = True
        else:
            self.look_for_efferent = False

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pylint: disable=invalid-name
        module_name = node.module if node.module else "relative import"
        module_name = " " + module_name + " "
        if self.look_for_efferent:
            for layer in self.all_layers:
                if layer != self.analyzed_layer and layer in module_name:
                    self.efferent_imports += 1
                    break
        if not self.look_for_efferent:
            if self.analyzed_layer in module_name:
                self.afferent_imports += 1
        self.generic_visit(node)
