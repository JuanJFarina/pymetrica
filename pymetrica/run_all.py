import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.models.metric import Metric, Results
from pymetrica.report_generators.reports_mapping import REPORTS_MAPPING
from pymetrica.utils.profiler import run_profiler

from .metric_calculators import (
    AlocCalculator,
    BaseStatsCalculator,
    CCCalculator,
    HalsteadVolumeCalculator,
    InstabilityCalculator,
    MaintainabilityCostCalculator,
    PrimitiveObsessionCalculator,
)

base_stats_calculator: BaseStatsCalculator = BaseStatsCalculator()
aloc_calculator: AlocCalculator = AlocCalculator()
cc_calculator: CCCalculator = CCCalculator()
hv_calculator: HalsteadVolumeCalculator = HalsteadVolumeCalculator()
mc_calculator: MaintainabilityCostCalculator = MaintainabilityCostCalculator()
po_calculator: PrimitiveObsessionCalculator = PrimitiveObsessionCalculator()
instability_calculator: InstabilityCalculator = InstabilityCalculator()


@click.command()
@click.option(
    "-a",
    "--audit",
    is_flag=True,
    help="Whether to get top findings regardless of threshold values.",
)
@click.option(
    "-lr",
    "--long-report",
    is_flag=True,
    help="Whether to generate a long summary report for each metric.",
)
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@click.argument("dir_path")
@run_profiler
def run_all(
    dir_path: str,
    report_type: str,
    audit: bool = False,
    long_report: bool = False,
) -> None:
    codebase = parse_codebase(dir_path)
    metrics = list[Metric[Results]]()
    metrics.append(base_stats_calculator.calculate_metric(codebase))
    metrics.append(aloc_calculator.calculate_metric(codebase))
    metrics.append(cc_calculator.calculate_metric(codebase))
    metrics.append(hv_calculator.calculate_metric(codebase))
    metrics.append(po_calculator.calculate_metric(codebase))
    metrics.append(mc_calculator.calculate_metric(codebase))
    metrics.append(instability_calculator.calculate_metric(codebase))

    report_generator = REPORTS_MAPPING[report_type](metrics)

    if long_report:
        report = report_generator.long_report(audit)
    else:
        report = report_generator.short_report(audit)

    report.echo_and_exit()
