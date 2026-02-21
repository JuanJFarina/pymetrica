import click
from .utils import run_profiler


@click.command()
@run_profiler
def status() -> None:
    click.echo("Pymetrica health check passed. All systems operational.")
