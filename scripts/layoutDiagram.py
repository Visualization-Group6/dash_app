import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx
import time as t
from scripts import preProcessing
from scripts import dataSelection
from math import sin, cos, pi


def angle(G, node): # returns angle in radians
    return (360/(max(G.nodes()) + 1)  * node) * pi/180


def y_node(node):
    return 10 * sin(angle(G, node))


def x_node(node):
    return 30 * cos(angle(G, node))


def filter_time(time):
    newdata = []
    with open(preProcessing.get_working_dir() + "profile_semantic_trafo_final.txt", "r") as f:
        for line in f.read().split("\n")[2:]:
            if len(line.split(" ")) >= 4:
                if int(line.split(" ")[0]) == time:
                    newdata.append(" ".join(line.split(" ")[1:4]) + line.split(" ")[4])
    with open(preProcessing.get_working_dir() + "profile_semantic_trafo_final_"+str(time)+".txt", "w") as f:
        f.write("\n".join(newdata))
    return preProcessing.get_working_dir() +  "profile_semantic_trafo_final_"+str(time)+".txt"


time = 1

G = nx.read_edgelist(filter_time(time), nodetype=int, data=(('weight',int),))
print(G.edges())

weights = []
for edge in G.edges(data=True):
    weights.append(edge[2]['weight']*0.6)

labels = []
i = 0
for node in G.nodes(data=True):
    labels.append(node[0])
    i += 1


pos = {}
for key in G.nodes:
    print(key)
    pos[key] = [x_node(key), y_node(key)]

# Uncomment next lines to have a fruchterman reingold layout
# tree_pos = nx.fruchterman_reingold_layout(G, weight='weight')
# pos = {}
# for key in tree_pos:
#     pos[key] = list(tree_pos[key])

edge_trace = [dict(type='scatter',
             x=[pos[e[0]][0], pos[e[1]][0]],
             y=[pos[e[0]][1], pos[e[1]][1]],
              mode='lines',
              line=dict(color='black'))  for k, e in enumerate(G.edges())]

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
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

offline.plot(fig)