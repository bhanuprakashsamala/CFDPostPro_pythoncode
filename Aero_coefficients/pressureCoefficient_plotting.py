#!/usr/env/python
import numpy as np
import pprint
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import sys

## To compute the spanwise averaged pressure coefficient using the time averaged pressure data from
## pressure_TimeAverage.py. For example, the latter is a parview batch script which extracts all the
## pressure data on the wall (like airfoil). This script sorts the data and then average it in span direction for multiple cases at once

## function to sort the data and average in span-wise direction. 
def Cp(filename):
    points = open("/home/data/Research/UPC/Articles/Airfoils/Final_graphs/Cp/%s" %filename, "r")
    coods = []
    for(i, line) in enumerate(points):
        if line != '\n' and i != 0:
            temp = []
            line = line.replace(',', ' ')
            line = line.split()
            line = [ float(x) for x in line ]
            temp.append(line[0])
            temp.append(line[2])
            coods.append(temp)
            temp = []
    points.close()
    print(len(coods))
    def getKey(item):
        return item[1]	
    coods = sorted(coods, key=getKey)
    X = [row[1] for row in coods]
    myset1 = set(X)
    myset2 = sorted(myset1)
    Xunique = list(myset2)
    for i in range(0, len(myset1)):
        a = Xunique[i]
        b = X.count(a)
        if b != 129:				#### change here based on span elements
            print("alert. the number of span elements arent equal")
    ptemp = []
    pmean = []
    pmeantemp = []
    average = 0
    for k in range(0, len(coods)):
        coods[k][0] = 2 * coods[k][0]   ##2 because the rho is 1 and U is 1 hence dynamci pressure is 0.5 and when in numerator of Cp it will be multiplied by 2
    for i in range(0, len(Xunique)):
        pmeantemp.append(Xunique[i])
        d = Xunique[i]
        for k in range(0, len(X)):
            e = X[k]
            if e == d:
                ptemp.append(coods[k][0])		
        average = sum(ptemp)/float(len(ptemp))
        pmeantemp.append(average)
        pmean.append(pmeantemp)
        pmeantemp = []
        average = 0
        ptemp = []
#       print(pmean)
    return pmean

##arguments are read from sys.argv and passed on to the above function. 

##pressure side of baseline
basePS = Cp(sys.argv[1])
##suction side of baseline
baseSS = Cp(sys.argv[2])
##pressure side of case 1
case1PS = Cp(sys.argv[3])
##suction side front zone case 1
case1SSF = Cp(sys.argv[4])
##suction side front zone case 1
case1SSB = Cp(sys.argv[5])
##Likewise for case 2 and 3. script to be modified based on number of cases. 
case2PS = Cp(sys.argv[6])
case2SSF = Cp(sys.argv[7])
case2SSB = Cp(sys.argv[8])
case3PS = Cp(sys.argv[9])
case3SSF = Cp(sys.argv[10])
case3SSB = Cp(sys.argv[11])


##plotting parameters and can be modified as per requirement
fig = go.Figure()
fig.add_trace(go.Scatter(x=[i[0] for i in basePS], y=[i[1] for i in basePS], mode='lines', name='Baseline', showlegend=True, line=dict(color='red', width=1)))
fig.add_trace(go.Scatter(x=[i[0] for i in baseSS], y=[i[1] for i in baseSS], mode='lines', name='Baseline', showlegend=False, line=dict(color='red', width=1)))
fig.add_trace(go.Scatter(x=[i[0] for i in case1PS], y=[i[1] for i in case1PS], mode='lines', name='case1', showlegend=True, line=dict(color='black', width=1, dash='dot')))
fig.add_trace(go.Scatter(x=[i[0] for i in case1SSF], y=[i[1] for i in case1SSF], mode='lines', name='case1', showlegend=False, line=dict(color='black', width=1, dash='dot')))
fig.add_trace(go.Scatter(x=[i[0] for i in case1SSB], y=[i[1] for i in case1SSB], mode='lines', name='case1', showlegend=False, line=dict(color='black', width=1, dash='dot')))
fig.add_trace(go.Scatter(x=[i[0] for i in case2PS], y=[i[1] for i in case2PS], mode='lines', name='case2', showlegend=True, line=dict(color='black', width=2)))
fig.add_trace(go.Scatter(x=[i[0] for i in case2SSF], y=[i[1] for i in case2SSF], mode='lines', name='case2', showlegend=False, line=dict(color='black', width=2)))
fig.add_trace(go.Scatter(x=[i[0] for i in case2SSB], y=[i[1] for i in case2SSB], mode='lines', name='case2', showlegend=False, line=dict(color='black', width=2)))
fig.add_trace(go.Scatter(x=[i[0] for i in case3PS], y=[i[1] for i in case3PS], mode='lines', name='case3', showlegend=True, line=dict(color='black', width=1)))
fig.add_trace(go.Scatter(x=[i[0] for i in case3SSF], y=[i[1] for i in case3SSF], mode='lines', name='case3', showlegend=False, line=dict(color='black', width=1)))
fig.add_trace(go.Scatter(x=[i[0] for i in case3SSB], y=[i[1] for i in case3SSB], mode='lines', name='case3', showlegend=False, line=dict(color='black', width=1)))



fig.update_xaxes(title_text='Chord length', tickangle = 0, title_font=dict(size=30, family='Courier', color='black'), title_standoff = 10, ticks="outside", showline=True, linewidth=2, linecolor='black', mirror = True, tickwidth=2, tickcolor='black', ticklen=10, tickfont=dict(family='Rockwell', color='black', size=20))
fig.update_yaxes(title_text='Pressure Coefficient(C<sub>p</sub>)', tickangle = 0, title_font=dict(size=30, family='Courier', color='black'), title_standoff = 10, ticks="outside", showline=True, linewidth=2, linecolor='black', mirror = True, tickwidth=2, tickcolor='black', ticklen=10, tickfont=dict(family='Rockwell', color='black', size=20))
fig.update_layout(title_text="Pressure Coefficient for different cases", title_font=dict(size = 36),title_x=0.5,
                    legend=dict(x=1, y=1, font=dict(family="Courier",size=24, color="black"), bordercolor="black", borderwidth=2))
fig.update_yaxes(autorange="reversed")
fig.show()




