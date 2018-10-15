import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import io_resources as io_r

filename = "SingleFiberInContact_Eric_BMES_5sec_41_7mW_200Hz_200us.txt"
# Dimensions are: []

filereader = io_r.tempReader(filename, splitstring=' ')
headers, points, temps = filereader.tempdistread(pointscale=1000.0, tempscale=1.0, x=3000, y=0, z=650, swapxz=True)
xcoor = np.arange( -300, 300, 1.0, dtype=float)
ycoor = np.arange(-300, 300, 1.0, dtype=float)
zcoor = np.linspace(3000, 3000, num=1)

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

plt.figure()
for z_i, z in enumerate(zcoor):
    interp = list()
    for x in xcoor:
        for y in ycoor:
            interp.append([x, y, z])
    tempgrid = griddata(np.array(points), np.array(temps), interp, method='linear', fill_value=6.3)
    
    # r, c = (z_i)/3, (z_i) % 3
    # format into
    plt.contourf(xcoor, ycoor, np.reshape(tempgrid[:len(xcoor)*len(ycoor)], (len(ycoor), len(xcoor))), vmin=temp_min, vmax=temp_max)
    # ax[r, c].set_title(str(z))

plt.show()