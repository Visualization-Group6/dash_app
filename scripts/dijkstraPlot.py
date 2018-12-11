import plotly.graph_objs as go
from plotly import offline
import networkx as nx
import plotly.figure_factory as ff
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

def PlotArrows(realxstart, realystart,realxend,realyend, color, weight):
    sidepointx, sidepointy = [], []
    rcs = []
    for realxstart_, realystart_, realxend_, realyend_ in zip(realxstart, realystart, realxend, realyend):
        if realxend_-realxstart_ == 0:
            realxstart_+=0.0000001
        rc = (realyend_-realystart_)/(realxend_-realxstart_)
        if rc == 0:
            rc += 0.1
        if rc in rcs:
            status = -1
        else:
            status = 1
            rcs.append(rc)

        a = -1/rc
        middlex = (realxend_+realxstart_)/2
        middley =(realyend_+realystart_)/2
        b = middley-a*middlex
        linelength = ((abs(realyend_-realystart_)**2+(abs(realxend_-realxstart_)**2))**0.5)

        sidepointx.append(middlex+linelength*0.06*status)
        sidepointy.append(a*middlex+linelength*0.06*status+b)

    x,y = realxstart, realystart
    middle_x, middle_y = sidepointx, sidepointy
    u = [(xs-x_)*10 for xs, x_ in zip(middle_x, x)]
    v = [(ys-y_)*10 for ys, y_ in zip(middle_y, y)]

    lines = [go.Scatter(x=[realxend_,pointx_], y=[realyend_, pointy_], mode='lines', line=dict(width=weight_/2,
                                                                                               color=color_))
             for realxend_, pointx_, realyend_, pointy_, color_, weight_ in zip(realxend, sidepointx, realyend,
                                                                                sidepointy, color, weight)]

    for x_, y_, u_, v_, weight_, color_ in zip(x, y, u, v, weight, color):
        fig = ff.create_quiver([x_], [y_], [u_], [v_], line=dict(width=weight_/2, color=color_), scale=0.1, arrow_scale=0.1)
        lines.append(fig['data'][0])
    #offline.plot(lines, filename='Quiver Plot Example.html')
    return lines

def dijkstraPlot(filename, source, target):
    G = nx.read_edgelist(filter_weights(0, filename), create_using=nx.DiGraph)    #read the file

    labels = []     #put the labels of the different nodes in a list
    for node in G.nodes(data=True):
        labels.append(node[0])

    tree_pos = nx.fruchterman_reingold_layout(G, weight='weight')
    pos = {}        #determine the positions of the locations of the different nodes
    for key in tree_pos:
        pos[key] = list(tree_pos[key])

    nodepath = nx.dijkstra_path(G, source,target)

    edgelist = []       # make a list of all edges in the shortest path
    for node in range(len(nodepath)-1):
        edgelist.append((nodepath[node],nodepath[node+1]))

    xstart = []
    ystart = []
    yend = []
    xend = []

    weights = []
    colors = []     #assign red color to the edges in the shortest path, black to the ones not in the shortest path
    for edge in G.edges(data=True):
        if (edge[0], edge[1]) in edgelist or (edge[1], edge[0]) in edgelist:
            colors.append('red')
        else:
            colors.append('black')
        weights.append(edge[2]['weight'])
        xstart.append(pos[edge[0]][0])
        ystart.append(pos[edge[0]][1])
        xend.append(pos[edge[1]][0])
        yend.append(pos[edge[1]][1])

    ArrowEdges = PlotArrows(xstart,ystart,xend,yend, colors, weights)

    nodes = [dict(type='scatter',     #create the nodelist in a proper format
                x=[pos[label][0]],
                y=[pos[label][1]],
                mode='markers',
                hoverinfo='text',
                marker=dict(size=20, color='Blue'),
                text=label) for label in labels]

    fig = go.Figure(data=nodes+ArrowEdges,      #this is the plot we are going to make (using the edge and nodelist)
                 layout=go.Layout(
                    title='<br>Holliday destinations',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    offline.plot(fig)

dijkstraPlot("testgraph.txt", "UK", "IT")