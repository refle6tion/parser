from parser2 import parser
from parser_checks import run_checks
from pathlib import Path
from pprint import pprint

if __name__ == "__main__":
    # ponytail: one cheap smoke check before parsing the real input.
    run_checks(verbose=True)
    p = parser()
    result = p.parser(Path("diff.txt").read_text())
    pprint(result, width=120)
