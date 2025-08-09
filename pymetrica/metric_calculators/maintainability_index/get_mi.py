import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING

from .mi_calculator import MaintainabilityIndexCalculator


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
def maintainability_index(
    dir_path: str,
    report_type: str,
    mi_calculator: MaintainabilityIndexCalculator = MaintainabilityIndexCalculator(),
) -> None:
    codebase = parse_codebase(dir_path)
    mi_metric = mi_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([mi_metric]))
