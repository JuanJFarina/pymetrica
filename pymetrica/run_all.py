import click

from pymetrica.codebase_parser import parse_codebase


@click.command()
@click.argument("dir_path")
def run_all(dir_path: str) -> None:
    results = parse_codebase(dir_path)
    click.echo(
        f"Parsed codebase from {results.root_folder_name} with {results.files_number} files.",
    )
