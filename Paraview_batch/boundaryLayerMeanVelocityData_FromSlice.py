## This is a python script compatible with Paraview batch
## This script generates data of mean velocity magnitude at a sliced location all along the spanwise direction
## The objective then is to obtain mean velocity to be later averaged in span and plot the boundary layer velocity profiles

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

## For this script, an openFOAM case is needed. And also only the time step folders required for generating mean velocity data, should be inside the case folder in addition
## to 0/ constant/ and system/

##update the file path here to the case folder and a dummy .OpenFOAM extension file.

a25DOpenFOAM = OpenFOAMReader(FileName='/qnap/fernando/home/bhanu/Airfoil/baseline/baseline.OpenFOAM')
a25DOpenFOAM.MeshRegions = ['internalMesh']

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()

##slicing occurs in last time step in this case 
animationScene1.GoToLast()

a25DOpenFOAM.MeshRegions = ['internalMesh', 'AirfoilSS']
a25DOpenFOAM.CellArrays = ['U', 'UMean', 'UPrime2Mean', 'grad(p)']

renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = [1544, 805]

a25DOpenFOAMDisplay = Show(a25DOpenFOAM, renderView1)
a25DOpenFOAMDisplay.ColorArrayName = [None, '']
a25DOpenFOAMDisplay.GlyphType = 'Arrow'

ColorBy(a25DOpenFOAMDisplay, ('POINTS', 'UMean'))

a25DOpenFOAMDisplay.RescaleTransferFunctionToDataRange(True)

uMeanLUT = GetColorTransferFunction('UMean')
uMeanPWF = GetOpacityTransferFunction('UMean')

slice1 = Slice(Input=a25DOpenFOAM)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]
SetActiveSource(slice1)
slice1.Triangulatetheslice = 0
slice1.SliceType.Origin = [0.999961, 8.36e-06, -0.5]
slice1.SliceType.Normal = [3.9e-05, -8.36e-06, 0.0]

slice1Display = Show(slice1, renderView1)
slice1Display.ColorArrayName = ['POINTS', 'UMean']
slice1Display.LookupTable = uMeanLUT

Hide(a25DOpenFOAM, renderView1)

slice1Display.SetScalarBarVisibility(renderView1, True)

SetActiveSource(slice1)

viewLayout1 = GetLayout()
viewLayout1.SplitHorizontal(0, 0.5)
SetActiveView(None)

spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.BlockSize = 1024L
spreadSheetView1.ViewSize = [400, 400]

viewLayout1.AssignView(2, spreadSheetView1)
slice1Display_1 = Show(slice1, spreadSheetView1)
slice1Display_1.CompositeDataSetIndex = 1

# save data
SaveData('/qnap/fernando/home/bhanu/Airfoil/data/uMeanSlicesBL/baseline/uMeanX_099.csv', proxy=slice1, Precision=6)

slice1.SliceType.Origin = [0.01120970, 0.02861100, -0.5]
slice1.SliceType.Normal = [0.0013606, 0,0010634, 0.0]

SaveData('/qnap/fernando/home/bhanu/Airfoil/data/uMeanSlicesBL/baseline/uMeanX_01.csv', proxy=slice1, Precision=6)


