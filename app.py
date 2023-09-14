import os
import pandas as pd
from dash import Dash, Input, Output, dcc, html

file = os.path.join('data', 'waAcp.parquet')

acpData = (
    pd.read_parquet(file)
    .sort_values(by="Data Month")
)

counties = acpData['County Name'].sort_values().unique()

# Join Max reciepients into data!!

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Washington ACP Adoption"
application = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children = [
                html.Img(src='assets/WSU-EXT-lockup-horz-rgb-12in.gif', className='header-logo'),
                html.H1(children='ACP in Washington'),
                html.P(
                    children='How is ACP adoption going in Washington?'
                ),
            ],
            className='header'
        ),
        html.Div(
            children=[
                html.Div(children='County'),
                dcc.Dropdown(
                    id='county-filter',
                    options=[
                        {'label': county.title(), 'value': county}
                        for county in counties
                    ],
                    value='ADAMS COUNTY',
                    searchable=True,
                    clearable=False,
                )
            ]
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id='subscriber-chart',
                    config={'displayModeBar': False}
                )
            ]
        )
    ]
)

@app.callback(
    Output('subscriber-chart', 'figure'),
    Input('county-filter', 'value'),
)
def update_charts(county):
    print(county)
    filteredAcpData = acpData.query(
        "`County Name` == @county"
    )
    subscriber_chart_figure = {
        'data': [
            {
                'x': filteredAcpData['Data Month'],
                'y': filteredAcpData['Total Subscribers'],
                'type': 'lines',
                'hovertemplate': '%{y} Subscribers<extra></extra>'
            }
        ]
    }
    return subscriber_chart_figure

if __name__ == '__main__':
    app.run_server(debug=True)