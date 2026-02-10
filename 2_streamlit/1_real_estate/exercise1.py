import pandas as pd
import streamlit as st

st.title("Real Estate individual properties info")

st.header("Selec a property and get the information you need")
st.write("Streamlit app to display real estate information in **Paris**")



FILE = (
    f"https://files.data.gouv.fr/geo-dvf/latest/csv/2022/"
    "departements/75.csv.gz"
)
df = pd.read_csv(FILE, compression="gzip", low_memory=False)

street_name = st.text_input("Filter by street name", "")

if street_name:
    df.dropna(subset=["adresse_nom_voie"], inplace=True)
    df = df[df["adresse_nom_voie"].str.contains(street_name, case=False)]

type_local = st.selectbox("type_local:", ['Dépendance', 'Appartement', 'Local industriel. commercial ou assimilé', 'Maison'])

df = df[df['type_local'] == type_local]

st.dataframe(df)

st.write(f"""Number of places: {df.shape[0]} 
         Average price: {df['valeur_fonciere'].mean(axis=0)}""")

st.write(f"Number of places: {df.shape[0]} \nAverage price: {df['valeur_fonciere'].mean(axis=0)}")