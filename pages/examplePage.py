import dash_html_components as html
import dash_core_components as dcc


def serve_menu():
    return(
        html.Div([
            html.A(children="Home page", className="button button-primary", href="/"),
            html.A(children="Data-sets page", className="button button-primary", href="/pages/showDatasetsPage")
            ]))


def serve_layout():
    return(html.Div(className='container', children=[
        serve_menu(),
        html.Section([
            html.H4("This is a title"),
            html.Div("This is text"),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            )
            ])
        ])
    )
