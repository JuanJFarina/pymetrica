import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import run_profiler

from .cc_calculator import CCCalculator

cc_calculator: CCCalculator = CCCalculator()


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@run_profiler
def cc(
    dir_path: str,
    report_type: str,
) -> None:
    codebase = parse_codebase(dir_path)
    cc_metric = cc_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([cc_metric]))
