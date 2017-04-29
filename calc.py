import vtk
import math
import sys
import os.path
import os

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("ChalVec1.vtk")
reader.Update()

reader.Update()
mags = reader.GetOutput()
bounds = mags.GetBounds()
x0 = bounds[0]
x1 = bounds[1]
xdm1 = x1 - x0
xd = int(x1 - x0 + 1)
y0 = bounds[2]
y1 = bounds[3]
ydm1 = y1 - y0
yd = int(y1 - y0 + 1)
z0 = bounds[4]
z1 = bounds[5]
zdm1 = z1 - z0
zd = int(z1 - z0 + 1)
print "DATA DIMENSIONS ARE: %d %d %d" %(xd, yd, zd)

vecinfo = reader.GetOutput().GetPointData().GetVectors()

curlData = vtk.vtkStructuredPoints()
curlData.SetDimensions(xd, yd, zd)
curlData.SetSpacing(1, 1, 1)
curlData.SetOrigin(0, 0, 0)

divData = vtk.vtkStructuredPoints()
divData.SetDimensions(xd, yd, zd)
divData.SetSpacing(1, 1, 1)
divData.SetOrigin(0, 0, 0)

curlmagData = vtk.vtkStructuredPoints()
curlmagData.SetDimensions(xd, yd, zd)
curlmagData.SetSpacing(1, 1, 1)
curlmagData.SetOrigin(0, 0, 0)

div = vtk.vtkFloatArray()
div.SetNumberOfComponents(1)
div.SetNumberOfTuples(xd * yd * zd)

curl = vtk.vtkFloatArray()
curl.SetNumberOfComponents(3)
curl.SetNumberOfTuples(xd * yd * zd)

curlmag = vtk.vtkFloatArray()
curlmag.SetNumberOfComponents(1)
curlmag.SetNumberOfTuples(xd * yd * zd)

for k in range(zd):
	for j in range(yd):
		for i in range(xd):
			index = (i + (xd * j) + (xd * yd * k))
			if((i == 0) or (j == 0) or (k == 0) or (i == xdm1) or (j == ydm1) or (k == zdm1)):
				div.SetTuple1(index, 0.0)
				curl.SetTuple3(index, 0.0, 0.0, 0.0)
				curlmag.SetTuple1(index, 0.0)
			else:
				idxminus1 = ((i - 1) + (xd * j) + (xd * yd * k))
				idxplus1 = ((i + 1) + (xd * j) + (xd * yd * k))
				idyminus1 = (i + (xd * (j - 1)) + (xd * yd * k))
				idyplus1 = (i + (xd * (j + 1)) + (xd * yd * k))
				idzminus1 = (i + (xd * j) + (xd * yd * (k - 1)))
				idzplus1 = (i + (xd * j) + (xd * yd * (k + 1)))

				xxm1 = vecinfo.GetComponent(idxminus1, 0)
				yxm1 = vecinfo.GetComponent(idxminus1, 1)
				zxm1 = vecinfo.GetComponent(idxminus1, 2)

				xym1 = vecinfo.GetComponent(idyminus1, 0)
				yym1 = vecinfo.GetComponent(idyminus1, 1)
				zym1 = vecinfo.GetComponent(idyminus1, 2)

				xzm1 = vecinfo.GetComponent(idzminus1, 0)
				yzm1 = vecinfo.GetComponent(idzminus1, 1)
				zzm1 = vecinfo.GetComponent(idzminus1, 2)

				xxp1 = vecinfo.GetComponent(idxplus1, 0)
				yxp1 = vecinfo.GetComponent(idxplus1, 1)
				zxp1 = vecinfo.GetComponent(idxplus1, 2)

				xyp1 = vecinfo.GetComponent(idyplus1, 0)
				yyp1 = vecinfo.GetComponent(idyplus1, 1)
				zyp1 = vecinfo.GetComponent(idyplus1, 2)

				xzp1 = vecinfo.GetComponent(idzplus1, 0)
				yzp1 = vecinfo.GetComponent(idzplus1, 1)
				zzp1 = vecinfo.GetComponent(idzplus1, 2)
				# Calculate divergence
				dxx = (xxp1 - xxm1) / 2
				dyy = (yyp1 - yym1) / 2
				dzz = (zzp1 - zzm1) / 2
				# Calculate curl
				dzy = (zyp1 - zym1) / 2
				dyz = (yzp1 - yzm1) / 2
				dxz = (xzp1 - xzm1) / 2
				dzx = (zxp1 - zxm1) / 2
				dyx = (yxp1 - yxm1) / 2
				dxy = (xyp1 - xym1) / 2

				x = dzy - dyz
				y = dxz - dzx
				z = dyx - dxy

				div.SetTuple1(index, (dxx + dyy + dzz))
				curl.SetTuple3(index, x, y, z)
				# Calculate curl magnitude
				curlmag.SetTuple1(index, math.sqrt(x * x + y * y + z * z))
	print "JUST DID VOXEL: %d %d %d %d" %(k, j, i, index)

divData.GetPointData().SetScalars(div)
curlData.GetPointData().SetVectors(curl)
curlmagData.GetPointData().SetScalars(curlmag)

# create a writer, to save information to a file
writeDiv = vtk.vtkStructuredPointsWriter()
writeDiv.SetFileName("./ChalDMag0.vtk")
writeDiv.SetFileTypeToBinary()
writeDiv.SetInputData(divData)
writeDiv.Write()

writeCurl = vtk.vtkStructuredPointsWriter()
writeCurl.SetFileName("./ChalCur0.vtk")
writeCurl.SetFileTypeToBinary() 
writeCurl.SetInputData(curlData)
writeCurl.Write()

writeCurlMag = vtk.vtkStructuredPointsWriter()
writeCurlMag.SetFileName("./ChalCMag0.vtk")
writeCurlMag.SetFileTypeToBinary() 
writeCurlMag.SetInputData(curlmagData)
writeCurlMag.Write()

sys.exit()
