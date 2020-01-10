import struct
import numpy as np
import re # Regular expressions
from matplotlib import pyplot as plt 
import random
from scipy.signal import medfilt

def readMALA(file_name):
    '''
    Reads the MALA .rd3 data file and the .rad header. Can also be used
    to read .rd7 files but I'm not sure if they are really organized
    the same way.

    INPUT: 
    file_name     data file name without the extension!

    OUTPUT:
    data          data matrix whose columns contain the traces
    info          dict with information from the header
    '''
    # First read header
    
    info = readGPRhdr(file_name+'.rad')
    try:
        filename = file_name + '.rd3'
        data = np.fromfile(filename, dtype=np.int16)        
    except:
        # I'm not sure what the format of rd7 is. Just assuming it's the same
        filename = file_name + '.rd7'
        data = abs(np.fromfile(filename, dtype=np.int16))
    
    nrows=int(len(data)/int(info['SAMPLES']))
    
    data1 = (np.asmatrix(data.reshape(nrows,int(info['SAMPLES'])))).transpose()
    data = data.reshape(nrows,int(info['SAMPLES']))
    # data = medfilt(data, 3)
    rows,cols = data.shape  ## rows is the number of traces and cols is the no of samples
    
    #sin1 = []
    c = 0
    cmap = plt.get_cmap('inferno')
    # print(data.shape)
    colors = cmap(np.linspace(0, 1, 51))
    # sam1 = []
    sin1 = []
    range_w = []
    c = 0

    for i in range(45, 55, 1):
        c+=1
        plt.subplot(10,1,c)
        sin1 = []
        range_w =[]
        for j in range(1000,1200):
            sin1.append(data[j][i])
            range_w.append(j)
        plt.plot(range_w, sin1, 'y-')
        # for i in range_w:
        #     range_w.append()
        # plt.plot(range_w, sin1, 'y-')
    plt.show()
    #     sin1 = []
    #     if j%1 == 0:
    #         c+=1
    #         # for i in range(425, 475):
    #         #     if i == 2:
    #         sin1 = np.append(sin1,abs(data[j][150]))
    #             # sin1 = medfilt(sin1, 3)
    #             # print(type(sin1), sin1)
    #             # plt.plot(sam1,sin1,'y-')
    #         sam1.append(j)
    #     #print(j)
    # #plt.plot(sam1,sin1,c=colors[c])
    # #print(len)
    # plt.plot(sam1,sin1,'y-')
    # plt.xlabel("traces")
    # plt.ylabel("amp")

    # plt.show()


    amp = []  ## list to append average amplitude of each trace
    for i in range(rows):
        avg = 0
        for j in range(cols):
            avg+=(data[i][j]) ## absolute value of amplitude at each sample for all traces
        amp.append(avg/(j+1))
    trace = []
    #print("amp",(amp))
    amp_avg = []
    
    print(max(amp),min(amp), amp.index(max(amp)),amp.index(min(amp)))
    for i in range(len(amp)):
        if i%5 == 0:
            trace.append(i)
            amp_avg.append(amp[i])
    
    print(len(trace))
    # plt.plot(trace,amp_avg)
    # plt.xlabel('traces')
    # plt.ylabel('amp')
    # plt.show()
    return data1,info
    
def readGPRhdr(filename):
    '''
    Reads the MALA header

    INPUT: 
    filename      file name for header with .rad extension
    
    OUTPUT:
    info          dict with information from the header
    '''
    # Read in text file
    info = {}
    with open(filename) as f:
        for line in f:
            strsp = line.split(':')
            info[strsp[0]] = strsp[1].rstrip()
    return info

if __name__ == '__main__':
    readMALA("/home/omni/GPR_omni/Profile_0006")