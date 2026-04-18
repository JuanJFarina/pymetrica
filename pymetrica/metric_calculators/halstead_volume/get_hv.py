import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING
from pymetrica.utils import Configuration, run_profiler

from .hv_calculator import HalsteadVolumeCalculator

hv_calculator: HalsteadVolumeCalculator = HalsteadVolumeCalculator()


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
@run_profiler
def hv(
    dir_path: str,
    report_type: str,
) -> int:
    codebase = parse_codebase(dir_path)
    hv_metric = hv_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([hv_metric]))
    return (
        0
        if Configuration.hv_fail_threshold == 0
        or hv_metric.results.hv_number <= Configuration.hv_fail_threshold
        else 1
    )
