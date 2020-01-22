import os
import numpy as np
import matplotlib.pyplot as plt

from gprTOOLS import dewow
from gprIO_MALA import readMALA

class gprpyProfile:
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
        self.history = ["mygpr = gp.gprpyProfile()"]
        # Initialize previous for undo
        self.previous = {}
        if filename is not None:
            self.importdata(filename)
            # self.setZeroTime(5)
            # self.dewow(10)
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
    def prepProfileFig(self, color="gray", contrast=1.0, yrng=None, xrng=None, asp=None):
        '''
        This is a helper function.
        It prepares the plot showing the processed profile data.
        
        INPUT:
        color        "gray", or "bwr" for blue-white-red,
                     or any other Matplotlib color map [default: "gray"]
        contrast     Factor to increase contrast by reducing color range.
                     [default = 1.0]
        yrng         y-axis range to show [default: None, meaning "everything"]
        xrng         x-axis range to show [default: None, meaning "everything"]
        asp          aspect ratio [default: None, meaning automatic]

        OUTPUT:
        contrast     contrast value used to prepare the figure
        color        color value used to prepare the figure
        yrng         yrng value used to prepare the figure
        xrng         xrng value used to prepare the figure
        asp          asp value used to prepare the figure
        '''
        dx=self.profilePos[3]-self.profilePos[2]
        dt=self.twtt[3]-self.twtt[2]
        stdcont = np.nanmax(np.abs(self.data)[:])       
        if self.velocity is None:
            plt.imshow(self.data,cmap=color,extent=[min(self.profilePos)-dx/2.0,
                                                    max(self.profilePos)+dx/2.0,
                                                    max(self.twtt)+dt/2.0,
                                                    min(self.twtt)-dt/2.0],
                       aspect="auto",vmin=-stdcont/contrast, vmax=stdcont/contrast)
            plt.gca().set_ylabel("two-way travel time [ns]")
            plt.gca().invert_yaxis()
            if yrng is not None:
                yrng=[np.max(yrng),np.min(yrng)]
            else:
                yrng=[np.max(self.twtt),np.min(self.twtt)]
            
        elif self.maxTopo is None:
            dy=dt*self.velocity
            plt.imshow(self.data,cmap=color,extent=[min(self.profilePos)-dx/2.0,
                                                    max(self.profilePos)+dx/2.0,
                                                    max(self.depth)+dy/2.0,
                                                    min(self.depth)-dy/2.0],
                       aspect="auto",vmin=-stdcont/contrast, vmax=stdcont/contrast)
            plt.gca().set_ylabel("depth [m]")
            plt.gca().invert_yaxis()
            if yrng is not None:
                yrng=[np.max(yrng),np.min(yrng)]
            else:
                yrng=[np.max(self.depth),np.min(self.depth)]
                
        else:
            dy=dt*self.velocity
            plt.imshow(self.data,cmap=color,extent=[min(self.profilePos)-dx/2.0,
                                                    max(self.profilePos)+dx/2.0,
                                                    self.minTopo-max(self.depth)-dy/2.0,
                                                    self.maxTopo-min(self.depth)+dy/2.0],
                    aspect="auto",vmin=-stdcont/contrast, vmax=stdcont/contrast)            
            plt.gca().set_ylabel("elevation [m]")
            if yrng is None:
                yrng=[self.minTopo-np.max(self.depth),self.maxTopo-np.min(self.depth)]
            
        if xrng is None:
            xrng=[min(self.profilePos),max(self.profilePos)]       
            print(xrng)
        if yrng is not None:
            plt.ylim(yrng)
            
        if xrng is not None:
            plt.xlim(xrng)

        if asp is not None:
            plt.gca().set_aspect(asp)

        plt.gca().get_xaxis().set_visible(True)
        plt.gca().get_yaxis().set_visible(True)                
        plt.gca().set_xlabel("distance [m]")
        plt.gca().xaxis.tick_top()
        plt.gca().xaxis.set_label_position('top')
        
        return contrast, color, yrng, xrng, asp
       
    def showProfile(self, **kwargs):
        '''
        Plots the profile using Matplotlib. 
        You need to run .show() afterward to show it 
        '''
        self.prepProfileFig(**kwargs)
        plt.show(block=False)

    # Helper Functions
    def setZeroTime(self,newZeroTime):
        '''
        Deletes all data recorded before newZeroTime and 
        sets newZeroTime to zero.
        INPUT:
        newZeroTime     The new zero-time
        '''
        # Find index of value that is nearest to newZeroTime
        zeroind = np.abs(self.twtt - newZeroTime).argmin() 
        # Cut out everything before
        self.twtt = self.twtt[zeroind:] - newZeroTime
        # Set first value to 0
        self.twtt[0] = 0
        self.data = self.data[zeroind:,:]

    def dewow(self,window):
        '''
        Subtracts from each sample along each trace an 
        along-time moving average.
        Can be used as a low-cut filter.
        INPUT:
        window     length of moving average window 
                   [in "number of samples"]
        '''
        self.data = dewow(self.data,window)

if __name__ == '__main__':
    gpr = gprpyProfile("../data/VGT/Profile_0006.rd3")
    