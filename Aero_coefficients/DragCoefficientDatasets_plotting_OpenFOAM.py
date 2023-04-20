## This is a python script to read the .dat files of force coefficients computed by OpenFOAM. 
## When multiple files are needed to be read and plotted together, this script helps to plot Drag coefficient(Cd)

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

## path to the .dat files location
dcase2 = pd.read_csv("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/Cl_Cd/baseline_slot.dat" ,sep="\s+", header=None)
#dcase3 = pd.read_csv("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/Cl_Cd/baselinev3.dat" ,sep="\s+", header=None)
df3 = pd.read_csv("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/Cl_Cd/case1.dat" ,sep="\s+", header=None)
df4 = pd.read_csv("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/Cl_Cd/case2.dat" ,sep="\s+", header=None)
df5 = pd.read_csv("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/Cl_Cd/case3.dat" ,sep="\s+", header=None)

#dftemp = (dcase3[0] - dcase3[0].min())

print(df5.shape)
print(len(df5))
print(len(df5.columns))
print(df5.size)
print(df5.info())

## This is to cut the data set as needed for plotting. (basically removing time series before required convergence criteria)
case1_xcut = 0
case2_xcut = 0
case3_xcut = 0

for i in df3[0].index:
    if(df3[0][i] > 23.68):
        case1_xcut = i
        break

for i in df4[0].index:
    if(df4[0][i] > 23.36):
        case2_xcut = i
        break

for i in df5[0].index:
    if(df5[0][i] > 20):
        case3_xcut = i
        break




## plot commands. colors, line width, font sizes etc. can be modified as required
fig = go.Figure()
fig.add_trace(go.Scatter(x=dcase2[0], y=dcase2[2], mode='lines', name='Baseline', line=dict(color='red', width=1)))
#fig.add_trace(go.Scatter(x=dftemp, y=dcase3[2], mode='lines', name='base', line=dict(color='green', width=1)))
fig.add_trace(go.Scatter(x=(df3[0][case1_xcut:] - df3[0][case1_xcut]) , y=df3[2][case1_xcut:], mode='lines', name='case2', line=dict(color='black', width=1, dash='dot')))
fig.add_trace(go.Scatter(x=(df4[0][case2_xcut:] - df4[0][case2_xcut]), y=df4[2][case2_xcut:], mode='lines', name='case3', line=dict(color='black', width=2)))
fig.add_trace(go.Scatter(x=(df5[0][case3_xcut:] - df5[0][case3_xcut]), y=df5[2][case3_xcut:], mode='lines', name='case4', line=dict(color='black', width=1)))

fig.update_xaxes(title_text='Time units(tU<sub>0</sub>/C)', tickangle = 0, title_font=dict(size=30, family='Courier', color='black'), title_standoff = 10, ticks="outside", range=[0,28], showline=True, linewidth=2, linecolor='black', mirror = True, tickwidth=2, tickcolor='black', ticklen=10, tickfont=dict(family='Rockwell', color='black', size=20)) 
fig.update_yaxes(title_text='Drag Coefficient(C<sub>d</sub>)', tickangle = 0, title_font=dict(size=30, family='Courier', color='black'), title_standoff = 10, ticks="outside", range=[0,0.2], showline=True, linewidth=2, linecolor='black', mirror = True, tickwidth=2, tickcolor='black', ticklen=10, tickfont=dict(family='Rockwell', color='black', size=20))
fig.update_layout(title_text="Drag Coefficient time series", title_font=dict(size = 36),title_x=0.5, 
                    legend=dict(x=1, y=1, font=dict(family="Courier",size=24, color="black"), bordercolor="black", borderwidth=2))



fig.show()

