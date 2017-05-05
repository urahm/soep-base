import os, sys
import pandas as pd

sys.path.append(os.path.expanduser("~/github/ddi.py/"))

from ddi.onrails.repos import merge_instruments

def questions_from_generations():

    # Direct links

    questions_variables = pd.read_csv("metadata/logical_variables.csv")
    questions_variables.rename(columns={
        "study":"study_name",
        "dataset":"dataset_name",
        "variable":"variable_name",
        "questionnaire":"instrument_name",
        "question":"question_name"
    }, inplace=True)
    questions_variables = questions_variables[["study_name", "dataset_name",
        "variable_name", "instrument_name", "question_name"]]

    # Indirect links

    generations = pd.read_csv("metadata/generations.csv")
    logical_variables = pd.read_csv("metadata/logical_variables.csv")
    logical_variables = logical_variables[["dataset", "variable", "questionnaire", "question"]]
    x = generations.merge(
        logical_variables,
        how="left",
        left_on=("input_dataset", "input_variable"),
        right_on=("dataset", "variable"),
    )
    x = x[["output_study", "output_dataset", "output_variable", "questionnaire", "question"]]
    x.rename(columns={
        "output_study":"study_name",
        "output_dataset":"dataset_name",
        "output_variable":"variable_name",
        "questionnaire":"instrument_name",
        "question":"question_name",
    }, inplace=True)

    # Append

    questions_variables = questions_variables.append(x)
    questions_variables.dropna(axis=0, how="any", inplace=True)
    questions_variables.drop_duplicates(inplace=True)
    questions_variables.to_csv("ddionrails/questions_variables.csv", index=False)

def main():
    questions_from_generations()

if __name__ == "__main__":
    main()
