import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx
#  https://plot.ly/~empet/14683/networks-with-plotly/#/
#  https://plot.ly/python/network-graphs/

G = nx.read_edgelist("testgraph.txt")

weights = []
for edge in G.edges(data=True):
    weights.append(edge[2]['weight']*0.6)

labels = []
i = 0
for node in G.nodes(data=True):
    labels.append(node[0])
    i += 1

tree_pos = nx.fruchterman_reingold_layout(G, weight='weight')
pos = {}
for key in tree_pos:
    pos[key] = list(tree_pos[key])

nx.set_node_attributes(G,pos,name='pos')
nx.write_gml(G,"testgraph_out.txt")





edge_trace = [dict(type='scatter',
             x=[pos[e[0]][0], pos[e[1]][0]],
             y=[pos[e[0]][1], pos[e[1]][1]],
              mode='lines',
              line=dict(width=weights[k], color='black', ))  for k, e in enumerate(G.edges())]

#edge_trace = go.Scatter(
#    x=[],
#    y=[],
#    line=dict(width=0.5,color='#888'),
#    hoverinfo='none',
#    mode='lines')

#for edge in G.edges():
#    x0, y0 = G.node[edge[0]]['pos']
#    x1, y1 = G.node[edge[1]]['pos']
#    edge_trace['x'] += tuple([x0, x1, None])
#    edge_trace['y'] += tuple([y0, y1, None])

xs, ys = [], []
for key in pos:
    xs.append(pos[key][0])
    ys.append(pos[key][1])

nodes=dict(type='scatter',
           x=xs,
           y=ys,
           mode='markers',
           hoverinfo='text',
           marker=dict(size=20, color='red'),
           text=labels)

#for node in G.nodes():
#    x, y = G.node[node]['pos']
#    node_trace['x'] += tuple([x])
#    node_trace['y'] += tuple([y])

#for node, adjacencies in enumerate(G.adjacency()):
#    node_info = str(labels[node])
#    node_trace['text']+=tuple([node_info])

fig = go.Figure(data=edge_trace+[nodes],
             layout=go.Layout(
                title='<br>Holliday destinations',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

offline.plot(fig)