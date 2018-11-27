import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx
#  https://plot.ly/~empet/14683/networks-with-plotly/#/
#  https://plot.ly/python/network-graphs/


def filter_weights(weight):
    newdata = []
    with open("testgraph.txt", "r") as f:
        for line in f.read().split("\n"):
            if int(line.split("'weight':")[1].split("}")[0]) > weight:
                newdata.append(line)
    with open("testgraph_"+str(weight)+".txt", "w") as f:
        f.write("\n".join(newdata))
    return "testgraph_"+str(weight)+".txt"



G = nx.read_edgelist(filter_weights(0))

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

xs, ys = [], []
for key in pos:
    xs.append(pos[key][0])
    ys.append(pos[key][1])

pop_size = {}
temps = {}
locations = {}
with open("demographics.txt") as f:
    for line in f.read().split('\n'):
        pop_size[line.split(",")[0]] = int(np.log(int(line.split(",")[1]))) * 10
        locations[line.split(",")[0]] = line.split(",")[2]
        temps[line.split(",")[0]] = line.split(",")[3]

nodes = [dict(type='scatter',
            x=[pos[label][0]],
            y=[pos[label][1]],
            mode='markers',
            hoverinfo='text',
            marker=dict(size=pop_size[label], color='red'),
            text=label+", location: "+locations[label]+" average temp: "+temps[label]+" degrees.") for label in labels]

#for node in G.nodes():
#    x, y = G.node[node]['pos']
#    node_trace['x'] += tuple([x])
#    node_trace['y'] += tuple([y])

#for node, adjacencies in enumerate(G.adjacency()):
#    node_info = str(labels[node])
#    node_trace['text']+=tuple([node_info])
print(nodes)
fig = go.Figure(data=edge_trace+nodes,
             layout=go.Layout(
                title='<br>Holliday destinations',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

offline.plot(fig)