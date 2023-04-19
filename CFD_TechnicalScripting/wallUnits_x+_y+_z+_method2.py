#!/usr/bin/python3
import numpy as np
from decimal import *
import linecache
import math
import itertools
import time
from datetime import datetime

##This script computes the wall units in all directions x, y and z.
##It outputs x+, y+ and z+ maximum and minimum for a chosen boundary name in openfoam case.
##Method 2 uses wallgradient of velocity to compute wallShearStress which is further used to calculate 
##friction velocity required for wall units.

s3 = datetime.now() ## duration is recorded for functions as there is a possibility to optimize calculations
s = datetime.now()


##The openfoam Mesh folder polyMesh and its files are used in multiple code lines to obtain the physical x, y and z distances
##every cell. So direct the file openings towards polyMesh folder of interest
fboundary = open("/home/bhanu/airfoil/constant/polyMesh/boundary", "r")


#getting boundary faces number and start face from boundary file
temp = 0 
nfaces = 0
startface = 0
for(i, line) in enumerate(fboundary):
        ##the boundary name for which wall units are needed
	if (line.find('AirfoilPS')) != -1:
		temp = i
	if temp != 0:	
		if i == temp + 4:
			line = line.strip()
			line = line.replace("nFaces", "")
			line = line.strip()
			line = line.replace(";", "")
			nfaces = int(line)
			
		if i == temp + 5:
			line = line.strip()
			line = line.replace("startFace", "")
			line = line.strip()
			line = line.replace(";", "")
			startface = int(line)
print(nfaces)
print(startface)
fboundary.close()

e = datetime.now()
x = e -s 
print ("Duration for 1: ", x)

sn2=datetime.now()
fowner = open("/home/bhanu/airfoil/constant/polyMesh/owner", "r")
count = 0 #counter for 1st loop	
cells_dups = [] # list of owner faces in order with cell ids
for (i, line) in enumerate(fowner):	
	if i >= 21 + startface:
		if count < nfaces:
			cells_dups.append(int(line)) 
			count = count + 1
cells = []
for i in cells_dups: 
	if i not in cells:	
		cells.append(i) 
fowner.close()
en2 = datetime.now()
xn2 = en2 -sn2 
print ("Duration for 2: ", xn2)


sn3=datetime.now()
faceids = [[]*6 for i in range(len(cells))]
ownerids = []
neighbourids = []
with open('/home/bhanu/airfoil/constant/polyMesh/ownern') as fo:
	for _ in range(21):
		next(fo)
	for line in fo:
		ownerids.append(int(line))
with open('/home/bhanu/airfoil/constant/polyMesh/neighbourn') as fn:
	for _ in range(21):
		next(fn)
	for line in fn:
		neighbourids.append(int(line))
en3 = datetime.now()
xn3 = en3 -sn3 
print ("Duration for 3: ", xn3)

sn4 = datetime.now()
values = np.array(ownerids)
valuesn = np.array(neighbourids)
a = 0
for i in cells:
	searchval = i
	oo = np.where(values == searchval)[0]
	faceids[a].extend(oo)
	nn = np.where(valuesn == searchval)[0]
	faceids[a].extend(nn)
	a = a + 1
en4 = datetime.now()
xn4 = en4 -sn4 
print ("Duration for 3b: ", xn4)

print ("Duration net for 3 :", xn3 + xn4)


s1 = datetime.now()

parallelfaces = [[]*2 for i in range(len(faceids))]
for i in range(len(faceids)):
	for j in range(6):
		line = linecache.getline("/home/bhanu/airfoil/constant/polyMesh/faces", faceids[i][j]+ 21)
		line = line[2:-2]
		line = line.split()
		line = [ int(x) for x in line ]
		points = []
		for k in range(4):
			point = linecache.getline("/home/bhanu/airfoil/constant/polyMesh/points", line[k] + 21)
			point = point[1:-2]
			point = point.split()
			point = [ float(x) for x in point ]
			points.append(point)
		for l in range(1,4):
			if points[0][2] == points[l][2]:
				temp = 1
			else:
				temp = 0
				break
		if temp == 1:
			parallelfaces[i].append(line)
e1 = datetime.now()
x1 = e1-s1
print ("Duration for 4: ",x1)


s2 = datetime.now()

points = [[]*8 for i in range(1)]

distanceX = []
distanceY = []
distanceZ = []
for i in range(len(parallelfaces)):
	points[0] = []
	for j in range(2):
		for k in range(4):	
			point = linecache.getline("/home/bhanu/airfoil/constant/polyMesh/points", parallelfaces[i][j][k] + 21)
			point = point[1:-2]
			point = point.split()
			point = [ float(x) for x in point ]
			points[0].append(point)
	for l in range(4):
		for m in range(4,8):
			if points[0][l][0] == points [0][m][0] and points[0][l][1] == points[0][m][1]:
				if m == l + 4:
					break
				else:
					temp = points[0][l+4]
					points[0][l+4] = points[0][m]
					points[0][m] = temp
	distanceXtemp = []
	distanceYtemp = []
	distanceZtemp = []
	for n in range(0, 8, 2):
		a = np.array(points[0][n])
		b = np.array(points[0][n+1])
		distanceXtemp.append(np.linalg.norm(a-b))
	distanceX.append(sum(distanceXtemp)/float(len(distanceXtemp)))
	a = np.array(points[0][0])
	b = np.array(points[0][3])
	distanceYtemp.append(np.linalg.norm(a-b))
	a = np.array(points[0][1])
	b = np.array(points[0][2])
	distanceYtemp.append(np.linalg.norm(a-b))			
	a = np.array(points[0][4])
	b = np.array(points[0][7])
	distanceYtemp.append(np.linalg.norm(a-b))
	a = np.array(points[0][5])
	b = np.array(points[0][6])
	distanceYtemp.append(np.linalg.norm(a-b))
	distanceY.append(sum(distanceYtemp)/float(len(distanceYtemp)))
	for p in range(4):
		a = np.array(points[0][p])
		b = np.array(points[0][p+4])
		distanceZtemp.append(np.linalg.norm(a-b))
	distanceZ.append(sum(distanceZtemp)/float(len(distanceZtemp)))

print("min X =", min(distanceX), "max =", max(distanceX), "avg =", sum(distanceX)/len(distanceX))
print("min Y =", min(distanceY), "max =", max(distanceY), "avg =", sum(distanceY)/len(distanceY))
print("min Z=", min(distanceZ), "max =", max(distanceZ), "avg =", sum(distanceZ)/len(distanceZ))

e2 = datetime.now()
x2 = e2 - s2
print ("Duration for 5: ", x2)

sn3 = datetime.now()

##The location of velocity gradient file to be used.
fwallshear= open("/home/bhanu/airfoil/66.75445/grad(U)", "r")

temp = 0
count = 0 
wallgradU = []
##change boundary name to required one
for(i, line) in enumerate(fwallshear):
	if (line.find('AirfoilPS')) != -1:
		temp = i
	if temp != 0:	
		if i == temp + 4:
			q = int(line)
		if i >= temp + 6:
			if count < q:
				line = line.replace("(", "")
				line = line.replace(")", "")
				line = line.split()
				numbers = [ float(x) for x in line ]
				wallgradU.append(numbers)		
				count = count+1
mag = []
for i in range(len(cells)):
	mag.append(math.sqrt( math.pow(wallgradU[i][3],2) + math.pow(wallgradU[i][4],2) + math.pow(wallgradU[i][5],2)))

wallshearstress = []
dynamicviscosity = 0.0002
for i in range(len(cells)):
	wallshearstress.append(dynamicviscosity * mag[i])
	
density = 1
frictionvelocity = [] 
for i in range(len(cells)):
	frictionvelocity.append(math.sqrt(wallshearstress[i]/density))

## update kinematic viscosity value as per physical conditions
kinematicviscosity = 0.0002
viscouslength = []
for i in range(len(cells)):
	viscouslength.append(kinematicviscosity/ float(frictionvelocity[i]))

wallunitx = []
for i in range(len(cells)):
	wallunitx.append(distanceX[i]/float(viscouslength[i]))

wallunity = []
for i in range(len(cells)):
	wallunity.append(distanceY[i]/float(viscouslength[i]))			

wallunitz = []
for i in range(len(cells)):
	wallunitz.append(distanceZ[i]/float(viscouslength[i]))



print("min wallunit X =", min(wallunitx), "max wallunit X=", max(wallunitx), "avg wallunit X=", sum(wallunitx)/len(wallunitx))
print("min wallunit Y =", min(wallunity), "max wallunit Y=", max(wallunity), "avg wallunit Y=", sum(wallunity)/len(wallunity))
print("min wallunit Z=", min(wallunitz), "max wallunit Z=", max(wallunitz), "avg wallunit Z=", sum(wallunitz)/len(wallunitz))
en3 = datetime.now()
xn3 = en3 - sn3
print ("Duration for 6:", xn3)



for i in range(len(parallelfaces)):
	for j in range(2):
		for k in range(4):
			point = linecache.getline("/home/bhanu/airfoil/constant/polyMesh/points", parallelfaces[i][j][k] + 21)
			point = point[1:-2]
			point = point.split()
			point = [ float(x) for x in point ]
			parallelfaces[i][j][k] = point
for i in parallelfaces:
	print (i)

e3 = datetime.now()
x3 = e3 - s3
print ("Duration for total: ", x3)



