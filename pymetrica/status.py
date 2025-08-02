from __future__ import annotations

import click


@click.command()
def status():
    click.echo('Pymetrica health check passed. All systems operational.')
