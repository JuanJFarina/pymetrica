import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import run_profiler
from pymetrica.utils.settings import update_config_from_pyproject

from .cc_calculator import CCCalculator

cc_calculator: CCCalculator = CCCalculator()


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
def cc(
    dir_path: str,
    report_type: str,
    audit: bool = False,
) -> None:
    update_config_from_pyproject(dir_path)
    codebase = parse_codebase(dir_path)
    cc_metric = cc_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]([cc_metric])
    report = report_generator.long_report(audit)

    report.echo_and_exit()
