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

    def angle(self, node): # returns angle in radians
        return (360/(self.data.shape[0] + 1)  * node) * pi/180


    def y_node(self, node):
        return 10 * sin(self.angle(node))


    def x_node(self, node):
        return 10 * cos(self.angle(node))

    def read_data(self):
        self.data = preProcessing.open_dataset(self.dataset)
        self.startindex, self.endindex, self.timeindex = np.nonzero(self.data)

    def filter_time(self, time):
        newdata = []
        for start, end in zip(self.startindex[np.where(self.timeindex == time)],self.endindex[np.where(self.timeindex == time)]):
            newdata.append(" ".join([str(start), str(end), str(self.data[start, end, time])]))
        return nx.parse_edgelist(newdata, nodetype=int, data=(('weight',float),))

    def draw_plot(self, time):
        if len(self.data) == 1 :
            self.read_data()
        self.G = self.filter_time(time)
        weights = []
        for edge in self.G.edges(data=True):
            weights.append(edge[2]['weight']*0.6)

        labels = []
        i = 0
        for node in self.G.nodes(data=True):
            labels.append(node[0])
            i += 1

        # RADIAL: Comment the following lines if you want to use Fruchterman-Reingold
        pos = {}
        for key in self.G.nodes:
            pos[key] = [self.x_node(key), self.y_node(key)]

        # FORCE-DIRECTED: Uncomment next lines to have a fruchterman reingold layout
        # tree_pos = nx.fruchterman_reingold_layout(G, weight='weight')
        # pos = {}
        # for key in tree_pos:
        #     pos[key] = list(tree_pos[key])

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
        return fig




