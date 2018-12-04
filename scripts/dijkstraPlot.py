import plotly.graph_objs as go
from plotly import offline
import networkx as nx
from scripts import preProcessing
#  https://plot.ly/~empet/14683/networks-with-plotly/#/
#  https://plot.ly/python/network-graphs/


def filter_weights(weight,filename):
    newdata = []
    with open(filename, "r") as f:
        for line in f.read().split("\n"):
            if int(line.split("'weight':")[1].split("}")[0]) > weight:
                newdata.append(line)
    with open("output"+str(weight)+".txt", "w") as f:
        f.write("\n".join(newdata))
    return "output"+str(weight)+".txt"

def dijkstraPlot(filename, source, target):
    G = nx.read_edgelist(filter_weights(0, filename))    #read the file

    labels = []     #put the labels of the different nodes in a list
    for node in G.nodes(data=True):
        labels.append(node[0])

    tree_pos = nx.fruchterman_reingold_layout(G, weight='weight')
    pos = {}        #determine th positions of the locations of the different nodes
    for key in tree_pos:
        pos[key] = list(tree_pos[key])

    nodepath = nx.dijkstra_path(G, source,target)

    edgelist = []       # make a list of all edges in the shortest path
    for node in range(len(nodepath)-1):
        edgelist.append((nodepath[node],nodepath[node+1]))

    colors = []     #assign red color to the edges in the shortest path, black to the ones not in the shortest path
    for edge in G.edges(data=True):
        if (edge[0], edge[1]) in edgelist or (edge[1], edge[0]) in edgelist:
            colors.append('red')
        else:
            colors.append('black')

    nodes = [dict(type='scatter',     #create the nodelist in a proper format
                x=[pos[label][0]],
                y=[pos[label][1]],
                mode='markers',
                hoverinfo='text',
                marker=dict(size=20, color='Blue'),
                text=label) for label in labels]

    edge_trace = [dict(type='scatter',  #create the edgelist in a proper format
                 x=[pos[e[0]][0], pos[e[1]][0]],
                 y=[pos[e[0]][1], pos[e[1]][1]],
                  mode='lines',
                  line=dict(color=colors[k], )) for k, e in enumerate(G.edges())]

    fig = go.Figure(data=edge_trace+nodes,      #this is the plot we are going to make (using the edge and nodelist)
                 layout=go.Layout(
                    title='<br>Holliday destinations',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    offline.plot(fig)

dijkstraPlot(preProcessing.get_working_dir()+"/ testgraph.txt", "UK", "IT")