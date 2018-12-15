import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx
import time as t
from scripts import preProcessing
from scripts import dataSelection
from math import sin, cos, pi


class NodeLink():
    def __init__(self, dataset):
        self.dataset = dataset
        self.data = [0]
        self.timedata = {}
        self.saved_plotsR = {}
        self.saved_plotsFR = {}

    def angle(self, node): # returns angle in radians
        return (360/(self.data.shape[0] + 1)  * node) * pi/180


    def y_node(self, node):
        return 10 * sin(self.angle(node))


    def x_node(self, node):
        return 10 * cos(self.angle(node))

    def read_data(self):
        self.data = preProcessing.open_dataset(self.dataset)
        self.startindex, self.endindex, self.timeindex = np.nonzero(self.data)

    def filter(self, time, weightrange, noderange):
        if type(time) == list:
            return 0
        print(time)
        try:
            print(self.startindex)
        except AttributeError:
            self.read_data()
        try:
            self.timedata[time]
        except KeyError:
            print('New timerange, re-plotting')
            newdata = []
            for start, end in zip(self.startindex[np.where(self.timeindex == time)],self.endindex[np.where(self.timeindex == time)]):
                newdata.append(" ".join([str(start), str(end), str(self.data[start, end, time])]))
            edgelist = nx.parse_edgelist(newdata, nodetype=int, data=(('weight',float),))
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

    def draw_plot(self, time, layout, weightrange=None, noderange=None):
        print(layout)
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

        if len(self.data) == 1 :
            self.read_data()
        self.G = self.filter(time, weightrange, noderange)
        weights = []
        for edge in self.G.edges(data=True):
            weights.append(edge[2]['weight']*0.6)

        labels = []
        i = 0
        for node in self.G.nodes(data=True):
            labels.append(node[0])
            i += 1

        if layout == 'Fruchterman-Reingold':
            pos = self.get_fruchterman_pos()
        elif layout == 'Radial':
            pos = self.get_radial_pos()

        edge_trace = [dict(type='scatter',
                     x=[pos[e[0]][0], pos[e[1]][0]],
                     y=[pos[e[0]][1], pos[e[1]][1]],
                      mode='lines',
                      line=dict(color='black'))  for k, e in enumerate(self.G.edges())]

        xs, ys = [], []
        for key in pos:
            xs.append(pos[key][0])
            ys.append(pos[key][1])


        nodes = [dict(type='scatter',
                    x=[pos[label][0]],
                    y=[pos[label][1]],
                    mode='markers',
                    hoverinfo='text',
                    marker=dict(color='red'),
                    text=label) for label in labels]


        fig = go.Figure(data=edge_trace+nodes,
                     layout=go.Layout(
                        title='<br> Profile Semantic Trafo',
                        titlefont=dict(size=16),
                        showlegend=False,
                        width= 400,
                        height = 400,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        if layout == 'Fruchterman-Reingold':
            self.saved_plotsFR[time] = fig
            return self.saved_plotsFR[time]
        elif layout == 'Radial':
            self.saved_plotsR[time] = fig
            return self.saved_plotsR[time]




