import os, sys
import pandas as pd

sys.path.append(os.path.expanduser("~/github/ddi.py/"))

from ddi.onrails.repos import merge_instruments, dor1, copy, convert_r2ddi
from ddi.onrails.repos.merge_instruments import read_tables


def main():
    copy.study()
    dor1.datasets()
    dor1.variables()
    convert_r2ddi.Parser("soep-base", version="v1").write_json()
    copy.bibtex()

if __name__ == "__main__":
    main()
