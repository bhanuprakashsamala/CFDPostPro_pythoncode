##This script takes the probes data extracted from OpenFOAM at a single point probe but varying in time (outputted from probedataExtraction_FromOpenFOAMProbes.py)
##Then computes the fast fourier transform of the data to understand the dominant natural and harmonic frequencies.
##In addition a line with -5/3 slope can be plotted from log.dat file below to compare the inertial range dissipation slope line. 

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import sys
from scipy.fft import fft, fftfreq, ifft

filename = sys.argv[1]



df1 = pd.read_csv("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/energy_spec/%s" %filename,sep="\s+", header=None)
df2 = pd.read_csv("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/energy_spec/log.dat" ,sep="\s+", header=None)
print(df1.shape[0])

#number of samples
N = df1.shape[0]
t = 0.0002  ## Time step used in the simulation or the time difference between any two adjacent time steps


print(df1[1])
print(df1[1].values)


yf = fft(df1[1].values)
xf = fftfreq(N, t)
yinv = ifft(yf)
print(yf)
print(yinv)


## plot commands. colors, line width, font sizes etc. can be modified as required
fig = go.Figure()
fig.add_trace(go.Scatter(x = xf, y = np.abs(yf), mode='lines', name='Probe 190', line=dict(color='red', width=1)))
fig.add_trace(go.Scatter(x= df2[0], y=df2[1], mode='lines', name='base', line=dict(color='black', width=1)))
fig.update_xaxes(title_text='Frequency', tickangle = 0, title_font=dict(size=30, family='Courier', color='black'), title_standoff = 10, ticks="outside", range = [0,2], showline=True, linewidth=2, linecolor='black', mirror = True, tickwidth=2, tickcolor='black', ticklen=10, tickfont=dict(family='Rockwell', color='black', size=20), type="log") 
fig.update_yaxes(title_text='Signal amplitude', tickangle = 0, title_font=dict(size=30, family='Courier', color='black'), title_standoff = 10, ticks="outside", showline=True, linewidth=2, linecolor='black', mirror = True, tickwidth=2, tickcolor='black', ticklen=10, tickfont=dict(family='Rockwell', color='black', size=20), type="log")
fig.update_layout(title_text="Energy spectrum", title_font=dict(size = 36),title_x=0.5, 
                    legend=dict(x=1, y=1, font=dict(family="Courier",size=24, color="black"), bordercolor="black", borderwidth=2))
fig.show()



