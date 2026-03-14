import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import run_profiler

from .mc_calculator import MaintainabilityCostCalculator


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@run_profiler
def mc(
    dir_path: str,
    report_type: str,
    mc_calculator: MaintainabilityCostCalculator = MaintainabilityCostCalculator(),
) -> None:
    codebase = parse_codebase(dir_path)
    mc_metric = mc_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([mc_metric]))
