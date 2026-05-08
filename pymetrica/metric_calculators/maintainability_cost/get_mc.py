import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import run_profiler

from .mc_calculator import MaintainabilityCostCalculator

mc_calculator: MaintainabilityCostCalculator = MaintainabilityCostCalculator()


@click.command()
@click.option(
    "-a",
    "--audit",
    is_flag=True,
    help="Whether to generate an audit report.",
)
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@click.argument("dir_path")
@run_profiler
def mc(
    dir_path: str,
    report_type: str,
    audit: bool = False,
) -> None:
    codebase = parse_codebase(dir_path)
    mc_metric = mc_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]([mc_metric])
    report = report_generator.long_report(audit)

    report.echo_and_exit()
