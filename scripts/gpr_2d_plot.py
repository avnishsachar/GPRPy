import numpy as np
from matplotlib import pyplot as plt
from gprIO_MALA import readMALA

def PlotProfile():
    # distance, depth = readMALA()
    distance = [2, 4, 8, 22, 50, 44]      # distance of utility from starting point
    depth = [3, 7, 34, 6, 7, 8]       # avg sample number for the trace
    plt.plot(distance, depth, 'o')
    plt.xlabel('distance (meters)')
    plt.ylabel('depth (meters)')
    plt.show()

if __name__ == '__main__':
    PlotProfile()