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
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([po_metric]))
    exit_status = int(po_metric.results.exceeds_threshold)
    if exit_status > 0:
        click.echo(po_metric.results.fail_message, err=True)
    sys.exit(exit_status)
