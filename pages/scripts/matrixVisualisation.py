import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import offline
from pages.scripts import dataSelection as ds

def make_heatmap(filename):
    #matrix = ds.aggravate(filename)
    matrix = [[1, 20, 30], [20, 1, 60], [30, 60, 1]]
    trace = go.Heatmap(z = matrix)
    data = [trace]
    offline.plot(data, filename = 'blabla.html')
