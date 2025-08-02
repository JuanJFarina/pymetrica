from __future__ import annotations

import click

from .aloc_calculator import AlocCalculator
from pymetrica.codebase_parser import parse_codebase


@click.command()
@click.argument('dir_path')
def aloc(dir_path: str, aloc_calculator: AlocCalculator = AlocCalculator()) -> None:
    codebase = parse_codebase(dir_path)
    aloc_result = aloc_calculator.calculate_metric(codebase)
    click.echo(aloc_result)
    click.echo(
        f'Total logical lines of code in codebase: {codebase.lloc_number}',
    )
