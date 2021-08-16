import numpy as np
# script to load label dictunary to labels

def Dect2Mat(LabelDict,TimeResoutionPerSec = 20,RecTime=10):
    keys = list(LabelDict.keys())
    OutputLabel = np.zeros((len(keys),TimeResoutionPerSec*RecTime))
    for i,TimeIndex in enumerate( LabelDict.values()):
        for k in range(0,len(TimeIndex),2):
            Start = int(np.round(TimeIndex[k]*TimeResoutionPerSec))
            End = int(np.round(TimeIndex[k+1]*TimeResoutionPerSec))
            OutputLabel[i,Start:End] = 1
    
    return OutputLabel,keys
    
def PlotLabels(OutputLabel,keys,TimeResoutionPerSec = 20 ,RecTime=10) :
    
    plt.imshow(OutputLabel,aspect='auto')
    plt.xticks(np.arange(0,TimeResoutionPerSec*RecTime+1,TimeResoutionPerSec),np.arange(RecTime))
    plt.yticks(np.arange(OutputLabel.shape[0]),keys)
