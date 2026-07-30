import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import run_profiler
from pymetrica.utils.settings import update_config_from_pyproject

from .mc_calculator import MaintainabilityCostCalculator

mc_calculator: MaintainabilityCostCalculator = MaintainabilityCostCalculator()


@click.command()
@click.option(
    "-a",
    "--audit",
    is_flag=True,
    help="Whether to get top findings regardless of threshold values.",
)
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@click.argument("dir_path", default=".")
@run_profiler
def mc(
    dir_path: str,
    report_type: str,
    audit: bool = False,
) -> None:
    update_config_from_pyproject(dir_path)
    codebase = parse_codebase(dir_path)
    mc_metric = mc_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]([mc_metric])
    report = report_generator.long_report(audit)

    report.echo_and_exit()
