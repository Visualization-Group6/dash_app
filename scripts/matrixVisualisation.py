import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import offline
from scripts import preProcessing as pp
from scripts import dataSelection as ds
import time as t
import scipy.sparse as sc
import inspect


class AdjacencyMatrix:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def get_data(self, min_time=0, max_time=float("inf")):
        working_dir = pp.get_working_dir()
        with open(working_dir + self.filename, 'r') as f:
            encoded_data = f.read()
        new_data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]
        times = [int(i[0]) for i in new_data[1:] if len(i) == 4]
        self.mintime = min(times)
        self.maxtime = max(times)
        self.x = [int(i[1]) for i in new_data[1:] if len(i) == 4 and min_time <= int(i[0]) < max_time]
        self.y = [int(i[2]) for i in new_data[1:] if len(i) == 4 and min_time <= int(i[0]) < max_time]
        self.weight = [int(i[3]) for i in new_data[1:] if len(i) == 4 and min_time <= int(i[0]) < max_time]
        self.data = {}
        for i in new_data[1:]:
            if len(i) == 4 and min_time <= int(i[0]) < max_time:
                if (int(i[1]), int(i[2])) in self.data:
                    self.data[int(i[1]), int(i[2])] += int(i[3])
                else:
                    self.data[int(i[1]), int(i[2])] = int(i[3])

    def draw_plot(self, colorscale=None, xrange=None, weightrange=None, timerange=None):
        now = t.time()
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
                if self.data[coordinate] >= np.exp(weightrange[0]) and self.data[coordinate] < np.exp(weightrange[1]):
                    x.append(coordinate[0])
                    y.append(coordinate[1])
                    weight.append(self.data[coordinate])
            else:
                x.append(coordinate[0])
                y.append(coordinate[1])
                weight.append(self.data[coordinate])
        self.layout = go.Layout(hovermode='closest', height=260, margin={
            'l': 25, 'b': 17, 't': 10, 'r': 5}, xaxis=dict(range=xrange), yaxis=dict(range=xrange))
        fig = go.Figure([{'x': x, 'y': y, 'text': weight, 'type': 'scatter', 'mode': 'markers',
                          'marker': {'colorscale': colorscale, 'color': np.log(weight),
                                     'colorbar': {'thickness': 3, 'title': "Log"}}
                          }
                         ], layout=self.layout)
        print(t.time(), "@", inspect.currentframe().f_code.co_name, "<<<MATRIX PLOTTING TOOK", t.time() - now,
              "SECONDS>>>")
        return fig

    def get_range(self):
        if not self.data:
            self.get_data()
        return [min(self.x), max(self.x)]

    def get_weight(self):
        if not self.data:
            self.get_data()
        if int(np.log(min(self.weight))) == int(np.log(max(self.weight))):
            return [int(np.log(min(self.weight))), int(np.log(max(self.weight))) + 1]
        return [int(np.log(min(self.weight))), int(np.log(max(self.weight)))]

    def get_time(self):
        if not self.data:
            self.get_data()
        return [self.mintime, self.maxtime]

    def reorder(self, colorscale=None, xrange=None, weightrange=None, timerange=None):
        if timerange:
            self.get_data(max_time=timerange[1], min_time=timerange[0])
        else:
            self.get_data()
        x = []
        y = []
        weight = []
        for coordinate in self.data:
            if weightrange:
                if self.data[coordinate] >= np.exp(weightrange[0]) and self.data[coordinate] < np.exp(weightrange[1]):
                    x.append(coordinate[0])
                    y.append(coordinate[1])
                    weight.append(self.data[coordinate])
            else:
                x.append(coordinate[0])
                y.append(coordinate[1])
                weight.append(self.data[coordinate])
        length = max(max(x), max(y))
        sparse_matrix = sc.csr_matrix((weight, (x, y)), shape=(length + 1, length + 1))
        index_order = sc.csgraph.reverse_cuthill_mckee(sparse_matrix)  # returns order of new matrix
        index_mapping = dict()
        index_mapping_reverse = dict()
        for i in range(len(index_order)):
            index_mapping[index_order[i]] = i
            index_mapping_reverse[i] = index_order[i]
        reorder_x = [index_mapping[i] for i in x]
        reorder_y = [index_mapping[i] for i in y]
        reorder_weight = [self.data[index_mapping_reverse[x], index_mapping_reverse[y]] for x, y in
                          zip(reorder_x, reorder_y)]

        reorder_layout = go.Layout(hovermode='closest', height=260, margin={
            'l': 25, 'b': 17, 't': 10, 'r': 5}, xaxis=dict(range=xrange), yaxis=dict(range=xrange))
        fig = go.Figure([{'x': reorder_x, 'y': reorder_y,
                          'text': [str((index_mapping_reverse[x], index_mapping_reverse[y])) + '\n' + str(weight) for
                                   x, y, weight in zip(reorder_x, reorder_y, reorder_weight)], 'type': 'scatter',
                          'mode': 'markers',
                          'hoverinfo': 'text',
                          'marker': {'colorscale': colorscale, 'color': np.log(reorder_weight),
                                     'colorbar': {'thickness': 3, 'title': "Log"}}
                          }
                         ], layout=reorder_layout)
        return fig
