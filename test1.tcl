
package require vtk
package require vtkinteraction

#############################VTK Start stuff #####################

set VTK_DATA "."


############################File Readers ###########################

# These files should be replaced to get the visualization of different datasets

vtkStructuredPointsReader m_reader
	m_reader SetFileName "$VTK_DATA/ChalMag0.vtk"
	m_reader Update
vtkStructuredPointsReader v_reader
        v_reader SetFileName "$VTK_DATA/ChalVec0.vtk"
vtkStructuredPointsReader d_reader
        d_reader SetFileName "$VTK_DATA/ChalDMag0.vtk"
        d_reader Update
vtkStructuredPointsReader c_reader
        c_reader SetFileName "$VTK_DATA/ChalCur0.vtk"
vtkStructuredPointsReader cm_reader
        cm_reader SetFileName "$VTK_DATA/ChalCMag0.vtk"
        cm_reader Update

############################Getting various params from the file ###########################
set mags [m_reader GetOutput]
set bounds [$mags GetBounds]
set x0 [lindex $bounds 0]
set x1 [lindex $bounds 1]
set y0 [lindex $bounds 2]
set y1 [lindex $bounds 3]
set z0 [lindex $bounds 4]
set z1 [lindex $bounds 5]
#puts "VOLUME SIZE $x0 $x1 $y0 $y1 $z0 $z1"
set range [$mags GetScalarRange]
set v0 [lindex $range 0]
set v1 [lindex $range 1]
#puts "DATA RANGE: $v0 $v1"

############################Getting various params from the file ###########################
set magsd [d_reader GetOutput]
set ranged [$magsd GetScalarRange]
set d0 [lindex $ranged 0]
set d1 [lindex $ranged 1]
#puts "DATA RANGE: $v0 $v1"


############################Getting various params from the file ###########################
set magsc [cm_reader GetOutput]
set rangec [$magsc GetScalarRange]
set c0 [lindex $rangec 0]
set c1 [lindex $rangec 1]
#puts "DATA RANGE: $v0 $v1"


############################Rendering details ###########################

vtkInteractorStyleTrackballCamera style
vtkRenderer ren
vtkRenderWindow renWin
    renWin AddRenderer ren
renWin SetSize 800 800
vtkRenderWindowInteractor iren
    iren SetRenderWindow renWin
iren SetInteractorStyle style
if {[file exists "save_view.tcl"]} {    
  source "save_view.tcl"
}


##########################The Bounding box Axes and the Cube######################

vtkOutlineFilter outline
    outline SetInputConnection [m_reader GetOutputPort]

vtkPolyDataMapper map_outline
    map_outline SetInputConnection [outline GetOutputPort]

vtkActor actor_outline
    actor_outline SetMapper map_outline
    eval [actor_outline GetProperty] SetColor 1 1 1


# The axes and cube code are taken straight out of colcube.tcl example

# a line is sent through the tube filter to make the thin cylinder
# which will be used for the axes.  The pipeline for this object
# has three stages: line -> fatline -> lineMapper
#

vtkLineSource line
   line SetPoint1 0 0 0
   line SetPoint2 30 0 0
vtkTubeFilter fatline
fatline SetInputConnection [line GetOutputPort]
   fatline SetRadius 0.15
   fatline SetNumberOfSides 30
vtkPolyDataMapper lineMapper
lineMapper SetInputConnection [fatline GetOutputPort]

#
# create actors for each of the axes.  Each axis uses the same lineMapper,
# and then the seperate actors are rotated and colored
#

vtkActor lineXActor
   lineXActor SetMapper lineMapper
[lineXActor GetProperty] SetColor 1 0.2 0.2
vtkActor lineYActor
   lineYActor SetMapper lineMapper
   lineYActor RotateZ 90
[lineYActor GetProperty] SetColor 0.2 1 0.2
vtkActor lineZActor
   lineZActor SetMapper lineMapper
   lineZActor RotateY -90
[lineZActor GetProperty] SetColor 0.2 0.2 1

######## the cube
#
# a cube is connected to a vtkTransformFilter which will move the cube
# around according to user input (which will modify the vtkTransform)
#
vtkCubeSource cube
vtkTransform cubeT
vtkTransformFilter cubeTF
cubeTF SetTransform cubeT
cubeTF SetInputConnection [cube GetOutputPort]
vtkDataSetMapper cubeMapper
cubeMapper SetInputConnection [cubeTF GetOutputPort]
vtkActor cubeActor
   cubeActor SetMapper cubeMapper
   cubeActor SetPosition 0 0 0
[cubeActor GetProperty] SetColor 1.0 0 0
[cubeActor GetProperty] SetDiffuse 1.0


########################### Actor and Graphics Stuff ###########################


ren SetBackground 0 0 0
ren AddActor actor_outline
ren AddActor cubeActor
ren AddActor lineXActor
ren AddActor lineYActor
ren AddActor lineZActor




################### TK  interface Stuff ###################

# Cube movement stuff

frame .cube
label .cube.l -text "Position"
scale .cube.x -label "Red" -from $x0 -to $x1 -res 1.0 -orient horizontal -command SetPosCol
scale .cube.y -label "Green" -from $y0 -to $y1 -res 1.0 -orient horizontal -command SetPosCol
scale .cube.z -label "Blue" -from $z0 -to $z1 -res 1.0 -orient horizontal -command SetPosCol


pack .cube.l .cube.x .cube.y .cube.z -side top
pack .cube

# Iso Value and DataSet chooser

frame .iso
scale .iso.s1 -label "ISO Value" -from $v0 -to $v1 -res 0.1 -len 100 -orient h -command ContourGen

label .iso.l1 -text "DataSet Chooser"

radiobutton .iso.r1 -text "Magnitude" -var set -val vectmag -command ChooseData
radiobutton .iso.r2 -text "Divergence" -var set -val div -command ChooseData
radiobutton .iso.r3 -text "Curl" -var set -val curlmag -command ChooseData


pack .iso.s1
pack .iso.l1 .iso.r1 .iso.r2 .iso.r3 
pack .iso 


# Input Generator

frame .inp
label .inp.l1 -text "Input Plane Position"
scale .inp.x -from $x0 -to $x1 -res 0.1 -len 100 -ori h -var xPos -command InputGen
scale .inp.y -from $y0 -to $y1 -res 0.1 -len 100 -ori h -var yPos -command InputGen
scale .inp.z -from $z0 -to $z1 -res 0.1 -len 100 -ori h -var zPos -command InputGen

label .inp.l2 -text "Input Plane Rotation"
scale .inp.rotx -from 0 -to 180 -res 1 -len 100 -ori h -var xRot -command InputGen
scale .inp.roty -from 0 -to 180 -res 1 -len 100 -ori h -var yRot -command InputGen
scale .inp.rotz -from 0 -to 180 -res 1 -len 100 -ori h -var zRot -command InputGen

label .inp.l3 -text "Source Size and Resolution"
scale .inp.size1 -from 0.1 -to 80 -res 0.1 -len 100 -ori h -var size1 -command InputGen
scale .inp.res1 -from 2 -to 80 -res 1 -len 100 -ori h -var res1 -command InputGen

pack .inp.l3 .inp.size1 .inp.res1
pack .inp.l1 .inp.x .inp.y .inp.z
pack .inp.l2 .inp.rotx .inp.roty .inp.rotz

pack .inp -side left
# Visualization Techniques

frame .viz
label .viz.l -text "Viz Technique"

pack .viz.l


frame .viz.g
label .viz.g.l1 -text "Glyph"
checkbutton .viz.g.ck1 -text "Show/Hide" -var gl -command GlyphGen

label .viz.g.l2 -text "Curl Glyphs"
checkbutton .viz.g.ck2 -text "Show/Hide" -var clgl -command ClGlyphGen


frame .viz.s
label .viz.s.l1 -text "Streams"

label .viz.s.l2 -text "Length"
scale .viz.s.s1 -from 1.0 -to 50.0 -res 0.2 -len 100 -ori h -var prop -command SetLen 

label .viz.s.l3 -text "Direction"
radiobutton .viz.s.r1 -text "Front" -var dir1 -val forward -command SetDir
radiobutton .viz.s.r2 -text "Back" -var dir1 -val back -command SetDir
radiobutton .viz.s.r3 -text "Both" -var dir1 -val both -command SetDir

checkbutton .viz.s.ck1 -text "Show/Hide" -var st -command SetStream

pack .viz.g.l1 .viz.g.ck1 .viz.g.l2 .viz.g.ck2
pack .viz.g


pack .viz.s.l1 .viz.s.l2 .viz.s.s1 
pack .viz.s.l3 .viz.s.r1 .viz.s.r2 .viz.s.r3
pack .viz.s.ck1
pack .viz.s
pack .viz

button .saveview -text "Save Settings" -command saveView
pack .saveview

button .quit -text "Quit" -command {exit}
pack .quit



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

vtkLookupTable lut
	lut SetNumberOfColors 256
        lut SetTableRange $v0 $v1

	lut SetHueRange 0.9 0.0
	lut SetSaturationRange 1.0  1.0
        lut SetAlphaRange 0.8 0.8
	lut Build

########################### Contour Filter #######################
vtkContourFilter test_contour
	test_contour SetInputConnection [m_reader GetOutputPort]
	test_contour SetNumberOfContours 1
	test_contour SetValue 0 1.0

##############################Creating Commands for the UI####################

proc SetPosCol {value} {
    global x1 y1 z1 x0 y0 z0
    set A [expr [.cube.x get]]
    set B [expr [.cube.y get]]
    set C [expr [.cube.z get]]
    [cubeActor GetProperty] SetColor 1.0 0 0
    cubeT Identity
    cubeT Translate [expr $A] [expr $B] [expr $C]
    renWin Render
}


proc ContourGen {value} {
    test_contour SetValue 0 [expr [.iso.s1 get]]
    renWin Render
}

##############################Vector Magnitude##############################

vtkPolyDataMapper map_cont
	map_cont SetInputConnection [test_contour GetOutputPort]
	map_cont SetLookupTable lut
	map_cont SetColorModeToMapScalars
	eval map_cont SetScalarRange $v0 $v1

vtkActor actor_cont
actor_cont SetMapper map_cont
vtkScalarBarActor color_bar
color_bar SetLookupTable lut



##############################Divergence##############################
vtkProbeFilter probe_div
	probe_div SetInputConnection [test_contour GetOutputPort]
	probe_div SetSourceConnection [d_reader GetOutputPort]

vtkLookupTable lut_div
lut SetNumberOfColors 256
lut_div SetHueRange 0.5 0.0
lut_div SetSaturationRange 0.5 0.9
lut_div SetAlphaRange 0.4 0.4
lut_div SetTableRange $d0 $d1
lut_div Build
#   lut_div SetAlphaRange 0.3 0.3 
#   lut_div SetTableRange -8.0 5



vtkPolyDataMapper map_div
    map_div SetInputConnection [probe_div GetOutputPort]
    map_div SetLookupTable lut_div
    map_div SetColorModeToMapScalars
    map_div ScalarVisibilityOn
   #map SetScalarRange 0 255
    eval map_div SetScalarRange $d0 $d1

vtkActor actor_div
   actor_div SetMapper map_div
vtkScalarBarActor color_bar_div
color_bar_div SetLookupTable lut_div


##############################Curl##############################

vtkProbeFilter probe_curl 
	probe_curl SetInputConnection [test_contour GetOutputPort]
	probe_curl SetSourceConnection [cm_reader GetOutputPort]

vtkLookupTable lut_curl
lut SetNumberOfColors 256
lut_curl SetHueRange 0.0 0.8
lut_curl SetAlphaRange 0.4 0.4
lut_curl SetTableRange $c0 $c1
lut_curl Build


vtkPolyDataMapper map_curl
    map_curl SetInputConnection [probe_curl GetOutputPort]
    map_curl SetLookupTable lut_curl
    map_curl SetColorModeToMapScalars
    map_curl ScalarVisibilityOn
    eval map_curl SetScalarRange $c0 $c1

vtkActor actor_curl
   actor_curl SetMapper map_curl
vtkScalarBarActor color_bar_curl
color_bar_curl SetLookupTable lut_curl

############################### ImageMapToColors Module####################

# vtkImageMapToColors iMtC
#         iMtC SetLookupTable lut
#         iMtC SetInput [reader1 GetOutput]


##############################Input Generator ##############################

vtkPlaneSource InputPlane
  
   InputPlane SetOrigin 0 0 0
   InputPlane SetPoint1 1 0 0
   InputPlane SetPoint2 0 1 0
 
vtkTransform InputPlaneT

proc InputGen {value} {

   InputPlaneT Identity

   InputPlaneT Translate [expr [.inp.x get]] [expr [.inp.y get]] [expr [.inp.z get]]
   InputPlaneT RotateX [expr [.inp.rotx get]]
   InputPlaneT RotateY [expr [.inp.roty get]]
   InputPlaneT RotateZ [expr [.inp.rotz get]]
   InputPlaneT Translate [expr [.inp.size1 get]/-2] [expr [.inp.size1 get]/-2] 0

  
   InputPlane SetPoint1 [expr [.inp.size1 get]] 0 0
   InputPlane SetPoint2 0 [expr [.inp.size1 get]] 0
   InputPlane SetXResolution [expr [.inp.res1 get]]
   InputPlane SetYResolution [expr [.inp.res1 get]]

   renWin Render
}

vtkTransformFilter InputPlaneTF
  InputPlaneTF SetTransform InputPlaneT
  InputPlaneTF SetInputConnection [InputPlane GetOutputPort]

vtkDataSetMapper map_plane
   map_plane SetInputConnection [InputPlaneTF GetOutputPort]

vtkActor actor_plane
   actor_plane SetMapper map_plane
   actor_plane SetPosition 0 0 0
   [actor_plane GetProperty] SetColor 1.0 0.0 0.0 
   [actor_plane GetProperty] SetDiffuse 1

##############################Vector Glyphs##############################


vtkConeSource cone
   cone SetAngle 4
   cone SetResolution 10

vtkTransform coneT
  coneT Translate 0.5 0 0

vtkTransformFilter coneTF
  coneTF SetTransform coneT
  coneTF SetInputConnection [cone GetOutputPort]  

vtkProbeFilter probe_vect
   probe_vect SetInputConnection [InputPlaneTF GetOutputPort]
   probe_vect SetSourceConnection [v_reader GetOutputPort]

vtkGlyph3D glyphs
   glyphs SetInputConnection [probe_vect GetOutputPort]
   glyphs SetSourceConnection [coneTF GetOutputPort]
   glyphs SetScaleFactor 0.3
   glyphs SetScaleModeToScaleByVector
   glyphs SetColorModeToColorByVector


vtkPolyDataMapper map_glyph
    map_glyph SetInputConnection [glyphs GetOutputPort]
    eval map_glyph SetScalarRange $v0 $v1
    map_glyph SetLookupTable lut_div
 
vtkActor actor_glyph
    actor_glyph SetMapper map_glyph

##############################Curl Glyphs##############################

vtkProbeFilter probe_cl
  probe_cl SetInputConnection [InputPlaneTF GetOutputPort]
  probe_cl SetSourceConnection [c_reader GetOutputPort]

vtkGlyph3D glyph_cl
   glyph_cl SetInputConnection [probe_cl GetOutputPort]
   glyph_cl SetSourceConnection [coneTF GetOutputPort]
   glyph_cl SetScaleFactor 6
   #glyph_cl SetScaleModeToScaleByVector
   glyph_cl SetColorModeToColorByVector

vtkPolyDataMapper map_cl
    map_cl SetInputConnection [glyph_cl GetOutputPort]
    map_cl SetColorModeToMapScalars
    map_cl SetLookupTable lut_curl
    eval map_cl SetScalarRange $v0 $v1

vtkActor actor_cl
actor_cl SetMapper map_cl


# streamers ###################################################################
#
vtkRungeKutta4 integ
  
vtkStreamLine streams
    streams SetIntegrator integ
    streams SetInputConnection [v_reader GetOutputPort]
    streams SetSourceConnection [InputPlaneTF GetOutputPort]
    streams SetMaximumPropagationTime 5.0
    streams SetIntegrationDirectionToForward
    streams SetIntegrationStepLength 0.1
    streams SetStepLength 0.01
    streams SpeedScalarsOn
    streams SetTerminalSpeed .01

proc SetLen {value} {


    streams SetMaximumPropagationTime [expr [.viz.s.s1 get]]

renWin Render
}
 
proc SetDir {} {
 global dir1
    switch $dir1 {
	"front" {
	   streams SetIntegrationDirectionToForward
	} 

	"back" {
	    streams SetIntegrationDirectionToBackward
	}
	
	"both" {
	     streams SetIntegrationDirectionToIntegrateBothDirections
	}
    }

renWin Render
}


vtkPolyDataMapper map_stream
    map_stream SetInputConnection [streams GetOutputPort]
    eval map_stream SetScalarRange $v0 $v1
    map_stream SetLookupTable lut

vtkActor actor_stream
    actor_stream SetMapper map_stream

proc GlyphGen {} {
    global gl
    if [expr $gl] {
	ren AddActor actor_glyph
    } else {
	ren RemoveActor actor_glyph
    }
    
    renWin Render
}

proc ClGlyphGen {} {
    global clgl
    if [expr $clgl] {
	ren AddActor actor_cl
    } else {
	ren RemoveActor actor_cl
    }
    
    renWin Render
}

proc SetStream {} {
    global st
    if [expr $st] {
	ren AddActor actor_stream
    } else {
	ren RemoveActor actor_stream
    }
    
    renWin Render
}




proc ChooseData {} {
    global set

    switch $set {
	"vectmag" {
	    ren AddActor actor_cont
	    ren RemoveActor actor_curl
	    ren RemoveActor actor_div
	    ren AddActor color_bar
            ren RemoveActor color_bar_div
	    ren RemoveActor color_bar_curl
	}
	"div" {
	    ren AddActor actor_div
	    ren RemoveActor actor_curl
	    ren RemoveActor actor_cont
	    ren AddActor color_bar_div
	    ren RemoveActor color_bar
	    ren RemoveActor color_bar_curl
	}
	"curlmag" {
	    ren AddActor actor_curl
	    ren RemoveActor actor_cont
	    ren RemoveActor actor_div
	    ren AddActor color_bar_curl
	    ren RemoveActor color_bar
	    ren RemoveActor color_bar_div
	}

    }
renWin Render
}

proc saveView {} {
    global xPos 
    global yPos 
    global zPos 
    global xRot 
    global yRot 
    global zRot
    global size1
    global res1

    set chan [open "save_view.tcl" w]
    set cam [ren GetActiveCamera]
    puts $chan "set cam \[ren GetActiveCamera\]"
    puts $chan [format "\$cam SetPosition %s" [$cam GetPosition]]
    puts $chan [format "\$cam SetViewUp %s" [$cam GetViewUp]]
    puts $chan [format "\$cam SetFocalPoint %s" [$cam GetFocalPoint]]
    puts $chan [format "\$cam SetViewAngle %s" [$cam GetViewAngle]]
    puts $chan [format "renWin SetSize %s" [renWin GetSize]]
    puts $chan "ren ResetCameraClippingRange"

    puts $chan "set xPos $xPos"  
    puts $chan "set yPos $yPos" 
    puts $chan "set zPos $zPos" 
    puts $chan "set xRot $xRot"
    puts $chan "set yRot $yRot"
    puts $chan "set zRot $zRot"
    puts $chan "set size1 $size1"
    puts $chan "set res1 $res1"
    close $chan
}

#ren ResetCamera
renWin Render



