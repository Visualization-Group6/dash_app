import pandas as pd
import numpy as np
import dash_html_components as html
import time
import pickle
import os
from pages.scripts import dataSelection as ds

# Petitie om dit te renamen naar enlargePenis.py

def get_working_dir():
    wdr = os.getcwd()
    dirs = wdr.split("\\")
    working_dir = "/".join(dirs[:1+dirs.index("dash_app")])
    working_dir += "/datasets/"
    return working_dir


def save_data(encoded_data, filename, content_type):
    working_dir = get_working_dir()
    with open(working_dir + filename, 'w') as f:
        f.write(encoded_data.decode())


def open_dataset(filename):
    working_dir = get_working_dir()
    with open(working_dir + filename, 'r') as f:
        encoded_data = f.read()
    print("read data")
    # process data in usable format
    new_data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]
    print("data formatted")
    # we use new_data[1:] because we want to skip the line with the title
    # check time length
    time_length = max([int(i[0]) for i in new_data[1:] if len(i) == 4])
    print("got times")
    # maybe slightly change what's below
    nodes = max([max([int(i[1]) for i in new_data[1:] if len(i) == 4]),
                 max([int(i[2]) for i in new_data[1:] if len(i) == 4])])  # finds the highest node number
    print("got nodes")
    network_data = np.empty((nodes + 1, nodes + 1, time_length + 1))  # add 1 since arrays start with 0

    for i in new_data[1:]:
        if len(i) == 4:
            # [Start, end, time] = weight
            network_data[int(i[1]), int(i[2]), int(i[0])] = int(i[3])

    print(network_data.shape)
    return pd.DataFrame({'test': [network_data[498, 486, 1]]})  # TEST
    # return pd.DataFrame({ 'test': [1,2,3]})

