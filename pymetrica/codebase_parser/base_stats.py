import click

from pymetrica.utils import run_profiler

from .codebase_parser import parse_codebase
from .diagram_generator import create_diagram


@click.command()
@click.option(
    "--diagram",
    is_flag=True,
    help="Whether to generate a diagram of the codebase structure.",
)
@click.argument("dir_path")
@click.argument("diagram_filename", default=None)
@run_profiler
def base_stats(
    dir_path: str,
    diagram: bool = False,
    diagram_filename: str | None = None,
) -> None:
    results = parse_codebase(dir_path)
    if diagram:
        create_diagram(results, filename=diagram_filename)
    click.echo(
        f"root_folder_path: {results.root_folder_path}\n"
        f"root_folder_name: {results.root_folder_name}\n"
        f"folders_number: {results.folders_number}\n"
        f"files_number: {results.files_number}\n"
        f"lloc_number: {results.lloc_number}\n"
        f"lloc_file_ratio: {results.lloc_file_ratio}\n"
        f"comments_number: {results.comments_number}\n"
        f"comment_line_ratio: {results.comment_lloc_ratio}\n"
        f"classes_number: {results.classes_number}\n"
        f"functions_number: {results.functions_number}",
    )
