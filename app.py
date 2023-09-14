import os
import pandas as pd
from dash import Dash, dcc, html

file = os.path.join('data', 'waAcp.parquet')

acpData = (
    pd.read_parquet(file)
    .query("State == 'WA' and `County Name` == 'ADAMS COUNTY'")
    .sort_values(by="Data Month")
)

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
        dcc.Graph(
            figure={
                'data': [
                    {
                        'x': acpData['Data Month'],
                        'y': acpData['Total Subscribers'],
                        'type': 'lines',
                        'name': 'ACP Subscribers (Real data)'
                    },
                    {
                        'x': [acpData['Data Month'].min(), acpData['Data Month'].max()],
                        'y': [800, 800],
                        'type': 'lines',
                        'name': 'Possible Subscribers (Fake data)',
                    },
                ],
                'layout': {'title': 'ACP Subscribers in Adams County, Washington'},
            },
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)