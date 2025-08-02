from __future__ import annotations

import click

from .codebase_parser import base_stats
from .run_all import run_all
from .status import status
from pymetrica.metric_calculators import aloc
from pymetrica.metric_calculators import cc


@click.group()
def main(): ...


main.add_command(status)
main.add_command(run_all)
main.add_command(base_stats)
main.add_command(aloc)
main.add_command(cc)
