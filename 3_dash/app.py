"""
app.py
~~~~~~

First example to illustrate how to create a Dash app.
The use case is to display real estate prices in Paris.
"""

from dash import Dash, html, dash_table, dcc

from common import prepare_data

# Like in Streamlit, you can code any python logic here
# For example, we can load the data from the French government's
# Open Data Portal
FILE = (
    "https://files.data.gouv.fr/geo-dvf/latest/csv/2022/"
    "departements/75.csv.gz"
)
df = prepare_data(FILE)

# Now we can create the Dash app
app = Dash(__name__)

# The layout object is a tree of the components
# that make up the app's user interface
app.layout = html.Div([
    html.H1("Real estate prices in France"),
    html.P(children=[
        "Dash app to display real estate prices in Paris. ",
        "The data is available on the French government's ",
        dcc.Link(
            "Open Data Portal",
            href="https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres-geolocalisees/"
            )
    ]),
    html.H2("Raw data"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
],
className="app-shell")


# The main function should call the run method
def main():
    """Run the Dash app."""
    app.run(debug=False)


if __name__ == '__main__':
    main()
