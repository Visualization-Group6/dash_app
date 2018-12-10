from dash import Dash
import dash_html_components as html
import dash_ui as dui
import dash_core_components as dcc
from pages.menu_items import dropdownMenu, slider, checkboxes
from scripts import matrixVisualisation
from scripts import preProcessing
from app import app
from dash.dependencies import Input, Output, State
import json
import ast
import pickle
import mydcc

matrix_plot = matrixVisualisation.AdjacencyMatrix('profile_semantic_trafo_final.txt')
xrange_matrix_plot = matrix_plot.get_range()


def serve_layout():
    colorscales = ["Greys", "YlGnBu", "Greens", "YlOrRd", "Bluered", "RdBu", "Reds", "Blues", "Picnic", "Rainbow",
                   "Portland", "Jet", "Hot", "Blackbody", "Earth", "Electric", "Viridis", "Cividis"]
    interleaved = pickle.load(open(preProcessing.get_working_dir()+'profile_semantic_trafo_final.dat', 'rb'))
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
                                html.H6(children='Select colorscale: ', className='mid-text'),
                                dropdownMenu.draw('top-left-dropdown', colorscales),
                                html.H6(children='Select tools: ', className='mid-text'),
                                checkboxes.draw('top-left-checkbox', ['Kaas', 'Klant'])
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="seven columns",
                    children=[
                        #mydcc.Relayout(id="relayout-midgraph", aim='mid-graph-t'),
                        html.Div(
                            id='top-middle-container',
                            className='window',
                            style={
                                'height': 400,
                                'width': '100%',
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            children=html.Div(
                                className='plot-container',
                                style={
                                    'height': 400,
                                    'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                                },
                                children=dcc.Graph(
                                    id='mid-graph-t',
                                    figure=interleaved
                                )
                            )
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
                        mydcc.Relayout(id="relayout-adjacency", aim='adjacency_matrix'),
                        html.Div(
                          id='bottom-left-container',
                          className='window-small-bottom',
                          style={
                              'height': 200,
                              'width': '100%',
                              'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                          },
                          children=html.Div(
                              className='plot-container',
                              id='matrix_plot',
                              style={
                                  'height': 200,
                                  'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                              },
                              children=dcc.Graph(figure=matrix_plot.draw_plot(), id='adjacency_matrix')
                          )
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
                                slider.draw('time_slider', xrange_matrix_plot[0], xrange_matrix_plot[1], int(xrange_matrix_plot[1] / 10)),
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
    [Input('top-left-checkbox', 'values'), Input('del-selection', 'n_clicks')])
def update_output(*value):
    print(value)
    return ['You have selected "{}"'.format(value)]


@app.callback(
    Output('matrix_plot', 'children'),
    [Input('top-left-dropdown', 'value')])
def update_colorscale(colorscale):
    return dcc.Graph(figure=matrix_plot.draw_plot(colorscale), id='adjacency_matrix')


@app.callback(
    Output('time_slider', 'value'),
    [Input('matrix_plot', 'children')])
def update_silder(*args):
    return xrange_matrix_plot


#@app.callback(
#    Output('selected-data', 'children'),
#    [Input('mid-graph-t', 'selectedData')])
#def display_selected_data(selectedData):
#    try:
#       print(ast.literal_eval(json.dumps(selectedData, indent=2)))
#    except ValueError:
#        pass

#@app.callback(
#    Output('relayout-midgraph', 'layout'),
#    [Input('time_slider', 'value')])
#def adjust_xrange(slider_range):
#    return {'xaxis':dict(
#        range=slider_range
#    )}

@app.callback(
    Output('relayout-adjacency', 'layout'),
    [Input('time_slider', 'value')])
def adjust_xrange(slider_range):
    return {
        'xaxis': dict(
            range=slider_range),
        'yaxis':dict(
            range=slider_range)
    }