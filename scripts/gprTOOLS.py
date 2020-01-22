
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