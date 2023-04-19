## This is a python script compatible with Paraview batch
## Purpose: To extract data along a line normal to airfoil along all the cells in the span-wise direction, 
## for the time averaging done on the line

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

## For this script, an openFOAM case is needed 

##update the file path here to the case folder and a dummy .OpenFOAM extension file. 
airfoilOpenFOAM = OpenFOAMReader(FileName='/home/bhanu/airfoil/airfoil.OpenFOAM')
airfoilOpenFOAM.MeshRegions = ['internalMesh']

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()

## flow field data to be extracted. U = velocity
airfoilOpenFOAM.CellArrays = ['U']
animationScene1.GoToLast()

plotOverLine1 = PlotOverLine(Input=airfoilOpenFOAM,
    Source='High Resolution Line Source')

plotOverLine1.Tolerance = 2.22044604925031e-16

## 128 is number of equispaced spanwise cells. 
d = float(1)/128;
print d

z = 0
loop = float(1)/d
print loop
loop = int(loop)
print loop
for i in range(0, loop):
	z = z - d
	print z
        ##first point of the normal line to airfoil
	plotOverLine1.Source.Point1 = [0.901685, 0.0195875, z]
        ##second point of the normal line to airfoil
	plotOverLine1.Source.Point2 = [0.938115293919, 0.216241596537, z]
	plotOverLine1.Source.Resolution = 300
	temporalStatistics1 = TemporalStatistics(Input=plotOverLine1)
	temporalStatistics1.ComputeMinimum = 0
	temporalStatistics1.ComputeMaximum = 0
	temporalStatistics1.ComputeStandardDeviation = 0
        ##Path where data files along the span are stored
	SaveData('/home/bhanu/airfoil/data/'+str(z)+'.csv', proxy=temporalStatistics1, Precision=8)
