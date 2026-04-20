import sys

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
from pymetrica.utils import Configuration

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
    codebase = parse_codebase(dir_path)
    metrics = list[Metric[Results]]()
    metrics.append(aloc_calculator.calculate_metric(codebase))
    metrics.append(cc_calculator.calculate_metric(codebase))
    metrics.append(hv_calculator.calculate_metric(codebase))
    metrics.append(mc_calculator.calculate_metric(codebase))
    metrics.append(instability_calculator.calculate_metric(codebase))

    report_generator = REPORTS_MAPPING[report_type]()
    if long_report:
        click.echo(report_generator.generate_report(metrics))
        return
    click.echo(report_generator.generate_short_report(metrics))

    exit_status = 0
    if (
        Configuration.aloc_fail_threshold != 0
        and metrics[0].results.aloc_percentage > Configuration.aloc_fail_threshold  # type: ignore[attr-defined]  # pylint: disable=line-too-long
    ):
        click.echo(
            f"ALOC percentage {metrics[0].results.aloc_percentage:.2f}% exceeds "  # type: ignore[attr-defined]  # pylint: disable=line-too-long
            f"the fail threshold of {Configuration.aloc_fail_threshold}%",
        )
        exit_status += 1
    if (
        Configuration.cc_fail_threshold != 0
        and metrics[1].results.lloc_per_cc > Configuration.cc_fail_threshold  # type: ignore[attr-defined]  # pylint: disable=line-too-long
    ):
        click.echo(
            f"LLOC per CC {metrics[1].results.lloc_per_cc:.2f} exceeds the "  # type: ignore[attr-defined]  # pylint: disable=line-too-long
            f"fail threshold of {Configuration.cc_fail_threshold}",
        )
        exit_status += 10
    if (
        Configuration.hv_fail_threshold != 0
        and metrics[2].results.hv_per_lloc > Configuration.hv_fail_threshold  # type: ignore[attr-defined]  # pylint: disable=line-too-long
    ):
        click.echo(
            f"Halstead Volume per LLOC {metrics[2].results.hv_per_lloc:.2f} "  # type: ignore[attr-defined]  # pylint: disable=line-too-long
            f"exceeds the fail threshold of {Configuration.hv_fail_threshold}",
        )
        exit_status += 100
    if (
        Configuration.mc_fail_threshold != 0
        and metrics[3].results.maintainability_cost > Configuration.mc_fail_threshold  # type: ignore[attr-defined]  # pylint: disable=line-too-long
    ):
        click.echo(
            f"Maintainability Cost {metrics[3].results.maintainability_cost:.2f} "  # type: ignore[attr-defined]  # pylint: disable=line-too-long
            f"exceeds the fail threshold of {Configuration.mc_fail_threshold}",
        )
        exit_status += 1000
    sys.exit(exit_status)
