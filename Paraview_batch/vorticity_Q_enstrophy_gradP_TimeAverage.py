## This is a python script compatible with Paraview batch
## Purpose: To compute time averaging of vorticity, Q criterion, enstrophy and pressure gradient for a specific chosen time steps


from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

## For this script, an openFOAM case is needed. And also only the folders required for time averaging should be inside the case folder in addition
## to 0/ constant/ and system/

##update the file path here to the case folder and a dummy .OpenFOAM extension file.
a25DOpenFOAM = OpenFOAMReader(FileName='/home/data/Research/UPC/Articles/Airfoils/2.5D/2.5D.OpenFOAM')

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()
animationScene1.GoToLast()

##update the boundary name or if averaging is needed for internalMesh
a25DOpenFOAM.MeshRegions = ['internalMesh']

##update the field to be averaged.
a25DOpenFOAM.CellArrays = ['Q', 'vorticity', 'enstrophy', 'grad(p)']

temporalStatistics1 = TemporalStatistics(Input=a25DOpenFOAM)

temporalStatistics1.ComputeMinimum = 0
temporalStatistics1.ComputeMaximum = 0
plotData1 = PlotData(Input=temporalStatistics1)

##update the folder where the time averaged csv file should be located at
SaveData('/home/data/Research/UPC/Articles/Airfoils/2.5D/timeavs.csv', proxy=temporalStatistics1)

