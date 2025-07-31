import click
from pymetrica.models import Codebase
from pymetrica.codebase_parser import parse_codebase
from .aloc_calculator import AlocCalculator

@click.command()
@click.argument("dir_path")
def aloc(dir_path: str, aloc_calculator: AlocCalculator = AlocCalculator()) -> None:
    codebase = parse_codebase(dir_path)
    aloc_result = aloc_calculator.calculate_metric(codebase)
    click.echo(aloc_result)
    click.echo(codebase.lloc_number)
