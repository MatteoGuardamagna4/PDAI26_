import pandas as pd
import streamlit as st

st.title("Real Estate individual properties info")

st.header("Selec a property and get the information you need")
st.write("Streamlit app to display real estate information in **Paris**")


type_local = st.selectbox("Type local:", ['Dépendance', 'Appartement', 'Local industriel. commercial ou assimilé', 'Maison'])

FILE = (
    f"https://files.data.gouv.fr/geo-dvf/latest/csv/"
    "departements/75/{type_local}.csv.gz"
)
df = pd.read_csv(FILE, compression="gzip", low_memory=False)



street_name = st.text_input("Filter by street name", "")

if street_name:
    df.dropna(subset=["adresse_nom_voie"], inplace=True)
    df = df[df["adresse_nom_voie"].str.contains(street_name, case=False)]

st.dataframe(df)