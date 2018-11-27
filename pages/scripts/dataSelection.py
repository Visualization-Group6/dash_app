import numpy as np
import random


def aggravate(Array,x_min=0, x_max=None, y_min=0, y_max=None, z_min=0, z_max=None):
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
        xarrays[i] = aggravate(Array, x_min=xlist[i], x_max=xlist[i + 1])
        yarrays[i] = aggravate(Array, y_min=ylist[i], y_max=ylist[i + 1])
        zarrays[i] = aggravate(Array, z_min=zlist[i], z_max=zlist[i + 1])

    return zarrays#,yarrays,xarrays


if __name__ == '__main__':
    size = 1000
    testarray = np.zeros((size,size,size))
    for z in range(size):
        for y in range(size):
            for x in range(size):
                testarray[z][y][x] = random.randint(1,3)

    print('data filled')

    from pages.scripts import timeIt
    print(timeIt.get_average_runtime(preslice,[testarray,2],100))