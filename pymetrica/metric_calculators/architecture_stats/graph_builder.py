import ast

from pymetrica.models import Code, Codebase, Edge, Graph, Node
from pymetrica.utils import log

from .dependencies_visitor import DependenciesVisitor
from .module_paths import filepath_to_module_name


def create_graph(codebase: Codebase) -> Graph:
    modules = [
        (
            filepath_to_module_name(code.filepath, codebase.root_folder_path),
            code,
        )
        for code in codebase.non_init_files
    ]
    modules.sort(key=lambda module: module[0])
    module_names = {name for name, _ in modules}
    package_names = {
        filepath_to_module_name(code.filepath, codebase.root_folder_path)
        for code in codebase.files
        if code.filename == "__init__.py"
    }
    dependency_targets = module_names | package_names
    nodes = list[Node]()

    for module_name, code in modules:
        found_dependencies = get_node_dependencies(code, codebase.root_folder_path)
        dependencies = sorted(found_dependencies & dependency_targets)
        unresolved_dependencies = found_dependencies - dependency_targets
        if unresolved_dependencies:
            log.debug(
                "Ignoring dependencies without graph nodes: "
                f"{sorted(unresolved_dependencies)}",
            )
        nodes.append(Node(name=module_name, dependencies=dependencies))

    edges = [
        Edge(source=node.name, target=dependency, weight=1)
        for node in nodes
        for dependency in node.dependencies
    ]
    return Graph(nodes=nodes, edges=edges)


def get_node_dependencies(code: Code, root_folder_path: str) -> set[str]:
    log.info(f"Getting dependencies for code: {code.filepath}")
    visitor = DependenciesVisitor(root_folder_path, code.filepath)
    visitor.visit(ast.parse(code.code))
    log.info(f"Dependencies: {visitor.dependencies}")
    return visitor.dependencies
