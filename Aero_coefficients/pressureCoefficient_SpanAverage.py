#!/usr/bin/python2
import numpy as np
import pprint

## To compute the spanwise averaged pressure coefficient using the time averaged pressure data from 
## pressure_TimeAverage.py. For example, the latter is a parview batch script which extracts all the 
## pressure data on the wall (like airfoil). This script sorts the data and then average it in span direction

## the data file output from pressure_TimeAverage.py
points = open("/home/bhanu/aoa8/p0.csv", "r")
coods = []
for(i, line) in enumerate(points):
	if line != '\n' and i != 0:
		line = line.replace(',', ' ')
		line = line.split()
		line = [ float(x) for x in line ]
		coods.append(line[0:2])
points.close()
def getKey(item):
	return item[1]	
coods = sorted(coods, key=getKey)
##pprint.pprint(coods[0:400])
#for i in coods:
#	print i
X = [row[1] for row in coods]
myset1 = set(X)
##print "Number of x-coods=", len(myset)
##print sorted(myset)
##print len(myset)
Xunique = list(myset1)
for i in xrange(0, len(myset1)):
	a = Xunique[i]
	b = X.count(a)
	if b != 129:				#### change here based on span elements
		print "alert. the number of span elements arent equal"
##print coods[0][3]
ptemp = []
pmean = []
pmeantemp = []
average = 0
for k in xrange(0, len(coods)):
	coods[k][0] = 2 * coods[k][0]   ##2 because the rho is 1 and U is 1 hence dynamci pressure is 0.5 and when in numerator of Cp it will be multiplied by 2
for i in xrange(0, len(Xunique)):
	pmeantemp.append(Xunique[i])
	d = Xunique[i]
	for k in xrange(0, len(X)):
		e = X[k]
		if e == d:
			ptemp.append(coods[k][0])		
	average = sum(ptemp)/float(len(ptemp))
	pmeantemp.append(average)
	pmean.append(pmeantemp)
	pmeantemp = []
	average = 0
	ptemp = []
def getKey(item):
	return item[0]	
pmean = sorted(pmean, key=getKey)
for i in pmean:
	print i

X = []
Xunique = []

##another data file output from pressure_TimeAverage.py
points = open("/home/bhanu/aoa8/p1.csv", "r")	
coods = []
for(i, line) in enumerate(points):
	if line != '\n' and i != 0:
		line = line.replace(',', ' ')
		line = line.split()
		line = [ float(x) for x in line ]
		coods.append(line[0:2])

points.close()	
def getKey(item):
	return item[1]	
coods = sorted(coods, key=getKey)
X = [row[1] for row in coods]
myset2 = set(X)
Xunique = list(myset2)
for i in xrange(0, len(myset2)):
	a = Xunique[i]
	b = X.count(a)
	if b != 129:				#### change here based on span elements
		print "alert. the number of span elements arent equal"

ptemp = []
pmeanSS = []
pmeantemp = []
average = 0
for k in xrange(0, len(coods)):
	coods[k][0] = 2 * coods[k][0]   ##2 because the rho is 1 and U is 1 hence dynamci pressure is 0.5 and when in numerator of Cp it will be multiplied by 2
for i in xrange(0, len(Xunique)):
	pmeantemp.append(Xunique[i])
	d = Xunique[i]
	for k in xrange(0, len(X)):
		e = X[k]
		if e == d:
			ptemp.append(coods[k][0])		
	average = sum(ptemp)/float(len(ptemp))
	pmeantemp.append(average)
	pmeanSS.append(pmeantemp)
	pmeantemp = []
	average = 0
	ptemp = []
def getKey(item):
	return item[0]	
pmeanSS = sorted(pmeanSS, key=getKey)
##for i in pmeanSS:
##	print i



## the output file location
fout = open("/home/bhanu/aoa8/SS.dat", "w")
for i in xrange(0, len(pmean)):
	outputline = "%8.10f %8.8f\n " %(pmean[i][0], pmean[i][1])
	##print outputline
	fout.write(outputline)
fout.close()
## another output file location
fout = open("/home/bhanu/aoa8/PS.dat", "w")
for i in xrange(0, len(pmeanSS)):
	outputline = "%8.10f %8.8f\n " %(pmeanSS[i][0], pmeanSS[i][1])
	##print outputline
	fout.write(outputline)
fout.close()
