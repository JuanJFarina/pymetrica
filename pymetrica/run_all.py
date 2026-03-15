import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.metric_calculators.abstract_lines_of_code.aloc_calculator import (
    AlocCalculator,
)
from pymetrica.metric_calculators.cyclomatic_complexity.cc_calculator import (
    CCCalculator,
)
from pymetrica.metric_calculators.halstead_volume.hv_calculator import (
    HalsteadVolumeCalculator,
)
from pymetrica.metric_calculators.instability.instability_calculator import (
    InstabilityCalculator,
)
from pymetrica.metric_calculators.maintainability_cost.mc_calculator import (
    MaintainabilityCostCalculator,
)
from pymetrica.models.metric import Metric, Results
from pymetrica.report_generators.reports_mapping import REPORTS_MAPPING

aloc_calculator: AlocCalculator = AlocCalculator()
cc_calculator: CCCalculator = CCCalculator()
hv_calculator: HalsteadVolumeCalculator = HalsteadVolumeCalculator()
mc_calculator: MaintainabilityCostCalculator = MaintainabilityCostCalculator()
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
    results = parse_codebase(dir_path)
    metrics = list[Metric[Results]]()
    metrics.append(aloc_calculator.calculate_metric(results))
    metrics.append(cc_calculator.calculate_metric(results))
    metrics.append(hv_calculator.calculate_metric(results))
    metrics.append(mc_calculator.calculate_metric(results))
    metrics.append(instability_calculator.calculate_metric(results))

    report_generator = REPORTS_MAPPING[report_type]()
    if long_report:
        click.echo(report_generator.generate_report(metrics))
        return
    click.echo(report_generator.generate_short_report(metrics))
