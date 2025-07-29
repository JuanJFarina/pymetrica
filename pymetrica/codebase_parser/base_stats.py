import click
from .codebase_parser import parse_codebase


@click.command()
@click.argument("dir_path")
def base_stats(dir_path: str):
    results = parse_codebase(dir_path)
    click.echo(
        f"root_folder_path: {results.root_folder_path}\n"
        f"root_folder_name: {results.root_folder_name}\n"
        f"folders_number: {results.folders_number}\n"
        f"files_number: {results.files_number}\n"
        f"lloc_number: {results.lloc_number}\n"
        f"comments_number: {results.comments_number}\n"
        f"comment_line_ratio: {results.comment_line_ratio}\n"
        f"classes_number: {results.classes_number}\n"
        f"functions_number: {results.functions_number}"
    )
