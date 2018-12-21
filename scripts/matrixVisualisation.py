import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import offline
from scripts import dataSelection as ds
from scripts import preProcessing as pp
import time as t
import inspect
import scipy.sparse as sc

class AdjacencyMatrix:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}


    def get_data(self, min_time=0, max_time=float("inf")):
        self.x = []
        self.data = {}
        self.weight = []
        self.matrix, self.mintime, self.maxtime = ds.aggravate(self.filename, max_time=max_time, min_time=min_time)
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if self.matrix[i,j] != 0:
                    self.data[i,j] = self.matrix[i,j]
                    self.x.append(i)
                    self.weight.append(self.matrix[i,j])


    def draw_plot(self, colorscale=None, xrange=None, weightrange=None, timerange=None):
        if not self.data:
            self.get_data()
        if timerange:
            print(t.time(), "@", inspect.currentframe().f_code.co_name, "%0", timerange)
            self.get_data(min_time=timerange[0], max_time=timerange[1])
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

    def reorder(self):
        sparse_matrix = sc.csr_matrix(self.matrix)
        index_order = sc.csgraph.reverse_cuthill_mckee(sparse_matrix) # returns order of new matrix
        index_mapping = dict()
        for i in range(len(index_order)):
            index_mapping[index_order[i]] = i


        working_dir = pp.get_working_dir()
        with open(working_dir + self.filename, 'r') as f:
            encoded_data = f.read()
        new_data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]
        reorder_x = []
        reorder_y = []
        reorder_weight = []
        for i in new_data[1:]:
            if len(i) == 4:
                reorder_x.append(index_mapping[int(i[1])])
                reorder_y.append(index_mapping[int(i[2])])
                reorder_weight.append(int(i[3]))
        reorder_layout = go.Layout(hovermode='closest', width= 800,
                            height = 800, margin={
            'l': 25, 'b': 17, 't': 10, 'r': 5})
        fig = go.Figure([{'x': reorder_x, 'y': reorder_y, 'text': reorder_weight, 'type': 'scatter', 'mode': 'markers',
                          'marker': {'color': np.log(reorder_weight),
                                     'colorbar': {'thickness': 3, 'title': "Log"}}
                          }
                         ], layout=reorder_layout)
        return fig