import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING

from .instability_calculator import InstabilityCalculator


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
def instability(
    dir_path: str,
    report_type: str,
    instability_calculator: InstabilityCalculator = InstabilityCalculator(),
) -> None:
    codebase = parse_codebase(dir_path)
    instability_metric = instability_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([instability_metric]))
