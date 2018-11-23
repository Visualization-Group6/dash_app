import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
from app import app


def serve_layout():
    dirs = list(os.listdir(os.getcwd()+"/datasets"))
    return(
        html.Div([
            html.H3('App 1'),
            dcc.Dropdown(
                id='app-1-dropdown',
                options=[{'label': i, 'value': i} for i in dirs]
            ),
            html.Div(id='app-1-display-value'),
            dcc.Link('Go to App 2', href='/apps/app2')
        ])
    )


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
