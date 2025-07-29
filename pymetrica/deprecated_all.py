from pymetrica.deprecated.first_pass import gather_loc_and_classes
from pymetrica.deprecated.second_pass import count_uninstantiated_loc
import click


@click.command()
@click.argument("dir_path")
def deprecated_all(dir_path: str):
    summary = gather_loc_and_classes(dir_path)
    uninst = count_uninstantiated_loc(dir_path, summary["classes"])
    print("Total logical LOC:", summary["lloc"])
    print("Total abstract LOC:", summary["aloc"] + uninst)
    print(
        "Abstraction percentage:",
        f"{(summary['aloc'] + uninst) / summary['lloc'] * 100:.2f}%",
    )
