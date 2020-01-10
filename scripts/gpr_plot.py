import os
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from gprIO_MALA import readMALA

class gprpyPlot:
    '''
    Ground penetrating radar data processing and visualization class 
    for common-offset profiles.
    '''
    def __init__(self,filename=None):
        '''
        Initialization for a gprpyProfile object. Initialization can be 
        empty or with a provided filename for the GPR data.

        INPUT:
        filename     data file name. Currently supported formats:.rd3 (MALA)
        '''
        if filename is not None:
            self.importdata(filename)
            self.showProfile()
            plt.show()          
        
    def importdata(self,filename):
        '''
        Loads .rad (MALA) data files and populates all the gprpyProfile fields.
        '''
        file_name, file_ext = os.path.splitext(filename)       

        if file_ext==".rad" or file_ext==".rd3":
            self.data, self.info = readMALA(file_name)
            self.twtt = np.linspace(0,float(self.info["TIMEWINDOW"]),int(self.info["SAMPLES"]))
            self.profilePos = float(self.info["DISTANCE INTERVAL"])*np.arange(0,self.data.shape[1])
            self.velocity = None
            self.depth = None
            self.maxTopo = None
            self.minTopo = None
            self.threeD = None
            self.data_pretopo = None
            self.twtt_pretopo = None
            
        else:
            print("Can only read rad or rd3 files")
    
    # This is a helper function
    def prepProfileFig(self, yrng=None, xrng=None):
        c = 0
        traces_found = []
        trace_sample = []
        max_arr = np.zeros(2096)
        rows,cols = self.data.shape 
        for i in range(20,30, 1):
            c+=1
            sin1 = []
            prev_z = 0
            range_w =[]
            plt.subplot(10,1,c)
            for j in range(0,2096):
                sin1.append(abs(self.data[j][i]))
                range_w.append(j*0.04943)
            sin1 = array(sin1)
            peaks = np.where((sin1[1:-1] > sin1[0:-2]) * (sin1[1:-1] > sin1[2:]))[0] + 1
            for z in peaks:
                if (z-prev_z) > 20 and sin1[z] > 2000:
                    max_arr[z] = sin1[z]
            plt.plot(range_w, sin1, 'y-')
            max_idx = []
            a = np.nonzero(max_arr)[0]
            max_idx.append(a.tolist())
        
            for trace in range(750,900):
                if trace in ((max_idx[0])):
                    if trace not in traces_found:
                        traces_found.append(trace)
                        trace_sample.append(i)
                    
        print(len(traces_found))
        for i in range (len(traces_found)):
            print("trace %d first found at %d" %(traces_found[i],trace_sample[i]))

        amp = []  ## list to append average amplitude of each trace
        for i in range(rows):
            avg = 0
            for j in range(cols):
                avg+=(self.data[i][j]) ## absolute value of amplitude at each sample for all traces
            amp.append(avg/(j+1))
        trace = []
        amp_avg = []
        for i in range(len(amp)):
            if i%5 == 0:
                trace.append(i)
                amp_avg.append(amp[i])
        return traces_found, trace_sample
       
    def showProfile(self, **kwargs):
        '''
        Plots the profile using Matplotlib. 
        You need to run .show() afterward to show it 
        '''
        self.prepProfileFig(**kwargs)
        plt.show(block=False)
        
if __name__ == '__main__':
    gprpyPlot("/home/omni/Downloads/GPRPy/data/VGT/Profile_0006.rd3")