import numpy as np 
import csv
from matplotlib import pyplot as plt
from scipy.stats import norm
import math

filename = "fit0"

# nerve statistics
nerve_radius = 125 #um
fiber_density = 1.0/35.37 # fibers/um2

# population modeling statistics (normal model underlaying lognormal)
mu = 0.63 # um
sd = 0.81 # um

def lpac_diam():
	fib_t = np.random.uniform()
	return math.exp(norm.ppf(fib_t, loc=mu, scale=sd))

pop_file = open(filename+"_r"+str(nerve_radius)+".csv", 'w')

fiber_diameters = list()

fiber_spacing = (fiber_density)**(-0.5)  # um
w = csv.writer(pop_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
x_locations = np.arange(-nerve_radius, nerve_radius, step=fiber_spacing, dtype=float)
y_locations = np.arange(-nerve_radius, nerve_radius, step=fiber_spacing, dtype=float)
for x_loc in x_locations:
    for y_loc in y_locations:
        if (x_loc**2 + y_loc**2)**0.5 <= nerve_radius:
            diam = lpac_diam()
            fiber_diameters.append(diam)
            w.writerow([str(diam), str(x_loc), str(y_loc)])
            
pop_file.close()

plt.figure() 
plt.hist(fiber_diameters, bins=50)
plt.title("Fiber Count: " + str(len(fiber_diameters)))
plt.xlabel("Fiber Diameters")
plt.ylabel("Count")
plt.show()