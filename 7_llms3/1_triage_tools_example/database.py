"""
Functions to manage the database of the triage tool example.
The database is a CSV file that is read and updated by the user
or the anent.
"""

import numpy as np
import pandas as pd
import streamlit as st


DB_COLUMNS = [
    "age", "temperature", "reason_visit", "tests_performed", "diagnostic"
]


def clean_tests(x):
    """
    Clean the tests_performed string
    (necessary to display the information correctly
    according to pandas and streamlit way of working).

    Parameters
    ----------
    x: str
        The string to clean
    Returns
    -------
    str
        The cleaned string
    """
    if not isinstance(x, str):
        return x
    return x.replace("[", "")\
            .replace("]", "")\
            .replace("\"", "")\
            .replace("'", "")


def get_database():
    """
    Read database from a file or create an empty one.

    Returns
    -------
    pd.DataFrame
        The database as a pandas DataFrame
    """
    try:
        df = pd.read_csv("db.csv")
        df['tests_performed'] = df['tests_performed'].apply(clean_tests)
    except FileNotFoundError:
        # Not elegant, improve later
        st.warning("DB file not found, creating new DB.")
        df = pd.DataFrame(
            columns=DB_COLUMNS,
            )
        df = pd.DataFrame({
            'age': pd.Series([], dtype='int'),
            'temperature': pd.Series([], dtype='int'),
            'reason_visit': pd.Series([], dtype='str'),
            'tests_performed': pd.Series([], dtype='str'),
            'diagnosis': pd.Series([], dtype='str')
            })

    return df


def add_record(age="N/A", temperature="N/A", reason_visit="N/A",
               tests_performed="N/A", diagnosis="N/A"):
    """
    Add a record to the database.

    Parameters
    ----------
    age: int
        The age of the patient
    temperature: float
        The temperature of the patient
    reason_visit: str
        The reason for the patient's visit
    tests_performed: str
        The tests performed on the patient, as a comma-separated string
    diagnosis: str
        The diagnosis of the patient
        """
    df = get_database()
    new_record = {
        'age': age,
        'temperature': temperature,
        'reason_visit': reason_visit,
        'tests_performed': tests_performed,
        'diagnosis': diagnosis
    }
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    df.to_csv("db.csv", index=False)


def add_sample_record():
    """Add a sample record to the database."""

    REASONS = [
        "Fever",
        "Cough",
        "Headache",
        "Sore throat",
        "Fatigue",
        "Shortness of breath",
        "Loss of taste or smell",
        "Muscle or body aches",
        "Nausea or vomiting",
        ]

    TESTS = [
        "PCR test",
        "Antigen test",
        "Blood test",
        "X-ray",
        "CT scan",
        "Urine test",
    ]

    age = np.random.randint(30, 80)
    temperature = round(np.random.uniform(36.5, 40.0), 1)
    # select one or two random reasons
    reason_visit = ", ".join(
        np.random.choice(REASONS, size=np.random.randint(1, 3), replace=False)
        )
    # select one or two random tests
    tests_performed = ", ".join(
        np.random.choice(TESTS, size=np.random.randint(1, 3), replace=False)
        )

    add_record(
        age=age,
        temperature=temperature,
        reason_visit=reason_visit,
        tests_performed=tests_performed,
        diagnosis="Pending"
    )


def release_patient():
    """Release the first patient in the queue."""
    df = get_database()
    if len(df) > 0:
        df = df.iloc[1:]
        df.to_csv("db.csv", index=False)
