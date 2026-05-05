import sys

import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import run_profiler

from .po_calculator import PrimitiveObsessionCalculator

po_calculator: PrimitiveObsessionCalculator = PrimitiveObsessionCalculator()


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@run_profiler
def po(
    dir_path: str,
    report_type: str,
) -> int:
    codebase = parse_codebase(dir_path)
    po_metric = po_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]([po_metric])
    report = report_generator.long_report

    click.echo(report.content)
    sys.exit(report.exit_status)
