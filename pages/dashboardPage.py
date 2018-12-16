from dash import Dash
import dash_html_components as html
import dash_ui as dui
import dash_core_components as dcc
from pages.menu_items import dropdownMenu, rangeSlider, checkboxes, slider
from scripts import matrixVisualisation
from scripts import preProcessing
from app import app
from dash.dependencies import Input, Output, State
from scripts import layoutDiagram
import json
import ast
import pickle
import mydcc

plots = ['Radial', 'Fruchterman-Reingold', 'Interleaved dynamic network']
matrix_plot = matrixVisualisation.AdjacencyMatrix('profile_semantic_trafo_final.txt')
xrange_matrix_plot = matrix_plot.get_range()
weightrange_matrix_plot = matrix_plot.get_weight()
timerange_matrix_plot = matrix_plot.get_time()
current_plot = None
timerangeG, to_ploG, weightrangeG, noderangeG, dijkstrafromG, dijkstratoG = None, None, None, None, None, None
node_link_plot = layoutDiagram.NodeLink("profile_semantic_trafo_final.txt")


def serve_layout():
    colorscales = ["Greys", "YlGnBu", "Greens", "YlOrRd", "Bluered", "RdBu", "Reds", "Blues", "Picnic", "Rainbow",
                   "Portland", "Jet", "Hot", "Blackbody", "Earth", "Electric", "Viridis", "Cividis"]
    #interleaved = pickle.load(open(preProcessing.get_working_dir()+'profile_semantic_trafo_final.dat', 'rb'))
    return([
        html.Div(
            className="row",
            style={
              'height':500
            },
            children=[
                html.Div(
                    className="three columns",
                    children=[
                        html.Div(
                            id='top-left-container',
                            className='window',
                            style={
                                'height': 500,
                                'width': '100%',
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            children=[
                                html.H6(children='Select type of plot: ', className='mid-text'),
                                dropdownMenu.draw('plot-selector', plots),
                                html.H6(children='Select colorscale: ', className='mid-text'),
                                dropdownMenu.draw('top-left-dropdown', colorscales),
                                #html.H6(children='Select tools: ', className='mid-text'),
                                #checkboxes.draw('top-left-checkbox', ['Kaas', 'Klant']),
                                html.H6(children='Draw shortest path (from, to): ', className='mid-text'),
                                html.Div(className='textbox-small', children=[
                                    dcc.Input(id='shortestfrom', type='text', value=None, style={'display':'inline-table','width':'50%'}),
                                    dcc.Input(id='shortestto', type='text', value=None, style={'display':'inline-table','width':'50%'})])
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
                                'height': 500,
                                'width': '100%',
                            },
                            children=html.Div(
                                className='plot-container',
                                id='midplot',
                                style={
                                    'height': 500,
                                }
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
                            'height': 500,
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
            style={
                'height': 300
            },
            children=[
                html.Div(
                    className="three columns",
                    children=[
                        html.Div(
                          id='bottom-left-container',
                          className='window-small-bottom',
                          style={
                              'width': '100%',
                              'height':300,
                              'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                          },
                          children=html.Div(
                              className='plot-container',
                              id='matrix_plot',
                              style={
                                  'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0},
                              },
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
                                'width': '100%',
                                'height': 300,
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            children=[
                                    html.H6("Select node-range: ", className='mid-text'),
                                    rangeSlider.draw('node_slider', xrange_matrix_plot[0], xrange_matrix_plot[1],
                                                     int(xrange_matrix_plot[1] / 10), visible=False),
                                    html.H6("Select log weight-range: ", className='mid-text'),
                                    rangeSlider.draw('weight_slider', weightrange_matrix_plot[0], weightrange_matrix_plot[1],
                                                     int(weightrange_matrix_plot[1] / 10), visible=False),
                                    html.H6("Select time-range: ", className='mid-text'),
                                    rangeSlider.draw('time_slider', timerange_matrix_plot[0], timerange_matrix_plot[1],
                                                     int(timerange_matrix_plot[1] / 10), visible=False),
                                    html.Section(className='mid-text', id='output-text')
                            ]
                        )
                    ]
                  ),
                html.Div(
                    className="two columns",
                    children=[
                        html.Div(
                            id='bottom-right-container',
                            className='window-small-bottom',
                            style={
                                'height':300,
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            },
                            #children=[
                            #    html.Button('Run action', id='del-selection', className="button-option")
                            #]
                        )
                    ]
                  )
              ]
          )
    ])


#@app.callback(
#    Output('output-text', 'children'),
#    [Input('top-left-checkbox', 'values'), Input('del-selection', 'n_clicks')])
#def update_output(*value):
#    print("-----update_output----")
#    return ['You have selected "{}"'.format(value)]

@app.callback(
    Output('node_slider', 'value'),
    [Input('matrix_plot', 'children')])
def update_silder(*args):
    print("-----update_slider----")
    return xrange_matrix_plot

@app.callback(
    Output('matrix_plot', 'children'),
    [Input('top-left-dropdown', 'value'), Input('weight_slider', 'value'), Input('time_slider', 'value')])
def update_colorscale(colorscale, weight, timerange):
    print("-----update_colorscale----")
    global current_plot
    if current_plot:
        if type(timerange) != list:
            timerange = [timerange, timerange+1]
        return [mydcc.Relayout(id="relayout-adjacency", aim='adjacency_matrix'),
                dcc.Graph(figure=matrix_plot.draw_plot(colorscale, weightrange=weight,
                                                       timerange=timerange), id='adjacency_matrix')]
    else:
        return None


@app.callback(
    Output('midplot', 'children'),
    [Input('time_slider', 'value'), Input('plot-selector', 'value'), Input('weight_slider', 'value'),
     Input('node_slider', 'value'), Input('shortestfrom', 'n_submit'), Input('shortestto', 'n_submit')],
    [State('shortestfrom', 'value'),
     State('shortestto', 'value')])
def update_midplot(timerange, to_plot, weightrange, noderange, n1, n2, dijkstafrom, dijkstrato):
    global timerangeG, to_ploG, weightrangeG, noderangeG, dijkstrafromG, dijkstratoG
    run = False
    if timerangeG != timerange:
        timerangeG = timerange
        run = True
    if to_ploG != to_plot:
        to_ploG = to_plot
        run = True
    if weightrangeG != weightrange:
        weightrangeG = weightrange
        run = True
    if noderangeG != noderange:
        noderangeG = noderange
        run = True
    if dijkstrafromG != dijkstafrom:
        dijkstrafromG = dijkstafrom
        run = True
    if dijkstratoG != dijkstrato:
        dijkstratoG = dijkstrato
        run = True
    if run:
        print("-----update_midplot----")
        global current_plot
        current_plot = to_plot
        if to_plot == 'Radial' or to_plot == 'Fruchterman-Reingold':
            return dcc.Graph(id='mid-graph-t',
                             style={'margin':'auto'},
            figure=node_link_plot.draw_plot(timerange, to_plot, weightrange=weightrange, noderange=noderange, dijkstrafrom=dijkstafrom, dijkstrato=dijkstrato))
        if to_plot == 'Interleaved dynamic network':
            pass






@app.callback(
    Output('bottom-middle-container', 'children'),
    [Input('plot-selector', 'value')]
)
def update_plot_tools(plot):
    print("-----update_plot_tools----")
    global current_plot
    current_plot = plot
    if plot == 'Radial' or plot == 'Fruchterman-Reingold':
        return [
            html.H6("Select node-range: ", className='mid-text'),
            rangeSlider.draw('node_slider', xrange_matrix_plot[0], xrange_matrix_plot[1],
                             int(xrange_matrix_plot[1] / 10)),
            html.H6("Select log weight-range: ", className='mid-text'),
            rangeSlider.draw('weight_slider', weightrange_matrix_plot[0], weightrange_matrix_plot[1],
                             int(weightrange_matrix_plot[1] / 10)),
            html.H6("Select time-range: ", className='mid-text'),
            slider.draw('time_slider', timerange_matrix_plot[0], timerange_matrix_plot[1],
                             int(timerange_matrix_plot[1] / 10)),
            html.Section(className='mid-text', id='output-text')
        ]
    else:
        return [
                html.H6("Select node-range: ", className='mid-text'),
                rangeSlider.draw('node_slider', xrange_matrix_plot[0], xrange_matrix_plot[1],
                                 int(xrange_matrix_plot[1] / 10), visible=False),
                html.H6("Select log weight-range: ", className='mid-text'),
                rangeSlider.draw('weight_slider', weightrange_matrix_plot[0], weightrange_matrix_plot[1],
                                 int(weightrange_matrix_plot[1] / 10), visible=False),
                html.H6("Select time-range: ", className='mid-text'),
                rangeSlider.draw('time_slider', timerange_matrix_plot[0], timerange_matrix_plot[1],
                                 int(timerange_matrix_plot[1] / 10), visible=False),
                html.Section(className='mid-text', id='output-text')
        ]



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
#    [Input('node_slider', 'value')])
#def adjust_xrange(rangeSlider_range):
#    return {'xaxis':dict(
#        range=rangeSlider_range
#    )}

@app.callback(
    Output('relayout-adjacency', 'layout'),
    [Input('node_slider', 'value')])
def adjust_xrange(rangeSlider_range):
    print("-----adjust_xrange----")
    return {
        'xaxis': dict(
            range=rangeSlider_range),
        'yaxis':dict(
            range=rangeSlider_range)
    }
