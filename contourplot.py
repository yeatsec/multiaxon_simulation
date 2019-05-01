import io_resources as io_r
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

dpi_spec = 600

diameters = range(2, 26, 2)

dxy = 1

diam_points = list()
diam_x = list()
diam_y = list()
diam_inhib = list()
for i in range(1377):
    diam_points.append([0.0, 0.0])
    diam_x.append(0.0)
    diam_y.append(0.0)
    diam_inhib.append(0.0)

xcoor = np.arange( -300,300, dxy, dtype=float)
ycoor = np.arange(-300, 300, dxy, dtype=float)

for diam in diameters:
    r = io_r.FileReader("uni"+str(diam)+"_r150_114_tempdataxz_stat.csv")
    statlist = r.filereader_read()
    r.filereader_close()
    for i in range(len(statlist)):
        row = statlist[i]
        if row[0] == "0":
            diam_inhib[i] += 2
        diam_points[i] = [float(row[2]), float(row[3])]
        diam_x[i] = float(row[2])
        diam_y[i] = float(row[3])

interp = list()
for x in xcoor:
    for y in ycoor:
        interp.append((x, y))
inhibgrid = griddata(np.array(diam_points), np.array(diam_inhib), interp, method='cubic')

inhibgrid = np.reshape(inhibgrid[:len(xcoor)*len(ycoor)], (len(ycoor), len(xcoor)))
print inhibgrid.shape

# zero out the periphery
for row in range(inhibgrid.shape[0]):
        for col in range(inhibgrid.shape[1]):
                if ((row-300)**2+(col-300)**2 >= 155.**2):
                        inhibgrid[row][col] = np.nan


plt.figure()
ax = plt.gca()
cs = plt.pcolor(xcoor, ycoor, inhibgrid, cmap='YlOrRd', vmin = 0, vmax = 26)
plt.colorbar(cs, ax=ax)
plt.savefig("inhib_scatter.png", dpi=dpi_spec)
# plt.figure()
# plt.contourf(diam_x, diam_y, np.reshape(diam_inhib, len(diam_y), len(diam_x)), cmap='OrRed')
plt.show()


# colorplots of inhibition based on location