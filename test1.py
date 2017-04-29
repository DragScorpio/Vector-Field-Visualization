import vtk
import os
import os.path
import sys
from Tkinter import *
#############################VTK Start stuff #####################

# VTK_DATA = "."


############################File Readers ###########################

# These files should be replaced to get the visualization of different datasets

m_reader = vtk.vtkStructuredPointsReader
m_reader.SetFileName("./ChalMag0.vtk")
m_reader.Update()
v_reader = vtk.vtkStructuredPointsReader
v_reader.SetFileName("./ChalVec0.vtk")
d_reader = vtk.vtkStructuredPointsReader
d_reader.SetFileName("./ChalDMag0.vtk")
d_reader.Update()
c_reader = vtk.vtkStructuredPointsReader
c_reader.SetFileName("./ChalCur0.vtk")
cm_reader = vtk.vtkStructuredPointsReader
cm_reader.SetFileName("./ChalCMag0.vtk")
cm_reader.Update()

############################Getting various params from the file ###########################
mags = m_reader.GetOutput()
bounds = mags.GetBounds()
x0 = bounds[0]
x1 = bounds[1]
y0 = bounds[2]
y1 = bounds[3]
z0 = bounds[4]
z1 = bounds[5]
#puts "VOLUME SIZE $x0 $x1 $y0 $y1 $z0 $z1"
range = mags.GetScalarRange()
v0 = range[0]
v1 = range[1]
#puts "DATA RANGE: $v0 $v1"

############################Getting various params from the file ###########################
magsd = d_reader.GetOutput()
ranged = magsd.GetScalarRange()
d0 = ranged[0]
d1 = ranged[1]
#puts "DATA RANGE: $v0 $v1"


############################Getting various params from the file ###########################
magsc = cm_reader.GetOutput()
rangec = magsc.GetScalarRange()
c0 = rangec[0]
c1 = rangec[1]
#puts "DATA RANGE: $v0 $v1"


############################Rendering details ###########################

style = vtk.vtkInteractorStyleTrackballCamera()
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(800, 800)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.SetInteractorStyle(style)
if(os.path.exists("save_view.py"):
	exec(open("save_view.py").read())

##########################The Bounding box Axes and the Cube######################

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(m_reader.GetOutputPort())

map_outline = vtk.vtkPolyDataMapper()
map_outline.SetInputConnection(outline.GetOutputPort())

actor_outline = vtk.vtkActor()
actor_outline.SetMapper(map_outline)
eval("actor_outline.GetProperty()").SetColor(1, 1, 1)


# The axes and cube code are taken straight out of colcube.tcl example

# a line is sent through the tube filter to make the thin cylinder
# which will be used for the axes.  The pipeline for this object
# has three stages: line -> fatline -> lineMapper
#

line = vtk.vtkLineSource()
line.SetPoint1(0, 0, 0)
line.SetPoint2(30, 0, 0)
fatline = vtk.vtkTubeFilter()
fatline.SetInputConnection(line.GetOutputPort())
fatline.SetRadius(0.15)
fatline.SetNumberOfSides(30)
lineMapper = vtk.vtkPolyDataMapper()
lineMapper.SetInputConnection(fatline.GetOutputPort())

#
# create actors for each of the axes.  Each axis uses the same lineMapper,
# and then the seperate actors are rotated and colored
#

lineXActor = vtk.vtkActor()
lineXActor.SetMapper(lineMapper)
lineXActor.GetProperty().SetColor(1, 0.2, 0.2)
lineYActor = vtk.vtkActor()
lineYActor.SetMapper(lineMapper)
lineYActor.RotateZ(90)
lineYActor.GetProperty().SetColor(0.2, 1, 0.2)
lineZActor = vtk.vtkActor()
lineZActor.SetMapper(lineMapper)
lineZActor.RotateY(-90)
lineZActor.GetProperty().SetColor(0.2, 0.2, 1)

######## the cube
#
# a cube is connected to a vtkTransformFilter which will move the cube
# around according to user input (which will modify the vtkTransform)
#
cube = vtk.vtkCubeSource()
cubeT = vtk.vtkTransform()
cubeTF = vtk.vtkTransformFilter()
cubeTF.SetTransform(cubeT)
cubeTF.SetInputConnection(cube.GetOutputPort())
cubeMapper = vtk.vtkDataSetMapper()
cubeMapper.SetInputConnection(cubeTF.GetOutputPort())
cubeActor = vtk.vtkActor()
cubeActor.SetMapper(cubeMapper)
cubeActor.SetPosition(0, 0, 0)
cubeActor.GetProperty().SetColor(1.0, 0, 0)
cubeActor.GetProperty().SetDiffuse(1.0)


########################### Actor and Graphics Stuff ###########################


ren.SetBackground(0, 0, 0)
ren.AddActor(actor_outline)
ren.AddActor(cubeActor)
ren.AddActor(lineXActor)
ren.AddActor(lineYActor)
ren.AddActor(lineZActor)




################### TK  interface Stuff ###################
root = Tk()
# Cube movement stuff
cube = Frame(root)
cube.pack()
# frame .cube
l = Label(cube, text = "Position")
l.pack(in_ = cube, side = TOP)
# label .cube.l -text "Position"
x = Scale(cube, label = "Red", from_ = x0, to = x1, resolution = 1.0, orient = HORIZONTAL, command = SetPosCol)
x.pack(in_ = cube, side = TOP)
# scale .cube.x -label "Red" -from $x0 -to $x1 -res 1.0 -orient horizontal -command SetPosCol
y = Scale(cube, label = "Green", from_ = y0, to = y1, resolution = 1.0, orient = HORIZONTAL, command = SetPosCol)
y.pack(in_ = cube, side = TOP)
# scale .cube.y -label "Green" -from $y0 -to $y1 -res 1.0 -orient horizontal -command SetPosCol
z = Scale(cube, label = "Blue", from_ = z0, to = z1, resolution = 1.0, orient = HORIZONTAL, command = SetPosCol)
z.pack(in_ = cube, side = TOP)
# scale .cube.z -label "Blue" -from $z0 -to $z1 -res 1.0 -orient horizontal -command SetPosCol

# pack .cube.l .cube.x .cube.y .cube.z -side top
# pack .cube

# Iso Value and DataSet chooser
iso = Frame(root)
iso.pack()
# frame .iso
s1 = Scale(iso, label = "ISO Value", from_ = v0, to = v1, resolution = 0.1, length = 100, orient = HORIZONTAL, command = ContourGen)
s1.pack(in_ = iso)
# scale .iso.s1 -label "ISO Value" -from $v0 -to $v1 -res 0.1 -len 100 -orient h -command ContourGen
l1 = Label(iso, text = "DataSet Chooser")
l1.pack(in_ = iso)
# label .iso.l1 -text "DataSet Chooser"
r1 = Radiobutton(iso, text = "Magnitude", variable = set, value = "vectmag", command = ChooseData)
r1.pack(in_ = iso)
# radiobutton .iso.r1 -text "Magnitude" -var set -val vectmag -command ChooseData
r2 = Radiobutton(iso, text = "Divergence", variable = set, value = "div", command = ChooseData)
r2.pack(in_ = iso)
# radiobutton .iso.r2 -text "Divergence" -var set -val div -command ChooseData
r3 = Radiobutton(iso, text = "Curl", variable = set, value = "curlmag", command = ChooseData)
r3.pack(in_ = iso)
# radiobutton .iso.r3 -text "Curl" -var set -val curlmag -command ChooseData

# pack .iso.s1
# pack .iso.l1 .iso.r1 .iso.r2 .iso.r3 
# pack .iso 


# Input Generator
inp = Frame(root)
inp.pack(side = LEFT)
# frame .inp
l1 = Label(inp, text = "Input Plane Position")
l1.pack()
# label .inp.l1 -text "Input Plane Position"
x = Scale(inp, from_ = x0, to = x1, resolution = 0.1, length = 100, orient = HORIZONTAL, variable = xPos, command = InputGen)
x.pack(in_ = inp)
# scale .inp.x -from $x0 -to $x1 -res 0.1 -len 100 -ori h -var xPos -command InputGen
y = Scale(inp, from_ = y0, to = y1, resolution = 0.1, length = 100, orient = HORIZONTAL, variable = yPos, command = InputGen)
y.pack(in_ = inp)
# scale .inp.y -from $y0 -to $y1 -res 0.1 -len 100 -ori h -var yPos -command InputGen
z = Scale(inp, from_ = z0, to = z1, resolution = 0.1, length = 100, orient = HORIZONTAL, variable = zPos, command = InputGen)
z.pack(in_ = inp)
# scale .inp.z -from $z0 -to $z1 -res 0.1 -len 100 -ori h -var zPos -command InputGen

l2 = Label(inp, text = "Input Plane Rotation")
l2.pack(in_ = inp)
# label .inp.l2 -text "Input Plane Rotation"
rotx = Scale(inp, from_ = 0, to = 180, resolution = 1, length = 100, orient = HORIZONTAL, variable = xRot, command = InputGen)
rotx.pack(in_ = inp)
# scale .inp.rotx -from 0 -to 180 -res 1 -len 100 -ori h -var xRot -command InputGen
roty = Scale(inp, from_ = 0, to = 180, resolution = 1, length = 100, orient = HORIZONTAL, variable = yRot, command = InputGen)
roty.pack(in_ = inp)
# scale .inp.roty -from 0 -to 180 -res 1 -len 100 -ori h -var yRot -command InputGen
rotz = Scale(inp, from_ = 0, to = 180, resolution = 1, length = 100, orient = HORIZONTAL, variable = zRot, command = InputGen)
rotz.pack(in_ = inp)
# scale .inp.rotz -from 0 -to 180 -res 1 -len 100 -ori h -var zRot -command InputGen

l3 = Label(inp, text = "Source Size and Resolution")
l3.pack(in_ = inp)
# label .inp.l3 -text "Source Size and Resolution"
size1 = Scale(inp, from_ = 0.1, to = 80, resolution = 0.1, length = 100, orient = HORIZONTAL, variable = size1, command = InputGen)
size1.pack(in_ = inp)
# scale .inp.size1 -from 0.1 -to 80 -res 0.1 -len 100 -ori h -var size1 -command InputGen
res1 = Scale(inp, from_ = 2, to = 80, resolution = 1, length = 100, orient = HORIZONTAL, variable = res1, command = InputGen)
res1.pack(in_ = inp)
# scale .inp.res1 -from 2 -to 80 -res 1 -len 100 -ori h -var res1 -command InputGen

# pack .inp.l3 .inp.size1 .inp.res1
# pack .inp.l1 .inp.x .inp.y .inp.z
# pack .inp.l2 .inp.rotx .inp.roty .inp.rotz

# pack .inp -side left
# Visualization Techniques

viz = Frame(root)
viz.pack()
# frame .viz
l = Label(viz, text = "Viz Technique")
# label .viz.l -text "Viz Technique"

l.pack(in_ = viz)
# pack .viz.l


g = Frame(viz)
g.pack(in_ = viz)
# frame .viz.g
l1 = Label(g, text = "Glyph")
l1.pack(in_ = g)
# label .viz.g.l1 -text "Glyph"
ck1 = Checkbutton(g, text = "Show/Hide", variable = gl, command = GlyphGen)
ck1.pack(in_ = g)
# checkbutton .viz.g.ck1 -text "Show/Hide" -var gl -command GlyphGen

l2 = Label(g, text = "Curl Glyphs")
l2.pack(in_ = g)
# label .viz.g.l2 -text "Curl Glyphs"
ck2 = Checkbutton(g, text = "Show/Hide", variable = clgl, command = ClGlyphGen)
ck2.pack(in_ = g)
# checkbutton .viz.g.ck2 -text "Show/Hide" -var clgl -command ClGlyphGen

s = Frame(viz)
s.pack(in_ = viz)
# frame .viz.s
l1 = Label(s, text = "Streams")
l1.pack(in_ = s)
# label .viz.s.l1 -text "Streams"

l2 = Label(s, text = "Length")
l2.pack(in_ = s)
# label .viz.s.l2 -text "Length"
s1 = Scale(s, from_ 1.0, to = 50.0, resolution = 0.2, length = 100, orient = HORIZONTAL, variable = prop, command = SetLen)
s1.pack(in_ = s)
# scale .viz.s.s1 -from 1.0 -to 50.0 -res 0.2 -len 100 -ori h -var prop -command SetLen 

l3 = Label(s, text = "Direction")
l3.pack(in_ = s)
# label .viz.s.l3 -text "Direction"
r1 = Radiobutton(s, text = "Front", variable = dir1, value = "forward", command = SetDir)
r1.pack(in_ = s)
# radiobutton .viz.s.r1 -text "Front" -var dir1 -val forward -command SetDir
r2 = Radiobutton(s, text = "Back", variable = dir1, value = "back", command = SetDir)
r2.pack(in_ = s)
# radiobutton .viz.s.r2 -text "Back" -var dir1 -val back -command SetDir
r3 = Radiobutton(s, text = "Both", variable = dir1, value = "both", command = SetDir)
r3.pack(in_ = s)
# radiobutton .viz.s.r3 -text "Both" -var dir1 -val both -command SetDir

ck1 = Checkbutton(s, text = "Show/Hide", variable = st, command = SetStream)
ck1.pack(in_ = s)
# checkbutton .viz.s.ck1 -text "Show/Hide" -var st -command SetStream

# pack .viz.g.l1 .viz.g.ck1 .viz.g.l2 .viz.g.ck2
# pack .viz.g

# pack .viz.s.l1 .viz.s.l2 .viz.s.s1 
# pack .viz.s.l3 .viz.s.r1 .viz.s.r2 .viz.s.r3
# pack .viz.s.ck1
# pack .viz.s
# pack .viz

saveview = Button(text = "Save Settings", command = saveView)
# button .saveview -text "Save Settings" -command saveView
saveview.pack()
# pack .saveview

def Quit():
	sys.exit()

quit = Button(text = "Quit", command = Quit)
# button .quit -text "Quit" -command {exit}
quit.pack()
# pack .quit



####### SetPosCol
#
# This is called with each modification of the scales.  The argument
# which is passed ("value") is actually ignored- the positions of all
# of the scrollbars are obtained each time (i.e. ".f.x. get")
# To set the color of the cube, we use SetColor on cubeActor.
# To move hte cube around, we alter the transform ("cubeT") which
# controls the cube's transform filter.
#

###############################End of Axes and Cube stuctures################

lut = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
lut.SetTableRange(v0, v1)

lut.SetHueRange(0.9, 0.0)
lut.SetSaturationRange(1.0, 1.0)
lut.SetAlphaRange(0.8, 0.8)
lut.Build()

########################### Contour Filter #######################
test_contour = vtk.vtkContourFilter()
test_contour.SetInputConnection(m_reader.GetOutputPort())
test_contour.SetNumberOfContours(1)
test_contour.SetValue(0, 1.0)

##############################Creating Commands for the UI####################
def SetPosCol(value):
	global x1, y1, z1, x0, y0, z0
	A = x.get()
	B = y.get()
	C = z.get()
	cubeActor.GetProperty().SetColor(1.0, 0, 0)
	cubeT.Identity()
	cubeT.Translate(A, B, C)
	reWin.Render()

def ContourGen(value):
	test_contour.SetValue(0, s1.get())
	reWin.Render()

##############################Vector Magnitude##############################

map_cont = vtk.vtkPolyDataMapper()
map_cont.SetInputConnection(test_contour.GetOutputPort())
map_cont.SetLookupTable(lut)
map_cont.SetColorModeToMapScalars()
eval(map_cont.SetScalarRange(v0, v1))

actor_cont = vtk.vtkActor()
actor_cont.SetMapper(map_cont)
color_bar = vtk.vtkScalarBarActor()
color_bar.SetLookupTable(lut)

##############################Divergence##############################
probe_div = vtk.vtkProbeFilter()
probe_div.SetInputConnection(test_contour.GetOutputPort())
probe_div.SetSourceConnection(d_reader.GetOutputPort())

lut_div = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
lut_div.SetHueRange(0.5, 0.0)
lut_div.SetSaturationRange(0.5, 0.9)
lut_div.SetAlphaRange(0.4, 0.4)
lut_div.SetTableRange(d0, d1)
lut_div.Build()
#   lut_div SetAlphaRange 0.3 0.3 
#   lut_div SetTableRange -8.0 5



map_div = vtk.vtkPolyDataMapper()
map_div.SetInputConnection(probe_div.GetOutputPort())
map_div.SetLookupTable(lut_div)
map_div.SetColorModeToMapScalars()
map_div.ScalarVisibilityOn()
   #map SetScalarRange 0 255
eval(map_div.SetScalarRange(d0, d1))

actor_div = vtk.vtkActor()
actor_div.SetMapper(map_div)
color_bar_div = vtk.vtkScalarBarActor()
color_bar_div.SetLookupTable(lut_div)


##############################Curl##############################

probe_curl = vtk.vtkProbeFilter()
probe_curl.SetInputConnection(test_contour.GetOutputPort())
probe_curl.SetSourceConnection(cm_reader.GetOutputPort())

lut_curl = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
lut_curl.SetHueRange(0.0, 0.8)
lut_curl.SetAlphaRange(0.4, 0.4)
lut_curl.SetTableRange(c0, c1)
lut_curl.Build()


map_curl = vtk.vtkPolyDataMapper()
map_curl.SetInputConnection(probe_curl.GetOutputPort())
map_curl.SetLookupTable(lut_curl)
map_curl.SetColorModeToMapScalars()
map_curl.ScalarVisibilityOn()
eval(map_curl.SetScalarRange(c0, c1))

actor_curl = vtk.vtkActor()
actor_curl.SetMapper(map_curl)
color_bar_curl = vtk.vtkScalarBarActor()
color_bar_curl.SetLookupTable(lut_curl)

############################### ImageMapToColors Module####################

# vtkImageMapToColors iMtC
#         iMtC SetLookupTable lut
#         iMtC SetInput [reader1 GetOutput]


##############################Input Generator ##############################

InputPlane = vtk.vtkPlaneSource()

InputPlane.SetOrigin(0, 0, 0)
InputPlane.SetPoint1(1, 0, 0)
InputPlane.SetPoint2(0, 1, 0)
 
InputPlaneT = vtk.vtkTransform()

def InputGen(value):
	InputPlaneT.Identity()
	InputPlaneT.Translate(x.get(), y.get(), z.get())
	InputPlaneT.RotateX(rotx.get())
	InputPlaneT.RotateY(roty.get())
	InputPlaneT.RotateZ(rotz.get())
	InputPlaneT.Translate(size1.get()/-2, size1.get()/-2, 0)

	InputPlane.SetPoint1(size1.get(), 0, 0)
	InputPlane.SetPoint2(0, size1.get(), 0)
	InputPlane.SetXResolution(res1.get())
	InputPlane.SetYResolution(res1.get())
	reWin.Render()


InputPlaneTF = vtk.vtkTransformFilter()
InputPlaneTF.SetTransform(InputPlaneT)
InputPlaneTF.SetInputConnection(InputPlane.GetOutputPort())

map_plane = vtk.vtkDataSetMapper()
map_plane.SetInputConnection(InputPlaneTF.GetOutputPort())

actor_plane = vtk.vtkActor()
actor_plane.SetMapper(map_plane)
actor_plane.SetPosition(0, 0, 0)
actor_plane.GetProperty().SetColor(1.0, 0.0, 0.0) 
actor_plane.GetProperty().SetDiffuse(1)

##############################Vector Glyphs##############################


cone = vtk.vtkConeSource()
cone.SetAngle(4)
cone.SetResolution(10)

contT = vtk.vtkTransform()
coneT.Translate(0.5, 0 0)

coneTF = vtk.vtkTransformFilter()
coneTF.SetTransform(coneT)
coneTF.SetInputConnection(cone.GetOutputPort())

probe_vect = vtk.vtkProbeFilter()
probe_vect.SetInputConnection(InputPlaneTF.GetOutputPort())
probe_vect.SetSourceConnection(v_reader.GetOutputPort())

glyphs = vtk.vtkGlyph3D()
glyphs.SetInputConnection(probe_vect.GetOutputPort())
glyphs.SetSourceConnection(coneTF.GetOutputPort())
glyphs.SetScaleFactor(0.3)
glyphs.SetScaleModeToScaleByVector()
glyphs.SetColorModeToColorByVector()


map_glyph = vtk.vtkPolyDataMapper()
map_glyph.SetInputConnection(glyphs.GetOutputPort())
eval(map_glyph.SetScalarRange(v0, v1))
map_glyph.SetLookupTable(lut_div)
 
actor_glyph = vtk.vtkActor()
actor_glyph.SetMapper(map_glyph)

##############################Curl Glyphs##############################

probe_cl = vtk.vtkProbeFilter()
probe_cl.SetInputConnection(InputPlaneTF.GetOutputPort())
probe_cl.SetSourceConnection(c_reader.GetOutputPort())

glyph_cl = vtk.vtkGlyph3D()
glyph_cl.SetInputConnection(probe_cl.GetOutputPort())
glyph_cl.SetSourceConnection(coneTF.GetOutputPort())
glyph_cl.SetScaleFactor(6)
   #glyph_cl SetScaleModeToScaleByVector
glyph_cl.SetColorModeToColorByVector()

map_cl = vtk.vtkPolyDataMapper()
map_cl.SetInputConnection(glyph_cl.GetOutputPort())
map_cl.SetColorModeToMapScalars()
map_cl.SetLookupTable(lut_curl)
eval(map_cl.SetScalarRange(v0, v1))

actor_cl = vtk.vtkActor()
actor_cl.SetMapper(map_cl)


# streamers ###################################################################
#
integ = vtk.vtkRungeKutta4()
  
streams = vtk.vtkStreamLine()
streams.SetIntegrator(integ)
streams.SetInputConnection(v_reader.GetOutputPort())
streams.SetSourceConnection(InputPlaneTF.GetOutputPort())
streams.SetMaximumPropagationTime(5.0)
streams.SetIntegrationDirectionToForward()
streams.SetIntegrationStepLength(0.1)
streams.SetStepLength(0.01)
streams.SpeedScalarsOn()
streams.SetTerminalSpeed(0.01)

def SetLen(value):
	streams.SetMaximumPropagationTime(s1.get())
	reWin.Render()

def SetDir():
	global dir1
	if dir1 == "forward":
		streams.SetIntegrationDirectionToForward()
	elif dir1 == "back":
		streams.SetIntegrationDirectionToBackward()
	elif dir1 == "both":
		streams.SetIntegrationDirectionToBothDirections()

	renWin.Render()


map_stream = vtk.vtkPolyDataMapper()
map_stream.SetInputConnection(streams.GetOutputPort())
eval(map_stream.SetScalarRange(v0, v1))
map_stream.SetLookupTable(lut)

actor_stream = vtk.vtkActor()
actor_stream.SetMapper(map_stream)

def GlyphGen():
	global gl
	if gl:
		ren.AddActor(actor_glyph)
	else:
		ren.RemoveActor(actor_glyph)

	renWin.Render()


def ClGlyphGen():
	global clgl
	if clgl:
		ren.AddActor(actor_cl)
	else:
		ren.RemoveActor(actor_cl)

	renWin.Render()


def SetStream():
	global st
	if st:
		ren.AddActor(actor_stream)
	else:
		ren.RemoveActor(actor_stream)

	renWin.Render()


def ChooseData():
	global set
	if set == "vectmag":
		ren.AddActor(actor_cont)
		ren.RemoveActor(actor_curl)
		ren.RemoveActor(actor_div)
		ren.AddActor(color_bar)
		ren.RemoveActor(color_bar_div)
		ren.RemoveActor(color_bar_curl)
	elif set == "div":
		ren.AddActor(actor_div)
		ren.RemoveActor(actor_curl)
		ren.RemoveActor(actor_cont)
		ren.AddActor(color_bar_div)
		ren.RemoveActor(color_bar)
		ren.RemoveActor(color_bar_curl)
	elif set == "curlmag":
		ren.AddActor(actor_curl)
		ren.RemoveActor(actor_cont)
		ren.RemoveActor(actor_div)
		ren.AddActor(color_bar_curl)
		ren.RemoveActor(color_bar)
		ren.RemoveActor(color_bar_div)

	renWin.Render()


def saveView():
	global xPos 
	global yPos 
	global zPos 
	global xRot 
	global yRot 
	global zRot
	global size1
	global res1

	chan = open("save_view.py", 'w']
	cam = ren.GetActiveCamera()
#    puts $chan "set cam \[ren GetActiveCamera\]"
	chan.wirte("cam = ren.GetActiveCamera()\n")
#    puts $chan [format "\$cam SetPosition %s" [$cam GetPosition]]
	chan.write("cam.SetPosition({})\n".format(cam.GetPosition()))
#    puts $chan [format "\$cam SetViewUp %s" [$cam GetViewUp]]
	chan.write("cam.SetViewUp({})\n".format(cam.GetViewUp()))
#    puts $chan [format "\$cam SetFocalPoint %s" [$cam GetFocalPoint]]
	chan.write("cam.SetFocalPoint({})\n".format(cam.GetFocalPoint()))
#    puts $chan [format "\$cam SetViewAngle %s" [$cam GetViewAngle]]
	chan.write("cam.SetViewAngle({})\n".format(cam.GetViewAngle()))
#    puts $chan [format "renWin SetSize %s" [renWin GetSize]]
	chan.write("ren.SetSize({})\n".format(renWin.GetSize()))
#    puts $chan "ren ResetCameraClippingRange"
	chan.write("ren.ResetCameraClippingRange()\n")
#    puts $chan "set xPos $xPos"  
	chan.write("xPos = {:f}\n".format(xPos))
#    puts $chan "set yPos $yPos" 
	chan.write("yPos = {:f}\n".format(yPos))
#    puts $chan "set zPos $zPos" 
	chan.write("zPos = {:f}\n".format(zPos))
#    puts $chan "set xRot $xRot"
	chan.write("xRot = {:f}\n".format(xRot))
#    puts $chan "set yRot $yRot"
	chan.write("yRot = {:f}\n".format(yRot))
#    puts $chan "set zRot $zRot"
	chan.write("zRot = {:f}\n".format(zRot))
#    puts $chan "set size1 $size1"
	chan.write("size1 = {:f}\n".format(size1))
#    puts $chan "set res1 $res1"
	chan.write("res1 = {:f}\n".format(res1))
#    close $chan
	chan.close()

#ren ResetCamera
renWin.Render()
