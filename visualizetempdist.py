import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import io_resources as io_r

filename = "newtempdist.txt"
mirrxy = True
# Dimensions are: []

filereader = io_r.tempReader(filename, splitstring=' ')
headers, points, temps = filereader.tempdistread(pointscale=1000.0, tempscale=1.0, x=0, y=0, z=-2250, mirrorxy=mirrxy, swapxz=True) # z=650
xcoor = np.arange( -500, 500, 5.0, dtype=float)
ycoor = np.arange(-500, 500, 5.0, dtype=float)
zcoor = np.linspace(-200, 200, num=5)

altzcoor = np.arange(-500, 500, 5.0, dtype=float)

temp_min = min(temps)
temp_max = max(temps)
print temp_min, temp_max
filereader.tempreader_close()

ymin = [0, 0, 0]
for point in points:
	if point[0] < ymin[0]:
		ymin = point
print "ymin is ", ymin
ymax = list(ymin)
for point in points:
	if point[0] > ymax[0]:
		ymax = point
print "ymax is ", ymax

temp_min = 25

for z_i, z in enumerate(zcoor):
	interp = list()
	for x in xcoor:
		for y in ycoor:
			interp.append([x, y, z])
	tempgrid = griddata(np.array(points), np.array(temps), interp, method='linear', fill_value=20)
	
	# r, c = (z_i)/3, (z_i) % 3
	# format into
	plt.figure()
	plt.title('Crossectional View of Heated Nerve')
	plt.pcolor(xcoor, ycoor, np.reshape(tempgrid[:len(xcoor)*len(ycoor)], (len(ycoor), len(xcoor))), cmap='jet', vmin=int(temp_min), vmax=int(temp_max))
	plt.clim(25, temp_max)
	plt.colorbar()
	plt.gca().set_aspect('equal', adjustable='box')
	# ax[r, c].set_title(str(z))

interp = list()
for y in ycoor:
	for z in altzcoor:
		interp.append([0, y, z])
tempgrid = griddata(np.array(points), np.array(temps), interp, method='linear', fill_value=20)

plt.figure()
plt.title('Axial Transection of Heated Nerve')
plt.pcolor(ycoor, altzcoor, np.reshape(tempgrid[:len(ycoor)*len(altzcoor)], (len(altzcoor), len(ycoor))), cmap='jet', vmin=int(temp_min), vmax=int(temp_max))
plt.clim(temp_min, temp_max)
plt.gca().set_aspect('equal', adjustable='box')
#plt.colorbar()
plt.show()