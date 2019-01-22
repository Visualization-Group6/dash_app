import plotly.graph_objs as go
import numpy as np
import time as t
from scripts import preProcessing as pp
from scripts import color_scales as cs
import inspect


def y_node(node):  # function to determine y-value
    return node * 2


def check_weight(data_list, min_weight, max_weight, edge_trace, colorscale, max_d, min_d):
    xlist = []
    ylist = []
    color_weight = (min_weight + max_weight) / 2
    length = 10
    for i in data_list:
        if len(xlist) > 11000:
            edge_trace.append(go.Scattergl(x=xlist, y=ylist,
                                           line=dict(width=.5,
                                                     color=cs.get_color_interleaved(color_weight, colorscale))))
            xlist = []
            ylist = []
        if min_weight < (np.log(int(i[3])) - min_d) / (max_d - min_d) <= max_weight:
            x = int(i[0]) * 0.1 - 0.1
            xlist.append(None)
            xlist.append(x)
            xlist.append(x + length)
            ylist.append(None)
            ylist.append(y_node(int(i[1])))
            ylist.append(y_node(int(i[2])))
    if len(xlist) != 0:
        edge_trace.append(go.Scattergl(x=xlist, y=ylist,
                                       line=dict(width=.5,
                                                 color=cs.get_color_interleaved(color_weight, colorscale))))
    return edge_trace


def draw_interleaved(filename, colorscale,
                     start_time=-float("inf"), end_time=float("inf"), weight_start=-float("inf"),
                     weight_end=float("inf"), start_node=0, end_node=float('inf')):
    now = t.time()
    print(t.time(), "@", inspect.currentframe().f_code.co_name, start_time, end_time, weight_start, weight_end)
    working_dir = pp.get_working_dir()
    with open(working_dir + filename, 'r') as f:
        encoded_data = f.read()
    new_data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]
    new_data = [i for i in new_data[1:] if len(i) == 4 and start_time <= int(i[0]) < end_time and
                np.exp(weight_start) <= int(i[3]) < np.exp(weight_end) and start_node <= int(
        i[2]) < end_node and start_node <= int(i[2]) < end_node]
    max_w = np.log(max([int(i[3]) for i in new_data if len(i) == 4]))
    min_w = np.log(min([int(i[3]) for i in new_data if len(i) == 4]))
    edge_trace = []
    if max_w == min_w:
        xlist = []
        ylist = []
        length = 10
        for i in new_data:
            if len(xlist) > 11000:
                edge_trace.append(go.Scattergl(x=xlist, y=ylist,
                                               line=dict(width=.5,
                                                         color=cs.get_color_interleaved(0, colorscale))))
                xlist = []
                ylist = []
            x = int(i[0]) * 0.1 - 0.1
            xlist.append(None)
            xlist.append(x)
            xlist.append(x + length)
            ylist.append(None)
            ylist.append(y_node(int(i[1])))
            ylist.append(y_node(int(i[2])))
        if len(xlist) != 0:
            edge_trace.append(go.Scattergl(x=xlist, y=ylist,
                                           line=dict(width=.5,
                                                     color=cs.get_color_interleaved(0, colorscale))))
    else:
        edge_trace = check_weight(new_data, -0.01, 0.1, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.1, 0.2, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.2, 0.3, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.3, 0.4, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.4, 0.5, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.5, 0.6, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.6, 0.7, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.7, 0.8, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.8, 0.9, edge_trace, colorscale, max_w, min_w)
        edge_trace = check_weight(new_data, 0.9, 1.0, edge_trace, colorscale, max_w, min_w)
    fig = dict(data=edge_trace,
               layout=go.Layout(
                   height=500,
                   title=filename,
                   titlefont=dict(size=16),
                   width=1000,
                   showlegend=False,
                   hovermode='closest',
                   margin=dict(b=20, l=5, r=5, t=40),
                   xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                   yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)), )
    print(t.time(), "@", inspect.currentframe().f_code.co_name, "<<<MAIN PLOTTING TOOK", t.time() - now,
          "SECONDS>>>")
    return fig
