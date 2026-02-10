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

df = load_data()
###IMPORTANT FOR THE CACHING PART
street_name = st.text_input("Filter by street name", "", key='street_name', on_change=st.write(f"User \
                            has filtered by street"))

if street_name:
    df.dropna(subset=["adresse_nom_voie"], inplace=True)
    df = df[df["adresse_nom_voie"].str.contains(street_name, case=False)]

type_local = st.selectbox("type_local:", ['Dépendance', 'Appartement', 'Local industriel. commercial ou assimilé', 'Maison'])

df = df[df['type_local'] == type_local]

st.dataframe(df)

st.write(f"""Number of places: {df.shape[0]} 
         Average price: {df['valeur_fonciere'].mean(axis=0)}""")

st.write(f"Number of places: {df.shape[0]} \nAverage price: {df['valeur_fonciere'].mean(axis=0)}")import pandas as pd
import streamlit as st


st.title("Real Estate individual properties info")

st.header("Selec a property and get the information you need")
st.write("Streamlit app to display real estate information in **Paris**")



@st.cache_data
def load_data():
    FILE = (
        "https://files.data.gouv.fr/geo-dvf/latest/csv/2022/"
        "departements/75.csv.gz"
    )
    return pd.read_csv(FILE, compression="gzip", low_memory=False)

df = load_data()
###IMPORTANT FOR THE CACHING PART
street_name = st.text_input("Filter by street name", "", key='street_name', on_change=st.write(f"User \
                            has filtered by street"))

if street_name:
    df.dropna(subset=["adresse_nom_voie"], inplace=True)
    df = df[df["adresse_nom_voie"].str.contains(street_name, case=False)]

type_local = st.selectbox("type_local:", ['Dépendance', 'Appartement', 'Local industriel. commercial ou assimilé', 'Maison'])

if type_local:
    df = df[df['type_local'] == type_local]

st.dataframe(df)

st.write(f"""Number of places: {df.shape[0]} 
         Average price: {df['valeur_fonciere'].mean(axis=0)}""")

st.write(f"Number of places: {df.shape[0]} \nAverage price: {df['valeur_fonciere'].mean(axis=0)}")




#on_change = is something you want streamlit to do when the button/tickbox/... is changed by the user

#Widgets which support the on_click event:
#st.button
#st.download_button
#st.form_submit_button