import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
import numpy as np
import networkx as nx

from scripts import preProcessing
from scripts import dataSelection

def y_node(node): # function to determine y-value
    return node * 2

df = preProcessing.open_dataset('profile_semantic_trafo_final.txt') # Open the dataset

from_pos = [] # list for position of start nodes
to_pos = [] # list for position of end nodes
edges = [] # this list is not used at this moment
x = 0.0
length = 10 # distance between start and end node

# Next for-loops are for processing the data
for time in range(1, df.shape[2]):
    for start in range(1, df.shape[0]):
        for end in range(1, df.shape[1]):
            if df[start, end, time] > 0:
                from_pos.append([x, y_node(start)]) # start position
                to_pos.append([x + length, y_node(end)]) # end position
                edges.append([[x, y_node(start)], [x + length, y_node(end)]])
                # this can be removed (or maybe speed up the rest?
    print(time/df.shape[2], '%') # loading
    x += 0.1 # every time-unit x-value increases with 0.1
print('100%')

# Make a dictionary of edges for networkx and plotly
edge_trace = [dict(type='scatter',
                   x=[from_pos[i][0], to_pos[i][0]],
                   y=[from_pos[i][1], to_pos[i][1]],
                   mode='lines',
                   line=dict(width=.5, color='black', )) for i in range(0, len(from_pos))]

positions = from_pos.copy() # list to combine 'from' and 'to'-positions

for i in range(0, len(to_pos)):
    positions.append(to_pos[i])

# Make a dictionary of nodes for networkx and plotly
nodes = [dict(type='scatter',
              x=[positions[n][0]],
              y=[positions[n][1]],
              mode='markers',
              hoverinfo='text',
              marker=dict(color='red')) for n in range(0, len(positions))]

# Make the figure
fig = go.Figure(data=edge_trace+nodes,
             layout=go.Layout(
                title='<br>Dynamic Graph Visualization',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

offline.plot(fig)
