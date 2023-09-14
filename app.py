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
                html.H1(children='ACP in Washington', className='header-title'),
                html.P(
                    children='How is ACP adoption going in Washington?',
                    className='header-description'
                ),
            ],
            className='header'
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children='County', className='menu-title'),
                        dcc.Dropdown(
                            id='county-filter',
                            options=[
                                {'label': county.title(), 'value': county}
                                for county in counties
                            ],
                            value='ADAMS COUNTY',
                            searchable=True,
                            clearable=False,
                            className='dropdown'
                        ),
                    ],
                )
            ],
            className='menu'
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(
                        id='subscriber-chart',
                        config={'displayModeBar': False}
                    ),
                    className='card'
                )
            ],
            className='wrapper'
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
        ],
        'layout': {
            'title': {'text': ''}
        }
    }
    return subscriber_chart_figure

if __name__ == '__main__':
    app.run_server(debug=True)