import click

from pymetrica.codebase_parser import parse_codebase
from pymetrica.report_generators import REPORTS_MAPPING

from .hv_calculator import HalsteadVolumeCalculator


@click.command()
@click.argument("dir_path")
@click.option("-rt", "--report-type", type=str, default="BASIC_TERMINAL")
def halstead_volume(
    dir_path: str,
    report_type: str,
    hv_calculator: HalsteadVolumeCalculator = HalsteadVolumeCalculator(),
) -> None:
    codebase = parse_codebase(dir_path)
    hv_metric = hv_calculator.calculate_metric(codebase)
    report_generator = REPORTS_MAPPING[report_type]()
    click.echo(report_generator.generate_report([hv_metric]))
