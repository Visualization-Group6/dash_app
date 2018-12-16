import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import time as t
from scripts import preProcessing as pp
from scripts import dataSelection
from scipy import signal
import pickle


def y_node(node): # function to determine y-value
    return node * 2


def draw_interleaved(filename, start_time = -float("inf"), end_time = float("inf"), weight_start = -float("inf"),
                     weight_end = float("inf")):

    working_dir = pp.get_working_dir()
    with open(working_dir + filename, 'r') as f:
        encoded_data = f.read()
    new_data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]
    xlist = []
    ylist = []
    length = 10  # distance between start and end node
    edge_trace = []

    for i in new_data[1:]:
        if len(xlist) > 11000:
            edge_trace.append(go.Scattergl(x=xlist, y=ylist, line=dict(width=.5, color='black')))
            xlist = []
            ylist = []
        if start_time < int(i[0]) < end_time and weight_start < int(i[3]) < weight_end:
            x = int(i[0]) * 0.1 - 0.1
            xlist.append(None)
            xlist.append(x)
            xlist.append(x+length)
            ylist.append(None)
            ylist.append(y_node(int(i[1])))
            ylist.append(y_node(int(i[2])))

    fig = dict(data=edge_trace,
                 layout=go.Layout(
                    height=400,
                    title='<br>Dynamic Graph Visualization',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)),
               )

    return fig

starttime = t.time()
dataset = 'profile_semantic_trafo_final.txt'
fig = draw_interleaved(dataset)
offline.plot(fig)
print(t.time() - starttime)
#pickle.dump(fig, open(preProcessing.get_working_dir()+dataset.split(".txt")[0]+".dat", "wb"))
