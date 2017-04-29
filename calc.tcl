catch {load vtktcl}
if { [catch {set VTK_TCL $env(VTK_TCL)}] != 0} { set VTK_TCL "." }
if { [catch {set VTK_DATA $env(VTK_DATA)}] != 0} { set VTK_DATA "./vtkdata" }

package require vtk
package require vtkinteraction

vtkStructuredPointsReader reader
    reader SetFileName "ChalVec1.vtk"
    reader Update

reader Update
set mags [reader GetOutput]
set bounds [$mags GetBounds]
set x0 [lindex $bounds 0]
set x1 [lindex $bounds 1]
set xdm1 [expr $x1-$x0]
set xd [expr int($x1-$x0+1)]
set y0 [lindex $bounds 2]
set y1 [lindex $bounds 3]
set ydm1 [expr $y1-$y0]
set yd [expr int($y1-$y0+1)]
set z0 [lindex $bounds 4]
set z1 [lindex $bounds 5]
set zdm1 [expr $z1-$z0]
set zd [expr int($z1-$z0+1)]
puts "DATA DIMENSIONS ARE: $xd $yd $zd"


set vecinfo [[[reader GetOutput] GetPointData] GetVectors]

vtkStructuredPoints curlData
  curlData SetDimensions $xd $yd $zd
  curlData SetSpacing 1 1 1
  curlData SetOrigin 0 0 0 

vtkStructuredPoints divData
  divData SetDimensions $xd $yd $zd
  divData SetSpacing 1 1 1
  divData SetOrigin 0 0 0 

vtkStructuredPoints curlmagData
  curlmagData SetDimensions $xd $yd $zd
  curlmagData SetSpacing 1 1 1
  curlmagData SetOrigin 0 0 0 

vtkFloatArray div
div SetNumberOfComponents 1
div SetNumberOfTuples [expr $xd*$yd*$zd]
vtkFloatArray curl
curl SetNumberOfComponents 3
curl SetNumberOfTuples [expr $xd*$yd*$zd]
vtkFloatArray curlmag
curlmag SetNumberOfComponents 1
curlmag SetNumberOfTuples [expr $xd*$yd*$zd]


for {set k 0} {$k < $zd} {incr k} {
  for {set j 0} {$j < $yd} {incr j} {
    for {set i 0} {$i < $xd } {incr i} {
      set index [expr ($i + ($xd * $j) + ($xd * $yd * $k))]
	
      if { (($i == 0) || ($j == 0) || ($k == 0) || ($i == $xdm1) || ($j == $ydm1) || ($k == $zdm1))} {
	  div SetTuple1 $index 0.0
	  curl SetTuple3 $index 0.0 0.0 0.0
	  curlmag SetTuple1 $index 0.0
      } else {
   
        set idxminus1 [expr (($i - 1) + ($xd * $j) + ($xd * $yd * $k))]
        set idxplus1 [expr  (($i + 1) + ($xd * $j) + ($xd * $yd * $k))]
        set idyminus1 [expr ($i + ($xd * ($j - 1)) + ($xd * $yd * $k))]
        set idyplus1 [expr  ($i + ($xd * ($j + 1)) + ($xd * $yd * $k))]
        set idzminus1 [expr ($i + ($xd * $j) + ($xd * $yd * ($k - 1)))]
        set idzplus1 [expr  ($i + ($xd * $j) + ($xd * $yd * ($k + 1)))]

        # Get the points to work with
        
          set xxm1 [$vecinfo GetComponent $idxminus1 0]
          set yxm1 [$vecinfo GetComponent $idxminus1 1]
          set zxm1 [$vecinfo GetComponent $idxminus1 2]

          set xym1 [$vecinfo GetComponent $idyminus1 0]
          set yym1 [$vecinfo GetComponent $idyminus1 1]
          set zym1 [$vecinfo GetComponent $idyminus1 2]

          set xzm1 [$vecinfo GetComponent $idzminus1 0]
          set yzm1 [$vecinfo GetComponent $idzminus1 1]
          set zzm1 [$vecinfo GetComponent $idzminus1 2]

          set xxp1 [$vecinfo GetComponent $idxplus1 0]
          set yxp1 [$vecinfo GetComponent $idxplus1 1]
          set zxp1 [$vecinfo GetComponent $idxplus1 2]

          set xyp1 [$vecinfo GetComponent $idyplus1 0]
          set yyp1 [$vecinfo GetComponent $idyplus1 1]
          set zyp1 [$vecinfo GetComponent $idyplus1 2]

          set xzp1 [$vecinfo GetComponent $idzplus1 0]
          set yzp1 [$vecinfo GetComponent $idzplus1 1]
          set zzp1 [$vecinfo GetComponent $idzplus1 2]


        # Calculate divergence
        set dxx [expr ($xxp1 - $xxm1)/2]
        set dyy [expr ($yyp1 - $yym1)/2]
        set dzz [expr ($zzp1 - $zzm1)/2]

        # Calculate curl
        set dzy [expr ($zyp1 - $zym1)/2]
        set dyz [expr ($yzp1 - $yzm1)/2]
        set dxz [expr ($xzp1 - $xzm1)/2]
        set dzx [expr ($zxp1 - $zxm1)/2]
        set dyx [expr ($yxp1 - $yxm1)/2]
        set dxy [expr ($xyp1 - $xym1)/2]

        set x [expr $dzy - $dyz]
        set y [expr $dxz - $dzx]
        set z [expr $dyx - $dxy]
      
        div SetTuple1 $index [expr $dxx + $dyy + $dzz]
        curl SetTuple3 $index $x $y $z

	# Calculate curl magnitude
        curlmag SetTuple1 $index [expr sqrt($x*$x + $y*$y + $z*$z)]

     }
    }
  }
  puts "JUST DID VOXEL: $k $j $i $index"
}

  [divData GetPointData] SetScalars div
  [curlData GetPointData] SetVectors curl
  [curlmagData GetPointData] SetScalars curlmag

# create a writer, to save information to a file
vtkStructuredPointsWriter writeDiv
    writeDiv SetFileName "./ChalDMag0.vtk"
    writeDiv SetFileTypeToBinary 
    writeDiv SetInputData divData
    writeDiv Write

vtkStructuredPointsWriter writeCurl
    writeCurl SetFileName "./ChalCur0.vtk"
    writeCurl SetFileTypeToBinary 
    writeCurl SetInputData curlData
    writeCurl Write

vtkStructuredPointsWriter writeCurlMag
    writeCurlMag SetFileName "./ChalCMag0.vtk"
    writeCurlMag SetFileTypeToBinary 
    writeCurlMag SetInputData curlmagData
    writeCurlMag Write

exit

