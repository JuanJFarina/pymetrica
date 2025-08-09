import click

from pymetrica.metric_calculators import (
    aloc,
    cc,
    halstead_volume,
    maintainability_index,
)

from .codebase_parser import base_stats
from .run_all import run_all
from .status import status


@click.group()
def main() -> None: ...


main.add_command(status)
main.add_command(run_all)
main.add_command(base_stats)
main.add_command(aloc)
main.add_command(cc)
main.add_command(halstead_volume)
main.add_command(maintainability_index)
