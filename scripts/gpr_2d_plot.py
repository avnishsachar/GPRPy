import numpy as np
from matplotlib import pyplot as plt
from gpr_plot import gprpyPlot

def showProfile(distance, depth):
    '''
    Plots the profile using Matplotlib. 
    You need to run .show() afterward to show it 
    '''
    # distance = [2, 4, 8, 22, 50, 44]      # distance of utility from starting point
    # depth = [3, 7, 34, 6, 7, 8]       # avg sample number for the trace
    plt.plot(distance, depth, 'o')
    plt.xlabel('distance (meters)')
    plt.ylabel('depth (meters)')
    plt.show()

if __name__ == '__main__':
    gprpyplot = gprpyPlot()
    distance, depth = gprpyplot.prepProfileFig()
    showProfile(distance, depth)