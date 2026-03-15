import click

from pymetrica.metric_calculators import (
    aloc,
    cc,
    hv,
    li,
    mc,
)

from .codebase_parser import base_stats
from .run_all import run_all
from .status import status


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None: ...


main.add_command(status)
main.add_command(run_all)
main.add_command(base_stats)
main.add_command(aloc)
main.add_command(cc)
main.add_command(hv)
main.add_command(mc)
main.add_command(li)

if __name__ == "__main__":
    main()
