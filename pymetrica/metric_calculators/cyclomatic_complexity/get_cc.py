import sys

import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import Configuration, run_profiler

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
    exit_status = (
        0
        if Configuration.cc_fail_threshold == 0
        or cc_metric.results.lloc_per_cc >= Configuration.cc_fail_threshold
        else 1
    )
    if exit_status > 0:
        click.echo(
            f"LLOC per CC {cc_metric.results.lloc_per_cc:.2f} exceeds the "
            f"fail threshold of {Configuration.cc_fail_threshold}",
            err=True,
        )
    sys.exit(exit_status)
