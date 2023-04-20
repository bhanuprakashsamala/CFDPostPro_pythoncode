## This is a python script compatible with Paraview batch
## This script generates two images of pressure at a sliced location of z = -0.5 for two different camera angles (z => (0,-1) one picture for wake and another for closeup.
## Also the color scales of pressure are tried with different values for identifying the right scale

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

## For this script, an openFOAM case is needed. And also only the time step folders required for generating pressure images should be inside the case folder in addition
## to 0/ constant/ and system/
aoa8PVOpenFOAM = OpenFOAMReader(FileName='/home/bhanu/baseline/baseline.OpenFOAM')
aoa8PVOpenFOAM.MeshRegions = ['internalMesh']
aoa8PVOpenFOAM.CellArrays = ['p']

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()
##all the time step folder names are arranged in list and saved in time list
time = list(aoa8PVOpenFOAM.TimestepValues)
##animationScene1.GoToLast()

renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = [1595, 758]

aoa8PVOpenFOAMDisplay = Show(aoa8PVOpenFOAM, renderView1)
aoa8PVOpenFOAMDisplay.ColorArrayName = [None, '']
aoa8PVOpenFOAMDisplay.GlyphType = 'Arrow'

ColorBy(aoa8PVOpenFOAMDisplay, ('POINTS', 'p'))
uLUT = GetColorTransferFunction('p')
uPWF = GetOpacityTransferFunction('p')

slice1 = Slice(Input=aoa8PVOpenFOAM)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1.SliceType.Origin = [5.0, 0.0, -0.5]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

slice1Display = Show(slice1, renderView1)
slice1Display.ColorArrayName = ['POINTS', 'p']
slice1Display.LookupTable = uLUT
slice1Display.GlyphType = 'Arrow'
slice1Display.SetScalarBarVisibility(renderView1, True)

##Modification of color bar location
bar = GetScalarBar(uLUT, renderView1)
bar.Position = [0.2, 0.6]
bar.Orientation = 0

##Looping the script to run across all time folders in OpenFOAM case and generate pressure images
for x in xrange(0, len(time)):
	animationScene1.AnimationTime = time[x]
        ##color scale (-0.25, 0.25)
	uLUT.RescaleTransferFunction(-0.25, 0.25)
	uPWF.RescaleTransferFunction(-0.25, 0.25)
        ##update camera view parameters as required
	renderView1.CameraPosition = [10.5, 0.487417996229907, 101.46391431813]
	renderView1.CameraFocalPoint = [10.5, 0.487417996229907, -0.5]
	renderView1.CameraParallelScale = 5.956409440717313
	renderView1.CameraParallelProjection = 1
	a = time[x]
        ##folder to save velocity images
	SaveScreenshot('/home/bhanu/baseline/pressure/p025/p_'+str(a)+'.png', magnification=1, quality=100, view=renderView1)
        ##color scale (-0.5, 0.5)
	uLUT.RescaleTransferFunction(-0.5, 0.5)
	uPWF.RescaleTransferFunction(-0.5, 0.5)
	SaveScreenshot('/home/bhanu/baseline/pressure/p05/p_'+str(a)+'.png', magnification=1, quality=100, view=renderView1)
        ##color scale (-1, 1)
	uLUT.RescaleTransferFunction(-1, 1)
	uPWF.RescaleTransferFunction(-1, 1)
	SaveScreenshot('/home/bhanu/baseline/pressure/p1/p_'+str(a)+'.png', magnification=1, quality=100, view=renderView1)
	Hide3DWidgets(proxy=slice1)
	# zoomedpic
        ##another camera angle for second set of velocity images
        uLUT.RescaleTransferFunction(-0.25, 0.25)
        uPWF.RescaleTransferFunction(-0.25, 0.25)
	renderView1.CameraPosition = [1.8181800158288386, 0.27107255014573944, 101.46391431813]
	renderView1.CameraFocalPoint = [1.8181800158288386, 0.27107255014573944, -0.5]
	renderView1.CameraParallelScale = 1.0165505548620317
	renderView1.CameraParallelProjection = 1
	SaveScreenshot('/home/bhanu/baseline/pressure/P025/p_'+str(a)+'.png', magnification=1, quality=100, view=renderView1)
	uLUT.RescaleTransferFunction(-0.5, 0.5)
        uPWF.RescaleTransferFunction(-0.5, 0.5)
        SaveScreenshot('/home/bhanu/baseline/pressure/P05/p_'+str(a)+'.png', magnification=1, quality=100, view=renderView1)
        uLUT.RescaleTransferFunction(-1, 1)
        uPWF.RescaleTransferFunction(-1, 1)
        SaveScreenshot('/home/bhanu/baseline/pressure/P1/p_'+str(a)+'.png', magnification=1, quality=100, view=renderView1)





