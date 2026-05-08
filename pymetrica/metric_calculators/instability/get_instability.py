import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils.profiler import run_profiler

from .instability_calculator import InstabilityCalculator

instability_calculator: InstabilityCalculator = InstabilityCalculator()


@click.command()
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@click.argument("dir_path")
@run_profiler
def li(
    dir_path: str,
    report_type: str,
    audit: bool = False,
) -> None:
    codebase = parse_codebase(dir_path)
    instability_metric = instability_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]([instability_metric])
    report = report_generator.long_report(audit)

    report.echo_and_exit()
