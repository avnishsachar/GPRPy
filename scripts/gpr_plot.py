import os
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from gprIO_MALA import readMALA
import time
from scipy.signal import find_peaks


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
            self.samples = int(self.info["SAMPLES"])
            self.profilePos = float(self.info["DISTANCE INTERVAL"])*np.arange(0,self.data.shape[1])
            self.frequency = float(self.info["FREQUENCY"])
            self.distance_int = float(self.info["DISTANCE INTERVAL"])
            self.trace = int(self.info["LAST TRACE"])
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
        range_w = []
        traces_found = []
        trace_sample = []
        max_peaks = np.zeros(self.trace)
        for i in range(30, 40, 1):
            c+=1
            #plt.subplot(40,1,c)
            sin1 = np.array([])
            range_w =[]
            for j in range(0,self.trace):
                
                sin1 = np.append(abs(self.data[j][i]),sin1)
                range_w.append(j*self.distance_int)   
            peaks, _ = find_peaks(sin1, height=25000, threshold=70, distance=250, width=50)
            peaks = peaks.tolist()
                
            for p in peaks:
                max_peaks[p] = sin1[p]
            
            #plt.plot( range_w,max_peaks,'b-')
            max_idx = []
            a = np.nonzero(max_peaks)[0]
            max_idx.append(a.tolist())
            
            for trace in range(0,self.trace):
                if trace in ((max_idx[0])):
                    if trace not in traces_found:                
                        traces_found.append(trace)
                        trace_sample.append(float(i*0.0079))
        
        for s in range (len(traces_found)):
            traces_found[s] = traces_found[s]*self.distance_int

            print("utility found at approx distance %f m and at depth %f m" %(traces_found[s],trace_sample[s]))
        record_depth = dict(zip(traces_found, trace_sample))
        new_traces = []
        new_samples = []
        for i in sorted(record_depth.keys()):
            if (i+1)-i>2:
                print(i,record_depth[i])
                new_traces.append(i)
                new_samples.append(record_depth[i])

        print("Showing graph for all utilities")
        time.sleep(1)
        plt.bar(traces_found,trace_sample)
        plt.plot(traces_found,trace_sample,'r*')
        plt.xlabel("Distance(m)")
        plt.ylabel("depth(m)")
        plt.title("GPR Output")
        plt.show()
        return self.data, self.info
       
    def showProfile(self, **kwargs):
        '''
        Plots the profile using Matplotlib. 
        You need to run .show() afterward to show it 
        '''
        self.prepProfileFig(**kwargs)
        plt.show(block=False)
        
if __name__ == '__main__':
    gprpyPlot("/home/omni/Downloads/GPRPy/data/VGT/Profile_0006.rd3")