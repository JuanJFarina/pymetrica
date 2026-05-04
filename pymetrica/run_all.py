import sys

import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.models.metric import Metric, Results
from pymetrica.report_generators.reports_mapping import REPORTS_MAPPING

from .metric_calculators import (
    AlocCalculator,
    CCCalculator,
    HalsteadVolumeCalculator,
    InstabilityCalculator,
    MaintainabilityCostCalculator,
    PrimitiveObsessionCalculator,
)

aloc_calculator: AlocCalculator = AlocCalculator()
cc_calculator: CCCalculator = CCCalculator()
hv_calculator: HalsteadVolumeCalculator = HalsteadVolumeCalculator()
mc_calculator: MaintainabilityCostCalculator = MaintainabilityCostCalculator()
po_calculator: PrimitiveObsessionCalculator = PrimitiveObsessionCalculator()
instability_calculator: InstabilityCalculator = InstabilityCalculator()


@click.command()
@click.option(
    "--long-report",
    is_flag=True,
    help="Whether to generate a long summary report for each metric.",
)
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
def run_all(
    dir_path: str,
    report_type: str,
    long_report: bool = False,
) -> None:
    codebase = parse_codebase(dir_path)
    metrics = list[Metric[Results]]()
    metrics.append(aloc := aloc_calculator.calculate_metric(codebase))
    metrics.append(cc := cc_calculator.calculate_metric(codebase))
    metrics.append(hv := hv_calculator.calculate_metric(codebase))
    metrics.append(po := po_calculator.calculate_metric(codebase))
    metrics.append(mc := mc_calculator.calculate_metric(codebase))
    metrics.append(instability_calculator.calculate_metric(codebase))

    report_generator = REPORTS_MAPPING[report_type]()
    if long_report:
        click.echo(report_generator.generate_report(metrics))
        return
    click.echo(report_generator.generate_short_report(metrics))

    exit_status = 0

    if aloc.results.exceeds_threshold:
        click.echo(aloc.results.fail_message, err=True)
        exit_status += 1

    if cc.results.exceeds_threshold:
        click.echo(cc.results.fail_message, err=True)
        exit_status += 2

    if hv.results.exceeds_threshold:
        click.echo(hv.results.fail_message, err=True)
        exit_status += 10

    if po.results.exceeds_threshold:
        click.echo(po.results.fail_message, err=True)
        exit_status += 20

    if mc.results.exceeds_threshold:
        click.echo(mc.results.fail_message, err=True)
        exit_status += 100

    sys.exit(exit_status)
