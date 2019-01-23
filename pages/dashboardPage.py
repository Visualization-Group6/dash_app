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


class interactiveDashboard():
    current_plot = None
    current_dataset = None
    current_colorscale = 'RdBu'
    matrix_plot = None
    current_from = None
    current_to = None
    current_timerange = None
    current_weightrange = None
    current_xrange = None

    def __init__(self):
        self.colorscales = ["Greys", "YlOrRd", "RdBu"]
        self.plots = ['Radial', 'Fruchterman-Reingold', 'Interleaved dynamic network']
        self.datasets = os.listdir(preProcessing.get_working_dir())

    def get_matrix_plot_info(self):
        if self.current_dataset:
            self.matrix_plot = matrixVisualisation.AdjacencyMatrix(self.current_dataset)
            self.xrange_matrix_plot = self.matrix_plot.get_range()
            self.weightrange_matrix_plot = self.matrix_plot.get_weight()
            self.timerange_matrix_plot = self.matrix_plot.get_time()
            self.static_graph_plot = layoutDiagram.NodeLink(self.current_dataset)

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
                        dropdownMenu.draw('top-left-dropdown', self.colorscales, default=self.current_colorscale),
                        checkboxes.draw('matrix-reorder', ['Normal Matrix', 'Reordered Matrix']),
                        html.H6(children='Draw shortest path (from, to): ', className='mid-text'),
                        html.Div(className='textbox-small', children=[
                            dcc.Input(id='shortestfrom', type='text', value=None, disabled=True,
                                      style={'display': 'inline-table', 'width': '50%'}),
                            dcc.Input(id='shortestto', type='text', value=None, disabled=True,
                                      style={'display': 'inline-table', 'width': '50%'})]),
                        html.Div(className='textbox-small', children=html.Button('Execute changes', id='execute',
                                                                                 className="button submit")),
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
            self.current_timerange = self.timerange_matrix_plot
            if self.current_plot == 'Radial' or self.current_plot == 'Fruchterman-Reingold':
                return [html.H6("Select time: ", className='mid-text'),
                        slider.draw('time_slider', self.timerange_matrix_plot[0], self.timerange_matrix_plot[1],
                                    int(self.timerange_matrix_plot[1] / 10))]
            elif self.current_plot == 'Interleaved dynamic network':
                return [html.H6("Select time-range: ", className='mid-text'),
                        rangeSlider.draw('time_slider', self.timerange_matrix_plot[0],
                                         self.timerange_matrix_plot[1],
                                         int(self.timerange_matrix_plot[1] / 10))]

        if self.current_plot and self.current_dataset:
            while True:
                try:
                    print(self.xrange_matrix_plot)
                    print(self.weightrange_matrix_plot)
                    print(self.timerange_matrix_plot)
                except AttributeError:
                    pass
                else:
                    break
            default = [
                html.H6("Select node-range: ", className='mid-text'),
                rangeSlider.draw('node_slider', self.xrange_matrix_plot[0], self.xrange_matrix_plot[1],
                                 int(self.xrange_matrix_plot[1] / 10)),
                html.H6("Select log weight-range: ", className='mid-text'),
                rangeSlider.draw('weight_slider', self.weightrange_matrix_plot[0], self.weightrange_matrix_plot[1],
                                 int(self.weightrange_matrix_plot[1] / 10))]
            default.extend(get_right_slidertype())
            return default
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

    def bottom_right_container(self):
        return html.Div(
            className="two columns",
            children=[
                html.Div(
                    id='bottom-right-container',
                    className='window-small-bottom',
                    style={
                        'height': 300,
                        'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                    }
                )
            ]
        )


@app.callback(
    Output('console_output', 'children'),
    [Input('plot-selector', 'value'), Input('top-left-dropdown', 'value'), Input('shortestfrom', 'value'),
     Input('shortestto', 'value'), Input('time_slider', 'value'), Input('weight_slider', 'value'),
     Input('node_slider', 'value')])
def handle_user_change(plottype, colorscale, shortestfrom, shortestto, timerange, weightrange, xrange):
    t.sleep(1)
    print(t.time(), "@", inspect.currentframe().f_code.co_name, "Handing event.")
    print(xrange)
    if type(timerange) != list:
        timerange = [timerange, timerange + 1]
    dashboard.current_colorscale = colorscale
    dashboard.current_from = shortestfrom
    dashboard.current_to = shortestto
    dashboard.current_timerange = timerange
    dashboard.current_weightrange = weightrange
    dashboard.current_xrange = xrange


@app.callback(
    Output('relayout-adjacency', 'layout'),
    [Input('node_slider', 'value')])
def adjust_node_range(rangeSlider_range):
    print(t.time(), "@", inspect.currentframe().f_code.co_name, "Handing event.")
    return {
        'xaxis': dict(
            range=rangeSlider_range),
        'yaxis': dict(
            range=rangeSlider_range)
    }


@app.callback(
    Output('bottom-middle-container', 'children'),
    [Input('plot-selector', 'value')]
)
def handle_plot_selection(plottype):
    print(t.time(), "@", inspect.currentframe().f_code.co_name, "Handing event.")
    dashboard.current_plot = plottype
    return dashboard.bottom_mid_menu_buttons()


@app.callback(Output('shortestfrom', 'value'),
              [Input('execute', 'n_clicks')])
def reset_path_from(n_clicks):
    if n_clicks:
        return ""


@app.callback(Output('shortestto', 'value'),
              [Input('execute', 'n_clicks')])
def reset_path_to(n_clicks):
    if n_clicks:
        return ""


@app.callback(Output('shortestto', 'disabled'),
              [Input('plot-selector', 'value')])
def reset_path_to(plottype):
    if plottype == 'Radial' or plottype == 'Fruchterman-Reingold':
        return False
    return True


@app.callback(Output('shortestfrom', 'disabled'),
              [Input('plot-selector', 'value')])
def reset_path_to(plottype):
    if plottype == 'Radial' or plottype == 'Fruchterman-Reingold':
        return False
    return True


@app.callback(Output('matrix_plot', 'children'),
              [Input('execute', 'n_clicks'), Input('dataset-selector', 'value'), Input('plot-selector', 'value'),
               Input('matrix-reorder', 'value')])
def execute_matrix(n_clicks, dataset, plottype, plottypeM):
    if dataset:
        dashboard.current_dataset = dataset
        dashboard.get_matrix_plot_info()
        if plottypeM == 'Reordered Matrix':
            return [mydcc.Relayout(id='relayout-adjacency', aim='adjacency_matrix'),
                    dcc.Graph(figure=dashboard.matrix_plot.reorder(colorscale=dashboard.current_colorscale,
                                                                   weightrange=dashboard.current_weightrange,
                                                                   timerange=dashboard.current_timerange,
                                                                   xrange=dashboard.current_xrange),
                              id='adjacency_matrix')]
        else:
            return [mydcc.Relayout(id='relayout-adjacency', aim='adjacency_matrix'),
                    dcc.Graph(figure=dashboard.matrix_plot.draw_plot(colorscale=dashboard.current_colorscale,
                                                                     weightrange=dashboard.current_weightrange,
                                                                     timerange=dashboard.current_timerange,
                                                                     xrange=dashboard.current_xrange),
                              id='adjacency_matrix')]


@app.callback(Output('midplot', 'children'),
              [Input('execute', 'n_clicks'), Input('dataset-selector', 'value'), Input('plot-selector', 'value')])
def execute_mainplot(n_clicks, dataset, plottype):
    if plottype:
        while True:
            try:
                print(dashboard.xrange_matrix_plot)
                print(dashboard.weightrange_matrix_plot)
                print(dashboard.timerange_matrix_plot)
            except AttributeError:
                pass
            else:
                break
        if plottype == 'Radial' or plottype == 'Fruchterman-Reingold':
            if not dashboard.current_timerange:
                dashboard.current_timerange = dashboard.timerange_matrix_plot[0]
            if not dashboard.current_weightrange:
                dashboard.current_weightrange = dashboard.weightrange_matrix_plot
            return dcc.Graph(id='mid-graph-t',
                             style={'margin': 'auto'},
                             figure=dashboard.static_graph_plot.draw_plot(dashboard.current_timerange, plottype,
                                                                          weightrange=dashboard.current_weightrange,
                                                                          noderange=dashboard.current_xrange,
                                                                          dijkstrafrom=dashboard.current_from,
                                                                          dijkstrato=dashboard.current_to,
                                                                          colorscale=dashboard.current_colorscale))
        elif plottype == 'Interleaved dynamic network':
            if not dashboard.current_timerange or dashboard.current_timerange[-1] - dashboard.current_timerange[0]:
                dashboard.current_timerange = dashboard.timerange_matrix_plot
            if not dashboard.current_weightrange:
                dashboard.current_weightrange = dashboard.weightrange_matrix_plot
            if not dashboard.current_xrange:
                dashboard.current_xrange = dashboard.xrange_matrix_plot
            return dcc.Graph(id='mid-graph-t',
                             style={'margin': 'auto'},
                             figure=interleavedPlot.draw_interleaved(dashboard.current_dataset,
                                                                     colorscale=dashboard.current_colorscale,
                                                                     start_time=dashboard.current_timerange[0],
                                                                     end_time=dashboard.current_timerange[1],
                                                                     weight_start=dashboard.current_weightrange[0],
                                                                     weight_end=dashboard.current_weightrange[1],
                                                                     start_node=dashboard.current_xrange[0],
                                                                     end_node=dashboard.current_xrange[1]))


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
            children=[dashboard.bottom_left_container(), dashboard.bottom_mid_menu(),
                      dashboard.bottom_right_container()]
        )])
