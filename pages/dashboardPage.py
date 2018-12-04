from dash import Dash
import dash_html_components as html
import dash_ui as dui
import dash_core_components as dcc
from pages.menu_items import dropdownMenu, slider, checkboxes
from scripts import matrixVisualisation
from app import app
from dash.dependencies import Input, Output, State
import json
import ast


def serve_layout():
    adjacency_matrix = matrixVisualisation.make_scatterplot('profile_semantic_trafo_final.txt')
    graph_1 = dcc.Graph(
        id='mid-graph-t',
        figure={
            'data': [{
                'x': [1, 2, 50],
                'y': [3, 1, 2],
                'type': 'bar'
            }],
            'layout': {
                'height': 200,
                'margin': {
                    'l': 50, 'b': 50, 't': 50, 'r': 50
                },
                'xaxis': dict(
                    tickmode='linear',
                    ticks='outside',
                    tick0=0,
                    dtick=5,
                    ticklen=8,
                    tickwidth=4,
                    tickcolor='#000'
                )
            }
        }
    )
    return([
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="three columns",
                    children=[
                        html.Div(
                            id='top-left-container',
                            className='window',
                            style={
                                'height': 400,
                                'width': '100%',
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            children=[
                                html.H6(children='Select dataset: ', className='mid-text'),
                                dropdownMenu.draw('top-left-dropdown', ['Option 1', 'Option 2']),
                                html.H6(children='Select tools: ', className='mid-text'),
                                checkboxes.draw('top-left-checkbox', ['Kaas', 'Klant'])
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="seven columns",
                    children=[
                        html.Div(
                            id='top-middle-container',
                            className='window',
                            style={
                                'height': 400,
                                'width': '100%',
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            children=graph_1
                        )
                    ]
                ),
                html.Div(
                    className="two columns",
                    children=[html.Div(
                        id='top-right-container',
                        className='window',
                        style={
                            'height': 400,
                            'width': '100%',
                            'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                        },
                        children=[
                            html.Div(id='selected-data')
                        ]
                    )]
                )
            ]),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="three columns",
                    children=[
                        html.Div(
                          id='bottom-left-container',
                          className='window-small-bottom',
                          style={
                              'height': 200,
                              'width': '100%',
                              'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                          },
                          children=dcc.Graph(figure=adjacency_matrix)
                        )
                    ]
                  ),
                html.Div(
                    className="seven columns",
                    children=[
                        html.Div(
                            id='bottom-middle-container',
                            className='window-mid-bottom',
                            style={
                                'height': 200,
                                'width': '100%',
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            children=[
                                html.H6("Select x-range: ", className='mid-text'),
                                slider.draw('time_slider', 0, 50, 5),
                                html.Section(className='mid-text', id='output-text')
                            ])
                    ]
                  ),
                html.Div(
                    className="two columns",
                    children=[
                        html.Div(
                            id='bottom-right-container',
                            className='window-small-bottom',
                            style={
                                'height': 200,
                                'width': '100%',
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            children=[
                                html.Button('Run action', id='del-selection', className="button-option")
                            ]
                        )
                    ]
                  )
              ]
          )
    ])


@app.callback(
    Output('output-text', 'children'),
    [Input('top-left-dropdown', 'value'), Input('top-left-checkbox', 'values'), Input('del-selection', 'n_clicks')])
def update_output(*value):
    print(value)
    return ['You have selected "{}"'.format(value)]


@app.callback(
    Output('selected-data', 'children'),
    [Input('mid-graph-t', 'selectedData')])
def display_selected_data(selectedData):
    try:
        print(ast.literal_eval(json.dumps(selectedData, indent=2)))
    except ValueError:
        pass
