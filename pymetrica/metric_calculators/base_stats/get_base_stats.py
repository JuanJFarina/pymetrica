import click

from pymetrica.codebase_parser import create_diagram, parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import run_profiler

from .base_stats_calculator import BaseStatsCalculator

base_stats_calculator = BaseStatsCalculator()


@click.command()
@click.option(
    "--diagram",
    is_flag=True,
    help="Whether to generate a diagram of the codebase structure.",
)
@click.argument("dir_path")
@click.argument("diagram_filename", required=False)
@run_profiler
def base_stats(
    dir_path: str,
    diagram: bool = False,
    diagram_filename: str | None = None,
) -> None:
    codebase = parse_codebase(dir_path)
    if diagram:
        create_diagram(codebase, filename=diagram_filename)

    metric = base_stats_calculator.calculate_metric(codebase)
    report = REPORTS_MAPPING["BASIC_TERMINAL"]([metric]).long_report()
    report.echo_and_exit()
