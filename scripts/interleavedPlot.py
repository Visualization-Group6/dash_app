import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx
import time as t
from scripts import preProcessing
from scripts import dataSelection

def y_node(node): # function to determine y-value
    return node * 2

starttime = t.time()

df = preProcessing.open_dataset('profile_semantic_trafo_final.txt') # Open the dataset
#df = dataSelection.slice_array(preProcessing.open_dataset('profile_semantic_trafo_final.txt'),x_max=100)
startindex, endindex, timeindex = np.nonzero(df)


xlist = []
ylist = []
length = 10 # distance between start and end node
edge_trace = []
current_time = 0
x = -0.1
# Next for-loops are for processing the data
for time in np.sort(timeindex):
    if time != current_time:
        print(time)
        current_time = time
        x += 0.1
    if len(xlist) > 11000:
        print("----saving----")
        edge_trace.append(go.Scattergl(x=xlist, y=ylist, mode='lines', line=dict(width=.5, color='black')))
        xlist = []
        ylist = []
    for start, end in zip(startindex[np.where(timeindex == time)],endindex[np.where(timeindex == time)]):
        if df[start, end, time] > 0:
            xlist.append(x)
            xlist.append(x)
            xlist.append(x+length)
            ylist.append(None)
            ylist.append(y_node(start))
            ylist.append(y_node(end))
        else:
            print("mmm")
print('100%')


# Make a dictionary of edges for networkx and plotly
#edge_trace = [go.Scattergl(
#                   x=[from_pos[i][0], to_pos[i][0]],
#                   y=[from_pos[i][1], to_pos[i][1]],
#                   mode='lines',
#                   line=dict(width=.5, color='black')) for i in range(len(from_pos))]

#positions = from_pos.copy() # list to combine 'from' and 'to'-positions

#for i in range(0, len(to_pos)):
#    positions.append(to_pos[i])

# Make a dictionary of nodes for networkx and plotly
#nodes = [go.Scattergl(
#              x=[positions[n][0]],
#              y=[positions[n][1]],
#              mode='markers',
#              hoverinfo='text',
#              marker=dict(color='red')) for n in range(0, len(positions))]

# Make the figure
fig = dict(data=edge_trace,
             layout=go.Layout(
                title='<br>Dynamic Graph Visualization',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

offline.plot(fig)
print(t.time()-starttime)