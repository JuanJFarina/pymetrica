import argparse
from .first_pass import gather_loc_and_classes
from .second_pass import count_uninstantiated_loc


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python code for LOC, abstraction, and uninstantiated class LOC."
    )
    parser.add_argument("dir_path", type=str, help="Path to analyze")
    args = parser.parse_args()

    summary = gather_loc_and_classes(args.dir_path)
    uninst = count_uninstantiated_loc(args.dir_path, summary["classes"])
    print("Total logical LOC:", summary["lloc"])
    print("Total abstract LOC:", summary["aloc"] + uninst)
    print(
        "Abstraction percentage:",
        f"{(summary['aloc'] + uninst) / summary['lloc'] * 100:.2f}%",
    )
