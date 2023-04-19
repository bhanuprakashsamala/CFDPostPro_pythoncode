## This is a python script compatible with Paraview batch
## Purpose: To compute time averaging of wallShearStress for a specific chosen time steps

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

## For this script, an openFOAM case is needed. And also only the folders required for time averaging should be inside the case folder in addition
## to 0/ constant/ and system/

##update the file path here to the case folder and a dummy .OpenFOAM extension file.
airfoilOpenFOAM = OpenFOAMReader(FileName='/home/bhanu/airfoil/airfoil.OpenFOAM')

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()
animationScene1.GoToLast()

##update the boundary name or if averaging is needed for internalMesh
airfoilOpenFOAM.MeshRegions = ['AirfoilPS']

##update the field to be averaged.
airfoilOpenFOAM.CellArrays = ['wallShearStress']

temporalStatistics1 = TemporalStatistics(Input=airfoilOpenFOAM)
temporalStatistics1.ComputeMinimum = 0
temporalStatistics1.ComputeMaximum = 0
temporalStatistics1.ComputeStandardDeviation = 0

plotData1 = PlotData(Input=temporalStatistics1)

##update the folder where the time averaged csv file should be located at
SaveData('/home/bhanu/airfoil/PSwallshear.csv', proxy=plotData1, Precision=8)
