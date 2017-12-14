import numpy as np 
import matplotlib.pyplot as plt 
import csv
from mpl_toolkits.mplot3d import Axes3D

filename = "output2_r250.csv"
nseg = 100
fiber_len = 15000
nerve_radius = 250
stim_to_record = 10000

point_of_ref = [0, nerve_radius + 50, stim_to_record]

# fetch and read population file
fiber_diameters = list()
nerve_x = list()
nerve_y = list()

pop_file = open(filename, mode='r')
read = csv.reader(pop_file, delimiter='\t', quotechar='|')
for row in read:
    fiber_diameters.append(float(row[0]))
    nerve_x.append(float(row[1]))
    nerve_y.append(float(row[2]))
pop_file.close()

theta = np.linspace(-np.pi, np.pi, nseg)
z = np.linspace(0, fiber_len, num=nseg, endpoint=True)


fig = plt.figure()
axes = fig.add_subplot(111, projection='3d')
plt.xlim(-5000, 5000)
plt.ylim(-5000, 5000)
for index in range(len(fiber_diameters)):
    r = fiber_diameters[index] / 2
    x = nerve_x[index] + r * np.sin(theta)
    y = nerve_y[index] + r * np.cos(theta)
    X,Z = np.meshgrid(x, z)
    axes.plot_surface(X, y, Z,rstride=50, cstride=50, linewidth = 0, antialiased = False)
# plot point_of_ref in red
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 10 * np.outer(np.cos(u), np.sin(v)) + point_of_ref[0]
y = 10 * np.outer(np.sin(u), np.sin(v)) + point_of_ref[1]
z = 10 * np.outer(np.ones(np.size(u)), np.cos(v)) + point_of_ref[2]
axes.plot_surface(x, y, z, color='r')
plt.show()