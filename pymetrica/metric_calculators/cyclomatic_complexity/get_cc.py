from __future__ import annotations

import click

from .cc_calculator import CCCalculator
from pymetrica.codebase_parser import parse_codebase


@click.command()
@click.argument('dir_path')
def cc(dir_path: str, cc_calculator: CCCalculator = CCCalculator()) -> None:
    codebase = parse_codebase(dir_path)
    cc_result = cc_calculator.calculate_metric(codebase)
    click.echo(cc_result)
    click.echo(
        f'Total logical lines of code in codebase: {codebase.lloc_number}',
    )
