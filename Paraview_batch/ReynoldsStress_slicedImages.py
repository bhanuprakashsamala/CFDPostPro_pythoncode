## This is a python script compatible with Paraview batch
## This script generates two images of Reynolds Stress at a sliced location of X = 0.95 Chord lengths and X = 2 chord lengths, 
## YZ plane images or spanwise crosssection.

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

## For this script, an openFOAM case is needed. And also only the time step folders required for generating velocity images should be inside the case folder in addition
## to 0/ constant/ and system/

##update the file path here to the case folder and a dummy .OpenFOAM extension file.
airfoilOpenFOAM = OpenFOAMReader(FileName='/qnap/fernando/home/bhanu/Airfoil/baseline/baseline.OpenFOAM')
airfoilOpenFOAM.MeshRegions = ['internalMesh']
airfoilOpenFOAM.CellArrays = ['UPrime2Mean']


animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()
##all the time step folder names are arranged in list and saved in time list
time = list(airfoilOpenFOAM.TimestepValues)
print time

renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [1544, 805]

uLUT = GetColorTransferFunction('UPrime2Mean')
uPWF = GetOpacityTransferFunction('UPrime2Mean')

airfoilOpenFOAMDisplay = Show(airfoilOpenFOAM, renderView1)
airfoilOpenFOAMDisplay.ColorArrayName = ['POINTS', 'UPrime2Mean']
airfoilOpenFOAMDisplay.LookupTable = uLUT

renderView1.ResetCamera()

ColorBy(airfoilOpenFOAMDisplay, ('POINTS', 'UPrime2Mean'))

# create a new 'Slice'
slice1 = Slice(Input=airfoilOpenFOAM)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1.SliceType.Origin = [0.95, 0.0, -0.5]

# show data in view
slice1Display = Show(slice1, renderView1)
slice1Display.ColorArrayName = ['POINTS', 'UPrime2Mean']
slice1Display.LookupTable = uLUT

# hide data in view
Hide(airfoilOpenFOAM, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)
renderView1.ResetCamera()
Hide3DWidgets(proxy=slice1)

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'UPrime2Mean'))

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

a = ["%04d" %int(time[i]) for i in range(0, len(time))]

## To label the time on every picture generated
annotateTimeFilter1 = AnnotateTimeFilter(Input=slice1)
annotateTimeFilter1Display = Show(annotateTimeFilter1, renderView1)
annotateTimeFilter1Display.WindowLocation = 'UpperCenter'
annotateTimeFilter1.Format = 'Time: %9.9f'

##Looping the script to run across all time folders in OpenFOAM case and generate Reynolds Stress mag. images
for x in xrange(0, (len(time)/10)):
	animationScene1.AnimationTime = time[10*x]
	uLUT.RescaleTransferFunction(0.0, 1.0)
	uPWF.RescaleTransferFunction(0.0, 1.0)
	slice1.SliceType.Origin = [0.95, 0.0, -0.5]
        ##update camera view parameters as required
        renderView1.CameraPosition = [2.9139260961387206, 0.10519199243495736, -0.6625439234682522]
	renderView1.CameraFocalPoint = [-43.44374845765281, 0.10519199243495736, -0.6625439234682522]
	renderView1.CameraViewUp = [0.0, 0.9999999202560829, -0.00039935927177369053]
	renderView1.CameraParallelScale = 11.998249061185744
        ##folder to save velocity images
	SaveScreenshot('/qnap/fernando/home/bhanu/Airfoil/baseline/yzplane_R/y095_'+str(x)+'.png', magnification=1, quality=100, view=renderView1)
	slice1.SliceType.Origin = [2, 0.0, -0.5]
        ##another camera angle for second set of Reynolds stress images
        renderView1.CameraPosition = [2.9139260961387206, 0.10519199243495736, -0.6625439234682522]
        renderView1.CameraFocalPoint = [-43.44374845765281, 0.10519199243495736, -0.6625439234682522]
        renderView1.CameraViewUp = [0.0, 0.9999999202560829, -0.00039935927177369053]
        renderView1.CameraParallelScale = 11.998249061185744
        SaveScreenshot('/qnap/fernando/home/bhanu/Airfoil/baseline/yzplane_R/y2_'+str(x)+'.png', magnification=1, quality=100, view=renderView1)


