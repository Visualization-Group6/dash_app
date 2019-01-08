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
import time as t
import ast
import inspect
import os
import pickle
from scripts import interleavedPlot
import mydcc

timerangeG, to_ploG, weightrangeG, noderangeG, dijkstrafromG, dijkstratoG = None, None, None, None, None, None
node_link_plot = layoutDiagram.NodeLink("profile_semantic_trafo_final.txt")


class interactiveDashboard():
    current_plot = None
    current_dataset = None
    current_colorscale = None
    matrix_plot = None

    def __init__(self):
        self.colorscales = ["Greys", "YlGnBu", "Greens", "YlOrRd", "Bluered", "RdBu", "Reds", "Blues",
                            "Picnic", "Rainbow", "Portland", "Jet", "Hot", "Blackbody", "Earth", "Electric",
                            "Viridis", "Cividis"]
        self.plots = ['Radial', 'Fruchterman-Reingold', 'Interleaved dynamic network']
        self.datasets = os.listdir(preProcessing.get_working_dir())

    def get_matrix_plot_info(self):
        if self.current_dataset:
            self.matrix_plot = matrixVisualisation.AdjacencyMatrix(self.current_dataset)
            self.xrange_matrix_plot = self.matrix_plot.get_range()
            self.weightrange_matrix_plot = self.matrix_plot.get_weight()
            self.timerange_matrix_plot = self.matrix_plot.get_time()

    def top_left_menu(self):
        return html.Div(
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
                        html.H6(children='Select dataset: ', className='mid-text'),
                        dropdownMenu.draw('dataset-selector', self.datasets),
                        html.H6(children='Select type of plot: ', className='mid-text'),
                        dropdownMenu.draw('plot-selector', self.plots),
                        html.H6(children='Select colorscale: ', className='mid-text'),
                        dropdownMenu.draw('top-left-dropdown', self.colorscales),
                        html.H6(children='Draw shortest path (from, to): ', className='mid-text'),
                        html.Div(className='textbox-small', children=[
                            dcc.Input(id='shortestfrom', type='text', value=None,
                                      style={'display': 'inline-table', 'width': '50%'}),
                            dcc.Input(id='shortestto', type='text', value=None,
                                      style={'display': 'inline-table', 'width': '50%'})]),
                        # only here because callbacks need output:
                        html.Div(className='textbox-small', id='console_output')
                    ]
                )
            ]
        )

    def top_mid_container(self):
        return html.Div(
            className="seven columns",
            children=[
                # mydcc.Relayout(id="relayout-midgraph", aim='mid-graph-t'),
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
        )

    def top_right_container(self):
        return html.Div(
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

    def bottom_left_container(self):
        return html.Div(
            className="three columns",
            children=[
                mydcc.Relayout(id='relayout-adjacency', aim='matrix_plot'),
                html.Div(
                    id='bottom-left-container',
                    className='window-small-bottom',
                    style={
                        'width': '100%',
                        'height': 300,
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
            ])

    def bottom_mid_menu_buttons(self):
        def get_right_slidertype():
            if self.current_plot == 'Radial' or self.current_plot == 'Fruchterman-Reingold':
                return (html.H6("Select time: ", className='mid-text'),
                        slider.draw('time_slider', self.timerange_matrix_plot[0], self.timerange_matrix_plot[1],
                                    int(self.timerange_matrix_plot[1] / 10)))
            elif self.current_plot == 'Interleaved dynamic network':
                return (html.H6("Select time-range: ", className='mid-text'),
                        rangeSlider.draw('time_slider', self.timerange_matrix_plot[0],
                                         self.timerange_matrix_plot[1],
                                         int(self.timerange_matrix_plot[1] / 10), visible=False))

        if self.current_plot and self.current_dataset:
            return [
                html.H6("Select node-range: ", className='mid-text'),
                rangeSlider.draw('node_slider', self.xrange_matrix_plot[0], self.xrange_matrix_plot[1],
                                 int(self.xrange_matrix_plot[1] / 10), visible=False),
                html.H6("Select log weight-range: ", className='mid-text'),
                rangeSlider.draw('weight_slider', self.weightrange_matrix_plot[0], self.weightrange_matrix_plot[1],
                                 int(self.weightrange_matrix_plot[1] / 10), visible=False),
                get_right_slidertype(),
                html.Section(className='mid-text', id='output-text')]
        else:
            return None

    def bottom_mid_menu(self):
        return html.Div(
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
                    children=self.bottom_mid_menu_buttons()
                )
            ]
        )


@app.callback(
    Output('console_output', 'children'),
    [Input('plot-selector', 'value'), Input('top-left-dropdown', 'value'), Input('shortestfrom', 'n_submit'),
     Input('shortestto', 'n_submit')])
def handle_top_left_menu(plottype, colorscale, shortestfrom, shortestto):
    print(t.time(), "@", inspect.currentframe().f_code.co_name, "Handing event.")
    dashboard.current_plot = plottype


@app.callback(
    Output('matrix_plot', 'children'),
    [Input('dataset-selector', 'value')])
def handle_dataset(dataset):
    print(t.time(), "@", inspect.currentframe().f_code.co_name, "Handing event.")
    if dataset:
        dashboard.current_dataset = dataset
        dashboard.get_matrix_plot_info()
        return dcc.Graph(figure=dashboard.matrix_plot.draw_plot(), id='adjacency_matrix')


@app.callback(
    Output('relayout-adjacency', 'layout'),
    [Input('node_slider', 'value')])
def adjust_node_range(rangeSlider_range):
    print("-----adjust_xrange----")
    return {
        'xaxis': dict(
            range=rangeSlider_range),
        'yaxis': dict(
            range=rangeSlider_range)
    }

""""PLACEHOLDER CALLBACK FOR FILLING IN MIDPLOT AFTER USER HAS SUBMITTED WANTED OPTIONS"""


def serve_layout():
    global dashboard
    dashboard = interactiveDashboard()
    return ([
        html.Div(
            className="row",
            style={
                'height': 500
            },
            children=[dashboard.top_left_menu(), dashboard.top_mid_container(), dashboard.top_right_container()]),
        html.Div(
            className="row",
            style={
                'height': 300
            },
            children=[dashboard.bottom_left_container(), dashboard.bottom_mid_menu()]
        )])

#                 html.Div(
#                     className="two columns",
#                     children=[
#                         html.Div(
#                             id='bottom-right-container',
#                             className='window-small-bottom',
#                             style={
#                                 'height':300,
#                                 'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
#                             },
#                             #children=[
#                             #    html.Button('Run action', id='del-selection', className="button-option")
#                             #]
#                         )
#                     ]
#                   )
#               ]
#           )
#     ])
#
#
# #@app.callback(
# #    Output('output-text', 'children'),
# #    [Input('top-left-checkbox', 'values'), Input('del-selection', 'n_clicks')])
# #def update_output(*value):
# #    print("-----update_output----")
# #    return ['You have selected "{}"'.format(value)]
#
# @app.callback(
#     Output('node_slider', 'value'),
#     [Input('matrix_plot', 'children')])
# def update_silder(*args):
#     print("-----update_slider----")
#     return xrange_matrix_plot
#
# @app.callback(
#     Output('matrix_plot', 'children'),
#     [Input('top-left-dropdown', 'value'), Input('weight_slider', 'value'), Input('time_slider', 'value')])
# def update_colorscale(colorscale, weight, timerange):
#     print("-----update_colorscale----")
#     global current_plot
#     if current_plot:
#         if type(timerange) != list:
#             timerange = [timerange, timerange+1]
#         return [mydcc.Relayout(id="relayout-adjacency", aim='adjacency_matrix'),
#                 dcc.Graph(figure=matrix_plot.draw_plot(colorscale, weightrange=weight,
#                                                        timerange=timerange), id='adjacency_matrix')]
#     else:
#         return None
#
#
# @app.callback(
#     Output('midplot', 'children'),
#     [Input('time_slider', 'value'), Input('plot-selector', 'value'), Input('weight_slider', 'value'),
#      Input('node_slider', 'value'), Input('shortestfrom', 'n_submit'), Input('shortestto', 'n_submit')],
#     [State('shortestfrom', 'value'),
#      State('shortestto', 'value')])
# def update_midplot(timerange, to_plot, weightrange, noderange, n1, n2, dijkstafrom, dijkstrato):
#     global timerangeG, to_ploG, weightrangeG, noderangeG, dijkstrafromG, dijkstratoG
#     run = True
#     if timerangeG != timerange:
#         timerangeG = timerange
#         run = True
#     if to_ploG != to_plot:
#         to_ploG = to_plot
#         run = True
#     if weightrangeG != weightrange:
#         weightrangeG = weightrange
#         run = True
#     #if noderangeG != noderange:
#     #    noderangeG = noderange
#     #    run = True
#     if dijkstrafromG != dijkstafrom:
#         dijkstrafromG = dijkstafrom
#         run = True
#     if dijkstratoG != dijkstrato:
#         dijkstratoG = dijkstrato
#         run = True
#     if noderange != noderangeG and to_plot == 'Interleaved dynamic network':
#         noderangeG = noderange
#         run = False
#     if run:
#         print("-----update_midplot----")
#         global current_plot
#         current_plot = to_plot
#         print(to_plot)
#         if to_plot == 'Radial' or to_plot == 'Fruchterman-Reingold':
#             return dcc.Graph(id='mid-graph-t',
#                              style={'margin':'auto'},
#             figure=node_link_plot.draw_plot(timerange, to_plot, weightrange=weightrange, noderange=noderange,
#                                             dijkstrafrom=dijkstafrom, dijkstrato=dijkstrato))
#         elif to_plot == 'Interleaved dynamic network':
#             return [mydcc.Relayout(id="relayout-midgraph", aim='mid-graph-t'), dcc.Graph(id='mid-graph-t',
#                              style={'margin': 'auto'},
#                              figure=
#                              interleavedPlot.draw_interleaved("profile_semantic_trafo_final.txt",
#                                                               start_time=timerange[0], end_time=timerange[1],
#                                                               weight_start=weightrange[0], weight_end=weightrange[1]))]
#
# @app.callback(
#     Output('bottom-middle-container', 'children'),
#     [Input('plot-selector', 'value')]
# )
# def update_plot_tools(plot):
#     print("-----update_plot_tools----")
#     global current_plot
#     current_plot = plot
#     if plot == 'Radial' or plot == 'Fruchterman-Reingold':
#         return [
#             html.H6("Select node-range: ", className='mid-text'),
#             rangeSlider.draw('node_slider', xrange_matrix_plot[0], xrange_matrix_plot[1],
#                              int(xrange_matrix_plot[1] / 10)),
#             html.H6("Select log weight-range: ", className='mid-text'),
#             rangeSlider.draw('weight_slider', weightrange_matrix_plot[0], weightrange_matrix_plot[1],
#                              int(weightrange_matrix_plot[1] / 10)),
#             html.H6("Select time-range: ", className='mid-text'),
#             slider.draw('time_slider', timerange_matrix_plot[0], timerange_matrix_plot[1],
#                              int(timerange_matrix_plot[1] / 10)),
#             html.Section(className='mid-text', id='output-text')
#         ]
#     elif plot == 'Interleaved dynamic network':
#         return [
#             html.H6("Select node-range: ", className='mid-text'),
#             rangeSlider.draw('node_slider', xrange_matrix_plot[0], xrange_matrix_plot[1],
#                              int(xrange_matrix_plot[1] / 10)),
#             html.H6("Select log weight-range: ", className='mid-text'),
#             rangeSlider.draw('weight_slider', weightrange_matrix_plot[0], weightrange_matrix_plot[1],
#                              int(weightrange_matrix_plot[1] / 10)),
#             html.H6("Select time-range: ", className='mid-text'),
#             rangeSlider.draw('time_slider', timerange_matrix_plot[0], timerange_matrix_plot[1],
#                              int(timerange_matrix_plot[1] / 10)),
#             html.Section(className='mid-text', id='output-text')
#         ]
#     else:
#         return [
#                 html.H6("Select node-range: ", className='mid-text'),
#                 rangeSlider.draw('node_slider', xrange_matrix_plot[0], xrange_matrix_plot[1],
#                                  int(xrange_matrix_plot[1] / 10), visible=False),
#                 html.H6("Select log weight-range: ", className='mid-text'),
#                 rangeSlider.draw('weight_slider', weightrange_matrix_plot[0], weightrange_matrix_plot[1],
#                                  int(weightrange_matrix_plot[1] / 10), visible=False),
#                 html.H6("Select time-range: ", className='mid-text'),
#                 rangeSlider.draw('time_slider', timerange_matrix_plot[0], timerange_matrix_plot[1],
#                                  int(timerange_matrix_plot[1] / 10), visible=False),
#                 html.Section(className='mid-text', id='output-text')
#         ]
#
#
#
# #@app.callback(
# #    Output('selected-data', 'children'),
# #    [Input('mid-graph-t', 'selectedData')])
# #def display_selected_data(selectedData):
# #    try:
# #       print(ast.literal_eval(json.dumps(selectedData, indent=2)))
# #    except ValueError:
# #        pass
#
# @app.callback(
#     Output('relayout-midgraph', 'layout'),
#     [Input('node_slider', 'value')])
# def adjust_xrange(rangeSlider_range):
#        return {'yaxis':dict(
#         range=rangeSlider_range
#     )}
#

