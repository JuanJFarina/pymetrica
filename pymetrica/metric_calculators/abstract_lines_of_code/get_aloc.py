import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING

from .aloc_calculator import AlocCalculator


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
def aloc(
    dir_path: str,
    report_type: str,
    aloc_calculator: AlocCalculator = AlocCalculator(),
) -> None:
    codebase = parse_codebase(dir_path)
    aloc_metric = aloc_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([aloc_metric]))
