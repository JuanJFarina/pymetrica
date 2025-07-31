from pymetrica.metric_calculators import aloc
from .deprecated_all import deprecated_all
from .run_all import run_all
from .status import status
from .codebase_parser import base_stats
import click


@click.group()
def main(): ...


main.add_command(status)
main.add_command(deprecated_all)
main.add_command(run_all)
main.add_command(base_stats)
main.add_command(aloc)
