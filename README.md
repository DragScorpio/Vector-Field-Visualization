# Vector-Field-Visualization

We have provided 5 volumes for you to inspect. The first three are small test volumes, for which we are giving you the location and type of the critical points inside. Use these volumes to develop and test your programs on. The last two are larger challenge volumes.
 
      Critical points in a vector field usually correspond to locations where the sampled magnitude of the vector field is zero or very large. You can locate critical points by isosurfacing the (scalar) magnitude of the scalar field. For each vector volume, we are supplying a vector magnitude volume.
Once you have determined the location of the critical points, glyphs can help to show the behavior of the field in a small neighborhood surrounding the critical point. In a weather map for instance, a group of arrows encircling a location in clockwise or counterclockwise directions indicate low or high pressure centers. In the same way the orientation of a small number of glyphs around a critical point will indicate whether it is a focus, saddle, etc.
Finding and describing the critical points is useful, but it is also important to understand the global shape of the vector field. For this, a set of streamlines over a large region of the volume can indicate the overall flow between critical points. Starting streamlines at ten or twenty representative seed points within the volume is usually sufficient to describe the global flow patterns.
We are providing a TCL program (calc.tcl ) that reads in the vector field, and computes the divergence , the curl , and the curl magnitude , and then saves out the results as three separate structured points datasets. The divergence is defined as the dot product of the <d/dx , d/dy , d/dz> operator with the vector to produce a scalar, which tells us if the volume
 
is contracting or expanding. If the divergence is negative then it means the volume is contracting and vice versa. The curl of a vector field is the cross product of the <d/dx , d/dy , d/dz> operator with the vector which results in a vector. This represents the measure imaginary component (or) the rotation component in the flow.
test1.tcl - The sample script to visualize the vector fields. Your work:
1. Rewrite the two codes into python codes.
2. Run test1.tcl. Please study this code and think about the following questions:
 The number of critical points in the challenge
volumes. (You can try test volumes first to verify the critical points).
 The location of each critical point in the challenge volumes.
 For each of the critical points: (1) Whether the sampled
vector magnitude is low or high. (2) The type of the critical point.
 For at least two of the critical points in each challenge volume: produce and display in your writeup at least one visualization which illustrates the type of the critical point (you may, and likely will, find it useful to include more than one such visualization). This should be an image which is zoomed up to the critical point, so that the close neighborhood of the critical point fills up the image. Take the time to make these pictures as clear as possible: choosing a good number and distribution of streamlines/streamtubes or glyphs, a good viewpoint, and whatever else you think is helpful to show the three- dimensional behavior.
 Produce a few (at least 2 or 3) visualizations of each challenge volume which shows the large-scale structure of the vector fields. You may mark the critical points in these visualizations.
3. Save some interesting pictures you find in this process.
Turn in:
Please submit the Python code and a report of your study with some of the pictures.
