"""
app3.py
~~~~~~

Third example to illustrate how to
create a Dash app.
The use case is to display real estate prices in Paris.
This example illustrates how to interact with a plot (the map),
e.g. to click on a certain property, and how to retrieve
information about the selected property.
"""

from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

from common import prepare_data, get_map


# Function to load data from French government's Open Data Portal
def get_file(year):
    """Return the URL to the CSV file for the given year."""
    return (f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/"
            "departements/75.csv.gz")


# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    dcc.Dropdown(
        id='year-dd',
        className="dd1",
        options=['2020', '2021', '2022', '2023'],
        value='2022'
    ),
    html.Div(id='table-container'),
    # In this example, we add a placeholder for the info
    # about the selected property
    # We also illustrate how to use the dbc.Row and dbc.Col
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='map')
            ], width=9),
            dbc.Col([
                html.Div(id='info')
            ], width=3)
            ])  # End row
    ])  # End container
],
className="app-shell")


# Callback for updating the table
@callback(
    Output('table-container', 'children'),
    Input('year-dd', 'value')
)
def update_output(value):
    """Update the table with the data for the selected year."""
    fname = get_file(value)
    df = prepare_data(fname)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )


# Callback for updating the map
@callback(
    Output('map', 'figure'),
    Input('year-dd', 'value')
)
def update_map(value):
    """Update the map with the data for the selected year."""
    fname = get_file(value)
    df = prepare_data(fname)
    return get_map(df)


def format_property_data(click_data):
    """Format the click data for display."""
    if click_data is None:
        return "Click on the map to display information"

    customdata = click_data['points'][0]['customdata']
    elements = customdata.split("\n")

    # Return as a list of HTML components
    return [html.P(f"{elem}") for elem in elements]


# Callback for updating the info
@callback(
    Output('info', 'children'),
    Input('map', 'clickData')
)
def display_click_data(click_data):
    """Update the information with the selected property."""
    return format_property_data(click_data)


# The main function should call the run method
def main():
    """Run the Dash app."""
    app.run(debug=False)


if __name__ == '__main__':
    main()
