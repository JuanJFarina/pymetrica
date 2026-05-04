import sys

import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import Config, run_profiler

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
    exit_status = (
        0
        if Config.po_fail_threshold == 0
        or po_metric.results.strict_po <= Config.po_fail_threshold
        else 1
    )
    if exit_status > 0:
        click.echo(
            po_metric.results.get_fail_message(Config.po_fail_threshold),
            err=True,
        )
    sys.exit(exit_status)
