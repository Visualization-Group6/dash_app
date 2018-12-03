import random

import numpy as np
from scripts import preProcessing as pp


def slice_array(Array, x_min=0, x_max=None, y_min=0, y_max=None, z_min=0, z_max=None):
    return Array[z_min:z_max,y_min:y_max,x_min:x_max]


def preslice(Array,level=10):
    zlen, ylen, xlen = Array.shape
    xlist, ylist, zlist = [0], [0], [0]     #create list of cut off values
    for i in range(level):
        xlist.append(int(xlen / level * (i + 1)))
        ylist.append(int(ylen / level * (i + 1)))
        zlist.append(int(zlen / level * (i + 1)))

    xarrays = [i for i in range(level)]
    yarrays = [i for i in range(level)]
    zarrays = [i for i in range(level)]

    for i in range(level):
        xarrays[i] = slice_array(Array, x_min=xlist[i], x_max=xlist[i + 1])
        yarrays[i] = slice_array(Array, y_min=ylist[i], y_max=ylist[i + 1])
        zarrays[i] = slice_array(Array, z_min=zlist[i], z_max=zlist[i + 1])

    return zarrays#,yarrays,xarrays


def aggravate(filename, min_time=0, max_time=float("inf")):
    working_dir = pp.get_working_dir()
    with open(working_dir + filename, 'r') as f:
        encoded_data = f.read()
    new_data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]
    nodes = max([max([int(i[1]) for i in new_data[1:] if len(i) == 4]),
                 max([int(i[2]) for i in new_data[1:] if len(i) == 4])])
    project_array = np.zeros((nodes + 1, nodes + 1))
    for i in new_data[1:]:
        if len(i) == 4:
            if max_time >= int(i[0]) >= min_time:
                project_array[int(i[1]), int(i[2])] += int(i[3])
    return project_array




if __name__ == '__main__':
    size = 1000
    testarray = np.zeros((size,size,size))
    for z in range(size):
        for y in range(size):
            for x in range(size):
                testarray[z][y][x] = random.randint(1,3)

    print('data filled')

    from scripts import timeIt

    print(timeIt.get_average_runtime(preslice, [testarray, 2], 100))