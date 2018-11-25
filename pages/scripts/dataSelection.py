import numpy as np



def aggravate(Array,x_min=0, x_max=None, y_min=0, y_max=None, z_min=0, z_max=None):
    return(Array[z_min:z_max,y_min:y_max,x_min:x_max])


def preslice(Array,level=10):
    pass


if __name__ == '__main__':
    testarray = np.zeros((10,10,10))
    for z in range(10):
        for y in range(10):
            for x in range(10):
                testarray[z][y][x] = z

    print(aggravate(testarray, z_min=1, z_max=2, y_min=2, y_max=3))
