import sys

import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import Configuration, run_profiler

from .mc_calculator import MaintainabilityCostCalculator

mc_calculator: MaintainabilityCostCalculator = MaintainabilityCostCalculator()


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@run_profiler
def mc(
    dir_path: str,
    report_type: str,
) -> int:
    codebase = parse_codebase(dir_path)
    mc_metric = mc_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([mc_metric]))
    exit_status = (
        0
        if Configuration.mc_fail_threshold == 0
        or mc_metric.results.maintainability_cost <= Configuration.mc_fail_threshold
        else 1
    )
    if exit_status > 0:
        click.echo(
            mc_metric.results.get_fail_message(Configuration.mc_fail_threshold),
            err=True,
        )
    sys.exit(exit_status)
