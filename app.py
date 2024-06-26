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
        ),
        html.Div(
            children=[
                html.P(
                    children=[
                        "This data was pulled from the ",
                        html.A(
                            children = 'USAC ACP Adoption Dataset',
                            href = "https://www.usac.org/about/affordable-connectivity-program/acp-enrollment-and-claims-tracker/"
                        ),
                    ],
                ),
                html.P(
                    children=[
                        "Data used in these visualizations can be found here: ",
                        html.A(
                            children = 'waACP.xlsx',
                            href = "assets/waAcp.xlsx"
                        ),
                    ],
                ),
                html.P(
                    children=[
                        "Maximum ESH Eligibility data is from the ",
                        html.A(
                            children="Education Super Highway ACP Dataset",
                            href='https://www.educationsuperhighway.org/no-home-left-offline/acp-data/#dashboard'
                        ),
                        # Nick! Don't delete the space it is necessary for formatting! 
                        " Methodology: ",
                        html.A(
                            children='here',
                            href='https://www.educationsuperhighway.org/wp-content/uploads/NHLO-Report-2022_Data-Methodology.pdf'
                        )
                    ]
                ),
                html.P(
                    children=[
                        "WSBO Estimates provided by the Washington State Broadband Office ",
                        "via email on 09-20-2023."
                        
                    ]
                ),
                html.P(
                    children = [
                        "Adoption data was at county level already, the eligibility data was ",
                        "at city level and I aggregated them to county via crosswalk."
                    ]
                )
            ],
            className='methodology'
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
    # print(filteredAcpData.info())
    maxValue = max([filteredAcpData['Total Subscribers'].max(), filteredAcpData['Eligible Households'].max(), filteredAcpData['WSBO_Eligible'].max()])
    subscriber_chart_figure = {
        'data': [
            {
                'x': filteredAcpData['Data Month'],
                'y': filteredAcpData['Total Subscribers'],
                'type': 'lines',
                'hovertemplate': '%{y} Subscribers<extra></extra>',
                'name': 'Subscribed'
            },
            {
                'x': filteredAcpData['Data Month'],
                'y': filteredAcpData['Eligible Households'],
                'type': 'lines',
                'hovertemplate': '%{y} ESH Estimate<extra></extra>',
                'name': 'ESH Eligible'
            },
            {
                'x': filteredAcpData['Data Month'],
                'y': filteredAcpData['WSBO_Eligible'],
                'type': 'lines',
                'hovertemplate': '%{y} WSBO Estimate<extra></extra>',
                'name': 'WSBO Eligible'
            }
        ],
        'layout': {
            'title': {'text': ''},
            'legend': {
                'yanchor': 'top',
                'y': 0.85,
                'xanchor': 'left',
                'x': 0.01,
                'bordercolor': 'Black',
                'borderwidth': 2
            },
            'colorway': ["#0072b2", "#d55e00", "#009e73"],
            'yaxis': {'range': [1, maxValue*1.1]}
        }
    }
    return subscriber_chart_figure

if __name__ == '__main__':
    app.run(debug=True)