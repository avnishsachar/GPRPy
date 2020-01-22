
import numpy as np
import scipy as sp
import numpy.matlib as matlib
import scipy.interpolate as interp
import scipy.signal as signal
# For progress bar
import time
from tqdm import tqdm


def dewow(data,window):
    '''
    Subtracts from each sample along each trace an 
    along-time moving average.
    Can be used as a low-cut filter.
    INPUT:
    data       data matrix whose columns contain the traces 
    window     length of moving average window 
               [in "number of samples"]
    OUTPUT:
    newdata    data matrix after dewow
    '''
    totsamps = data.shape[0]
    # If the window is larger or equal to the number of samples,
    # then we can do a much faster dewow
    if (window >= totsamps):
        newdata = data-np.matrix.mean(data,0)            
    else:
        newdata = np.asmatrix(np.zeros(data.shape))
        halfwid = int(np.ceil(window/2.0))
        
        # For the first few samples, it will always be the same
        avgsmp=np.matrix.mean(data[0:halfwid+1,:],0)
        newdata[0:halfwid+1,:] = data[0:halfwid+1,:]-avgsmp

        # for each sample in the middle
        for smp in tqdm(range(halfwid,totsamps-halfwid+1)):
            winstart = int(smp - halfwid)
            winend = int(smp + halfwid)
            avgsmp = np.matrix.mean(data[winstart:winend+1,:],0)
            newdata[smp,:] = data[smp,:]-avgsmp

        # For the last few samples, it will always be the same
        avgsmp = np.matrix.mean(data[totsamps-halfwid:totsamps+1,:],0)
        newdata[totsamps-halfwid:totsamps+1,:] = data[totsamps-halfwid:totsamps+1,:]-avgsmp
        
    print('done with dewow')
    return newdata

def profileSmooth(data,profilePos,ntraces=1,noversample=1):
    '''
    First creates copies of each trace and appends the copies 
    next to each trace, then replaces each trace with the 
    average trace over a moving average window.
    Can be used to smooth-out noisy reflectors appearing 
    in neighboring traces, or simply to increase the along-profile 
    resolution by interpolating between the traces.
    INPUT:
    data            data matrix whose columns contain the traces 
    profilePos      profile coordinates for the traces in data
    ntraces         window width [in "number of samples"]; 
                    over how many traces to take the moving average. 
    noversample     how many copies of each trace
    OUTPUT:
    newdata         data matrix after along-profile smoothing 
    newProfilePos   profile coordinates for output data matrix
    '''
    # New profile positions
    newProfilePos = np.linspace(profilePos[0],
                                profilePos[-1],
                                noversample*len(profilePos))
    # First oversample the data
    data = np.asmatrix(np.repeat(data,noversample,1))
    tottraces = data.shape[1]
    if ntraces == 1:
        newdata = data
    elif ntraces == 0:
        newdata = data
    elif ntraces >= tottraces:
        newdata=np.matrix.mean(data,1) 
    else:
        newdata = np.asmatrix(np.zeros(data.shape))    
        halfwid = int(np.ceil(ntraces/2.0))
        
        # First few traces, that all have the same average
        newdata[:,0:halfwid+1] = np.matrix.mean(data[:,0:halfwid+1],1)
        
        # For each trace in the middle
        for tr in tqdm(range(halfwid,tottraces-halfwid+1)):   
            winstart = int(tr - halfwid)
            winend = int(tr + halfwid)
            newdata[:,tr] = np.matrix.mean(data[:,winstart:winend+1],1) 

        # Last few traces again have the same average    
        newdata[:,tottraces-halfwid:tottraces+1] = np.matrix.mean(data[:,tottraces-halfwid:tottraces+1],1)

    print('done with profile smoothing')
    return newdata, newProfilePos