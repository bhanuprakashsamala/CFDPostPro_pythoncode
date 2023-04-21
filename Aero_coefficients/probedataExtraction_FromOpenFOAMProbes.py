#!/usr/bin/python3 

##To extract probe data from the probes file outputted by openfoam inside postProcessing folder. 
##Generally users include multiple probe locations and this script helps to extract specific probe and specific component if data is a vector.

# arguments - 1 - probe Number 2- component

import sys
import numpy as np
from statsmodels.tsa.stattools import acf
from scipy.fftpack import fft

##velocity probes data
f=open("Uprobes_80_120","r")

time = []
signal = []
probeNumber = int(sys.argv[1]) #starts with 0
component = int(sys.argv[2]) # has to be 1, 2, 3 as index 0 = time
index = (probeNumber * 3) + component
for i, line in enumerate(f):
        line1 = line.strip()
        line1 = line1.replace("(", "")
        line1 = line1.replace(")", "")
        line1 = line1.split()
        time.append(float(line1[0]))
        signal.append(float(line1[index]))
f.close()

###if time is not starting from 0, the below lines subtract the minimum time value from all the list and starts from 0.
minTime = min(time)
for i in range(0,len(time)):
    time[i] -= minTime


## data output file
f=open('U_'+str(probeNumber)+'.dat', "w+")
for i in range(0, len(time)):
    f.write("%f %.11f\n" % (time[i], signal[i]))
f.close()

