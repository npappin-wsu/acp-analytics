import os
import pandas as pd
from dash import Dash, dcc, html

file = os.path.join('data', 'waAcp.parquet')

data = (
    pd.read_parquet(file)
    .query("State == 'WA' and `County Name` == 'ADAMS COUNTY'")
    .sort_values(by="Data Month")
)

# Join Max reciepients into data!!

app = Dash(__name__)
application = app.server

app.layout = html.Div(
    children=[
        html.H1(children='Washington ACP Analytics'),
        html.P(
            children='Review the adoption of ACP over time in Washington'
        ),
        dcc.Graph(
            figure={
                'data': [
                    {
                        'x': data['Data Month'],
                        'y': data['Total Subscribers'],
                        'type': 'lines',
                    },
                    {
                        'x': [data['Data Month'].min(), data['Data Month'].max()],
                        'y': [800, 800],
                        'type': 'lines',
                    },
                ],
                'layout': {'title': 'ACP Subscribers in Adams County, Washington'},
            },
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)