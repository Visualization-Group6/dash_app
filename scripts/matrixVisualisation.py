import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import offline
from scripts import dataSelection as ds


class AdjacencyMatrix:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}


    def get_data(self, min_time=0, max_time=float("inf")):
        self.x = []
        self.data = {}
        self.weight = []
        matrix, self.mintime, self.maxtime = ds.aggravate(self.filename, max_time=max_time, min_time=min_time)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i,j] != 0:
                    self.data[i,j] = matrix[i,j]
                    self.x.append(i)
                    self.weight.append(matrix[i,j])


    def draw_plot(self, colorscale=None, xrange=None, weightrange=None, timerange=None):
        if not self.data:
            self.get_data()
        if timerange:
            print(timerange)
            self.get_data(min_time=timerange[0], max_time=timerange[1])
            print(self.data)
        if self.data == {}:
            self.layout = go.Layout(hovermode='closest', height=260, margin={
                'l': 25, 'b': 17, 't': 10, 'r': 5}, xaxis=dict(range=xrange), yaxis=dict(range=xrange))
            fig = go.Figure([{'x': [], 'y': [], 'type': 'scatter', 'mode': 'markers',
                              'marker': {'colorscale': colorscale,
                                         'colorbar': {'thickness': 3, 'title': "Log"}}
                              }
                             ], layout=self.layout)
            return fig
        if not xrange:
            xrange = [min(self.x), max(self.x)]
        x = []
        y = []
        weight = []
        for coordinate in self.data:
            if weightrange:
                if self.data[coordinate] > np.exp(weightrange[0]) and self.data[coordinate] < np.exp(weightrange[1]):
                    x.append(coordinate[0])
                    y.append(coordinate[1])
                    weight.append(self.data[coordinate])
            else:
                x.append(coordinate[0])
                y.append(coordinate[1])
                weight.append(self.data[coordinate])


        self.layout = go.Layout(hovermode= 'closest', height=260,margin={
        'l': 25, 'b': 17, 't': 10, 'r': 5},xaxis=dict(range=xrange),yaxis=dict(range=xrange))
        fig = go.Figure([{'x': x,  'y': y, 'text': weight, 'type' : 'scatter', 'mode' : 'markers',
                          'marker': {'colorscale': colorscale,'color': np.log(weight),
                                     'colorbar' : {'thickness':3,'title' : "Log"}}
                          }
                         ], layout=self.layout)
        return fig

    def get_range(self):
        if not self.data:
            self.get_data()
        return [min(self.x), max(self.x)]

    def get_weight(self):
        if not self.data:
            self.get_data()
        return [int(np.log(min(self.weight))), int(np.log(max(self.weight)))]

    def get_time(self):
        if not self.data:
            self.get_data()
        return [self.mintime, self.maxtime]