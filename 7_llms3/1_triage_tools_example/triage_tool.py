"""
Streamlit app that showcases use of Cohere tools in a simple
triage use case.
A simple tool-calling agent is implemented to process triage
reports and update a "database" (a CSV file) or release patients
from the queue.
This can be considered a "minimal agent" (chooses between tools
autonomously) but it's minimal as it does not make sequential
decision-making or iterative state tracking.
"""

import streamlit as st

from agent import TriageAgent
import database as db


DF_COLUMN_CONFIG = {
    "age": st.column_config.NumberColumn("Age"),
    "temperature": st.column_config.ProgressColumn(
        "Temperature", min_value=36.5, max_value=42.0, format="%.1f ºC",
        width="small"),
    "reason_visit": st.column_config.TextColumn("Reason"),
    "tests_performed": st.column_config.ListColumn("Tests", width="medium"),
    "diagnosis": st.column_config.TextColumn("Diagnosis")
}

@st.cache_resource
def init_agent():
    """Initialize the agent."""
    agent = TriageAgent()
    return agent


@st.dialog("Add patient manually")
def add_patient_manually(age, temperature, reason_visit, tests_performed, diagnosis):
    """Show a form to add a patient manually."""
    st.header("Add patient manually")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    temperature = st.number_input(
        "Temperature", min_value=35.0, max_value=42.0, value=36.5,
        step=0.1)
    reason_visit = st.text_input("Reason for visit")
    tests_performed = st.text_input("Tests performed")
    diagnosis = st.text_input("Diagnosis")

    if st.button("Add patient"):
        db.add_record(age, temperature, reason_visit, tests_performed, diagnosis)
        st.rerun()


def main():
    """Execute main program flow."""

    agent = init_agent()

    df = db.get_database()

    st.header("Example: Using LLMs to structure data")

    st.sidebar.markdown("""
    Enter the report with the known information about an incoming patient
    (age, temperature, symptoms, tests performed and diagnistics).
    
    Clicking on "Process" will process the report with an LLM, 
    create a structured record and add it to a "database".
    """
    )

    st.sidebar.header("Triage report")
    text = st.sidebar.text_area("Enter text:")
    if st.sidebar.button("Process"):
        response = agent.process_command(text)
        #with st.expander("LLM response"):
        #    st.json(response)
        if response.message.tool_calls:
            st.rerun()
        else:
            st.warning("Command unknown")

    if st.sidebar.button("Add sample record"):
        db.add_sample_record()
        st.rerun()

    if st.sidebar.button("Release patient"):
        db.release_patient()
        st.rerun()

    if st.sidebar.button("Add patient manually"):
        add_patient_manually(None, None, None, None, None)

    st.subheader("Patients in queue:")
    st.dataframe(df, column_config=DF_COLUMN_CONFIG)


if __name__ == "__main__":
    main()
