import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx
from scripts import preProcessing
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
        return (360 / (self.data.shape[0] + 1) * node) * pi / 180

    def y_node(self, node):
        return 10 * sin(self.angle(node))

    def x_node(self, node):
        return 10 * cos(self.angle(node))

    def read_data(self):
        print(t.time(), "@", inspect.currentframe().f_code.co_name, self.dataset)
        self.data = preProcessing.open_dataset(self.dataset)
        self.startindex, self.endindex, self.timeindex = np.nonzero(self.data)

    def filter(self, time, weightrange, noderange):
        if type(time) == list:
            return 0
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "%1", time, weightrange, noderange)
        try:
            print(t.time(), "@", inspect.currentframe().f_code.co_name, "%2", self.startindex)
        except AttributeError:
            self.read_data()
        if "".join([str(time), str(weightrange), str(noderange)]) not in self.timedata:
            print(t.time(), "@", inspect.currentframe().f_code.co_name, '%New timerange re-plotting')
            newdata = []
            for start, end in zip(self.startindex[np.where(self.timeindex == time)],
                                  self.endindex[np.where(self.timeindex == time)]):
                if (start > noderange[0] and start < noderange[1]) and (end > noderange[0] and end < noderange[1]):
                    if float(self.data[start, end, time]) >= np.exp(weightrange[0]) and float(
                            self.data[start, end, time]) < np.exp(weightrange[1]):
                        newdata.append(" ".join([str(start), str(end), str(self.data[start, end, time])]))
            edgelist = nx.parse_edgelist(newdata, nodetype=int, data=(('weight', float),))
            print(edgelist.edges())
            self.timedata["".join([str(time), str(weightrange), str(noderange)])] = edgelist
        return self.timedata["".join([str(time), str(weightrange), str(noderange)])]

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

    def draw_plot(self, time, layout, weightrange=None, noderange=None, dijkstrafrom=None, dijkstrato=None):
        if not noderange:
            noderange = [0, float('inf')]
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
        weights = []
        for edge in self.G.edges(data=True):
            weights.append(edge[2]['weight'] * 0.6)

        labels = []
        i = 0
        for node in self.G.nodes(data=True):
            labels.append(node[0])
            i += 1

        if layout == 'Fruchterman-Reingold':
            pos = self.get_fruchterman_pos()
        elif layout == 'Radial':
            pos = self.get_radial_pos()
        edgelist = []  # make a list of all edges in the shortest path
        print(self.G.nodes())
        if dijkstrato and dijkstrafrom:
            nodepath = nx.dijkstra_path(self.G, int(dijkstrafrom), int(dijkstrato))
            print(t.time(), "@", inspect.currentframe().f_code.co_name, "%2", dijkstrafrom, dijkstrato, nodepath)
            for node in range(len(nodepath) - 1):
                edgelist.append((nodepath[node], nodepath[node + 1]))

        edge_trace = []
        for edge in self.G.edges(data=True):
            if (edge[0], edge[1]) in edgelist or (edge[1], edge[0]) in edgelist:
                color = 'red'
            else:
                color = 'black'
            edge_trace.append(dict(type='scatter',
                                   x=[pos[edge[0]][0], pos[edge[1]][0]],
                                   y=[pos[edge[0]][1], pos[edge[1]][1]],
                                   mode='lines',
                                   line=dict(color=color)))

        nodes = [dict(type='scatter',
                      x=[pos[label][0]],
                      y=[pos[label][1]],
                      mode='markers',
                      hoverinfo='text',
                      marker=dict(color='red'),
                      text=label) for label in labels]

        if layout == 'Fruchterman-Reingold':
            fig = go.Figure(data=edge_trace + nodes,
                            layout=go.Layout(
                                title='<br> Profile Semantic Trafo',
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
                                title='<br> Profile Semantic Trafo',
                                titlefont=dict(size=16),
                                showlegend=False,
                                width=500,
                                height=500,
                                hovermode='closest',
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        if layout == 'Fruchterman-Reingold':
            self.saved_plotsFR[time] = fig
            return self.saved_plotsFR[time]
        elif layout == 'Radial':
            self.saved_plotsR[time] = fig
            return self.saved_plotsR[time]
