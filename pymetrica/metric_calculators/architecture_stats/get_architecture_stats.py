import click

from pymetrica.codebase_parser import parse_codebase

# from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import log, run_profiler
from pymetrica.utils.settings import update_config_from_pyproject

from .diagram_generator import create_diagram
from .graph_builder import create_graph


@click.command()
@click.option(
    "--diagram",
    is_flag=True,
    help="Whether to generate a diagram of the codebase structure.",
)
@click.argument("dir_path", default=".")
@click.argument("diagram_filename", required=False)
@run_profiler
def architecture_stats(
    dir_path: str,
    diagram: bool = False,
    diagram_filename: str | None = None,
) -> None:
    update_config_from_pyproject(dir_path)
    codebase = parse_codebase(dir_path)
    graph = create_graph(codebase)
    if diagram:
        rendered_diagram = create_diagram(graph, filename=diagram_filename)
        if diagram_filename is None:
            click.echo(rendered_diagram)

    log.info("Architecture stats calculation is not implemented yet.")
    # metric = architecture_stats_calculator.calculate_metric(codebase)
    # report = REPORTS_MAPPING["BASIC_TERMINAL"]([metric]).long_report()
    # report.echo_and_exit()
