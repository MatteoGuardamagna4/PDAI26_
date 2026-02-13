"""
app2.py
~~~~~~

Second example to illustrate how to create a Dash app.
The use case is to display real estate prices in Paris.
In this example, we'll add a Dropdown to select the year,
and the callback function to update the table.
"""

from dash import Dash, html, dash_table, dcc, Input, Output, callback

from common import prepare_data


# Function to load data from French government's Open Data Portal
def get_file(year):
    """Return the URL to the CSV file for the given year."""
    return (f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/"
            "departements/75.csv.gz")


# Create the Dash app
app = Dash(__name__)

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
        options=['2020', '2021', '2022', '2023'],
        value='2022'
    ),
    # Now this is a placeholder for the table,
    # not the table itself
    # It will be populated by the callback function
    html.Div(id='table-container')

],
className="app-shell")


# Now this is the callback function that will update the table
# when the year is changed
#
# The callback decorator takes the Output and Input objects
# as arguments and returns a function that will be called
# when the input changes
#
# Output('table-container', 'children') specifies the value
# and component that will be updated
# (the 'children' of the 'table-container' div).
#
# Input('year-dd', 'value') specifies which value of which
# component will trigger the function.
# (the 'value' of the 'year-dd' dropdown).
#
# The return value of the function specifies what will be the
# new value of the output.
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


# The main function should call the run method
def main():
    """Run the Dash app."""
    app.run(debug=False)


if __name__ == '__main__':
    main()
