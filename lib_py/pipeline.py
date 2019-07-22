# -*- coding: utf-8 -*-

""" Preprocessing pipeline for soep-base """

import pathlib

import pandas as pd
from convert_r2ddi import Parser as XmlParser

from helpers import add_columns, extract_unique_values, link_to, preprocess

STUDY = "soep-base"
VERSION = "v1"

INPUT_DIRECTORY = pathlib.Path("metadata")
LINK_TO_INPUT_DIRECTORY = pathlib.Path("..").joinpath(INPUT_DIRECTORY)
OUTPUT_DIRECTORY = pathlib.Path("ddionrails")


def preprocess_datasets() -> None:
    """ Preprocess datasets
        -------------------

        read from: metadata/datasets.csv

        add new columns:
            - label
            - label_de
            - description
            - description_de

        select subset of columns in specific order:
            - study
            - name
            - label
            - label_de
            - description
            - description_de
            - analysis_unit
            - conceptual_dataset
            - period

        write to: ddionrails/datasets.csv
    """

    NEW_COLUMNS = ["label", "label_de", "description", "description_de"]
    WANTED_COLUMNS = [
        "study",
        "name",
        "label",
        "label_de",
        "description",
        "description_de",
        "analysis_unit",
        "conceptual_dataset",
        "period",
    ]
    preprocess(
        in_filename=INPUT_DIRECTORY.joinpath("datasets.csv"),
        out_filename=OUTPUT_DIRECTORY.joinpath("datasets.csv"),
        wanted_columns=WANTED_COLUMNS,
        new_columns=NEW_COLUMNS,
    )


def run():
    # create symlinks
    link_to(
        LINK_TO_INPUT_DIRECTORY.joinpath("study.md"),
        OUTPUT_DIRECTORY.joinpath("study.md"),
    )
    link_to(
        LINK_TO_INPUT_DIRECTORY.joinpath("bibtex.bib"),
        OUTPUT_DIRECTORY.joinpath("bibtex.bib"),
    )
    link_to(
        LINK_TO_INPUT_DIRECTORY.joinpath("variables.csv"),
        OUTPUT_DIRECTORY.joinpath("variables.csv"),
    )

    # extract related objects from datasets
    datasets = pd.read_csv(INPUT_DIRECTORY.joinpath("datasets.csv"))
    analysis_units = extract_unique_values(datasets, "analysis_unit")
    analysis_units.insert(loc=0, column="study", value=STUDY)

    conceptual_datasets = extract_unique_values(datasets, "conceptual_dataset")
    conceptual_datasets.insert(loc=0, column="study", value=STUDY)

    periods = extract_unique_values(datasets, "period")
    periods.insert(loc=0, column="study", value=STUDY)

    # write to disk
    analysis_units.to_csv(OUTPUT_DIRECTORY.joinpath("analysis_units.csv"), index=False)
    conceptual_datasets.to_csv(
        OUTPUT_DIRECTORY.joinpath("conceptual_datasets.csv"), index=False
    )
    periods.to_csv(OUTPUT_DIRECTORY.joinpath("periods.csv"), index=False)

    # extract related objects from variables
    variables = pd.read_csv(INPUT_DIRECTORY.joinpath("variables.csv"))
    concepts = extract_unique_values(variables, "concept")
    concepts.insert(loc=len(concepts.columns), column="topic", value=None)
    concepts.to_csv(OUTPUT_DIRECTORY.joinpath("concepts.csv"), index=False)

    # preprocessing
    preprocess_datasets()
    XmlParser(STUDY, version=VERSION).write_json()


if __name__ == "__main__":
    run()
