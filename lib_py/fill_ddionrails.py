from ddi.onrails.repos import convert_r2ddi, copy, dor1


def main():
    copy.study()
    dor1.datasets()
    dor1.variables()
    convert_r2ddi.Parser("soep-base", version="v1").write_json()
    copy.bibtex()


if __name__ == "__main__":
    main()
