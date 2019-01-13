import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx
from scripts import preProcessing, color_scales
from scripts import dataSelection
from math import sin, cos, pi
import inspect
import time as t
import sys


class NodeLink():
    def __init__(self, dataset):
        self.dataset = dataset
        self.data = [0]
        self.timedata = {}
        self.saved_plotsR = {}
        self.saved_plotsFR = {}

    def angle(self, node):  # returns angle in radians
        return (360 / (self.shape) * node) * pi / 180

    def y_node(self, node):
        return 10 * sin(self.angle(node))

    def x_node(self, node):
        return 10 * cos(self.angle(node))

    def read_data(self):
        print(t.time(), "@", inspect.currentframe().f_code.co_name, self.dataset)
        working_dir = preProcessing.get_working_dir()
        with open(working_dir + self.dataset, 'r') as f:
            encoded_data = f.read()
        self.data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""][1:]

    def filter(self, time, weightrange, noderange):
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "%1", time, weightrange, noderange)
        if self.data == [0]:
            self.read_data()
        edgeweights = []
        for i in self.data:
            if (int(i[0])) == time:
                if (int(i[1]) >= noderange[0] and int(i[1]) <= noderange[1]) and (
                                int(i[2]) >= noderange[0] and int(i[2]) <= noderange[1]):
                    if float(i[3]) >= np.exp(weightrange[0]) and float(i[3]) < np.exp(weightrange[1]):
                        edgeweights.append(" ".join([str(i[1]), str(i[2]), str(i[3])]))
        edgelist = nx.parse_edgelist(edgeweights, nodetype=int, data=(('weight', float),))
        return edgelist

    def get_fruchterman_pos(self):
        tree_pos = nx.fruchterman_reingold_layout(self.G, weight='weight')
        pos = {}
        for key in tree_pos:
            pos[key] = list(tree_pos[key])
        return pos

    def get_radial_pos(self):
        pos = {}
        for key in self.G.nodes:
            pos[key] = [self.x_node(key), self.y_node(key)]
        return pos

    def draw_plot(self, time, layout, weightrange=None, noderange=None, dijkstrafrom=None, dijkstrato=None,
                  colorscale='RdBu'):
        now = t.time()
        if not noderange:
            noderange = [0, float('inf')]
        if type(time) == list:
            time = time[0]
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "%0", noderange)
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "%1", layout)
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "%1", time)
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "%1", weightrange)
        if layout == 'Radial':
            try:
                self.saved_plotsR["".join([str(time), str(weightrange), str(noderange)])]
            except KeyError:
                pass
            else:
                return self.saved_plotsR["".join([str(time), str(weightrange), str(noderange)])]
        elif layout == 'Fruchterman-Reingold':
            try:
                self.saved_plotsFR["".join([str(time), str(weightrange), str(noderange)])]
            except KeyError:
                pass
            else:
                return self.saved_plotsFR["".join([str(time), str(weightrange), str(noderange)])]
        else:
            return None

        if len(self.data) == 1:
            self.read_data()
        self.G = self.filter(time, weightrange, noderange)

        i = 0
        labels = []
        for node in self.G.nodes(data=True):
            labels.append(node[0])
            i += 1
        self.shape = i
        if layout == 'Fruchterman-Reingold':
            pos = self.get_fruchterman_pos()
        elif layout == 'Radial':
            pos = self.get_radial_pos()
        edgelist = []  # make a list of all edges in the shortest path
        if dijkstrato and dijkstrafrom:
            nodepath = nx.dijkstra_path(self.G, int(dijkstrafrom), int(dijkstrato))
            print(t.time(), "@", inspect.currentframe().f_code.co_name, "%2", dijkstrafrom, dijkstrato, nodepath)
            for node in range(len(nodepath) - 1):
                edgelist.append((nodepath[node], nodepath[node + 1]))
        edge_trace = []
        opacity = {}
        colors = {}
        for edge in self.G.edges(data=True):
            if edgelist:
                if (edge[0], edge[1]) in edgelist or (edge[1], edge[0]) in edgelist:
                    color = 'red'
                    width = 1
                else:
                    color = 'black'
                    width = 0.1
            else:
                color = color_scales.get_color(colorscale, min_weight=weightrange[0],
                                               max_weight=weightrange[1],
                                               current_weight=np.log(edge[2]['weight']))
                width = 1
            edge_trace.append(dict(type='scatter',
                                   x=[pos[edge[0]][0], pos[edge[1]][0]],
                                   y=[pos[edge[0]][1], pos[edge[1]][1]],
                                   mode='lines',
                                   line=dict(color=color, width=width)))
            opacity[edge[0]] = width
            opacity[edge[1]] = width
            colors[edge[0]] = color
            colors[edge[1]] = color

        nodes = [dict(type='scatter',
                      x=[pos[label][0]],
                      y=[pos[label][1]],
                      mode='markers',
                      hoverinfo='text',
                      marker=dict(color=colors[label], opacity=opacity[label]),
                      text=label) for label in labels]

        if layout == 'Fruchterman-Reingold':
            fig = go.Figure(data=edge_trace + nodes,
                            layout=go.Layout(
                                title=self.dataset,
                                titlefont=dict(size=16),
                                showlegend=False,
                                width=1000,
                                height=500,
                                hovermode='closest',
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        elif layout == 'Radial':
            fig = go.Figure(data=edge_trace + nodes,
                            layout=go.Layout(
                                title=self.dataset,
                                titlefont=dict(size=16),
                                showlegend=False,
                                width=500,
                                height=500,
                                hovermode='closest',
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "<<<MAIN PLOTTING TOOK", t.time() - now,
              "SECONDS>>>")
        return fig
