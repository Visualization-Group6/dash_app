import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import offline
from scripts import dataSelection as ds



### deze is backup
def make_heatmap(filename):
    matrix = ds.aggravate(filename)
    #matrix = [[1, 20, 30], [20, 1, 60], [30, 60, 1]]
    #trace = go.Heatmap(z = matrix, )
    #data = [trace]
    data = matrix
    #offline.plot(data, filename = 'blabla.html')
    fig = [{'z':data, 'type' : 'heatmap',
                     'colorscale' : [
                                    [0, 'rgb(255, 255, 255)'],
                                    [0.0001, 'rgb(255, 255, 255)'],
                                    [0.0001, 'rgb(0,0,0)'],
                                    [1, 'rgb(0,0,0)']
                                    ],
                     }]
    offline.plot(fig)

###
def make_scatterplot(filename):
    x = list()
    y = list()
    weight = list()
    matrix = ds.aggravate(filename)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i,j] != 0:
                x.append(i)
                y.append(j)
                weight.append(matrix[i,j])

    #tickpos = []
    #ticklabels = []

    #logsteps = [i for i in range(int(np.log(min(weight))), int(np.log(max(weight))), int(np.log((max(weight)/min(weight))/6)))]
    #print(logsteps)
    #realstaps = np.exp(logsteps)
    #'tickmode':'array', 'tickvals':logsteps, 'ticktext':realstaps
    #for i in range(int(min(weight)), int(max(weight)), 1000000):
    #    tickpos.append(np.log(i))
    #    ticklabels.append(i)

    layout = go.Layout(hovermode= 'closest', height=200,margin={
    'l': 40, 'b': 17, 't': 10, 'r': 0
})
    fig = go.Figure([{'x': x,  'y': y, 'text': weight, 'type' : 'scatter', 'mode' : 'markers',
            'marker': {'color': np.log(weight),  'colorbar' : {'thickness':3,'title' : "Log"}}}], layout=layout)
    return fig


#make_scatterplot("profile_semantic_trafo_final.txt")
