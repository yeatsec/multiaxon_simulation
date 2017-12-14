from __future__ import division
from neuron import h
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


axon1=h.Section()

dia=10
r  = dia/2
axon1.L=10000
axon1.diam=dia

nseg = 99
axon1.nseg = nseg


#shape = h.PlotShape()

#shape.exec_menu('Show Diam')


theta = np.linspace(-np.pi, np.pi, nseg)
z =  np.linspace(0, axon1.L, nseg)

x = r*np.sin(theta)
#y = r*np.cos(theta)



X, Z = np.meshgrid(x, z)

Y = r*np.cos(theta)





fig = plt.figure(figsize=plt.figaspect(1))
ax = fig.add_subplot(111, projection = '3d')
plt.axis('equal')
ax.plot_surface(X, Y, Z,rstride=1, cstride=1, linewidth = 0, antialiased = False)

#ax.auto_scale_xyz([-500, 500], [-500, 500], [0, 0.15])
plt.show()












