import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import offline
from scripts import dataSelection as ds


class AdjacencyMatrix:
    def __init__(self, filename):
        self.x = list()
        self.y = list()
        self.weight = list()
        matrix = ds.aggravate(filename)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i,j] != 0:
                    self.x.append(i)
                    self.y.append(j)
                    self.weight.append(matrix[i,j])


    def draw_plot(self, colorscale=None, xrange=None):
        if not xrange:
            xrange = [min(self.x)-50, max(self.x)+50]
        self.layout = go.Layout(hovermode= 'closest', height=200,margin={
        'l': 40, 'b': 17, 't': 10, 'r': 20},xaxis=dict(range=xrange),yaxis=dict(range=xrange))
        fig = go.Figure([{'x': self.x,  'y': self.y, 'text': self.weight, 'type' : 'scatter', 'mode' : 'markers',
                          'marker': {'colorscale': colorscale,'color': np.log(self.weight),
                                     'colorbar' : {'thickness':3,'title' : "Log"}}
                          }
                         ], layout=self.layout)
        return fig

    def get_range(self):
        return [min(self.x), max(self.x)]