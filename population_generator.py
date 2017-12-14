import numpy as np 
import csv
from matplotlib import pyplot as plt

filename = "output2"

# nerve statistics
nerve_radius = 250 #um
fiber_density = 0.0016 # fibers/um2
fiber_diam_mean = 6
fiber_diam_sdev = 1

pop_file = open(filename+"_r"+str(nerve_radius)+".csv", 'w')

fiber_diameters = list()

fiber_spacing = (fiber_density)**(-0.5)  # um
w = csv.writer(pop_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
x_locations = np.arange(-nerve_radius, nerve_radius, step=fiber_spacing, dtype=float)
y_locations = np.arange(-nerve_radius, nerve_radius, step=fiber_spacing, dtype=float)
for x_loc in x_locations:
    for y_loc in y_locations:
        if (x_loc**2 + y_loc**2)**0.5 <= nerve_radius:
            diam = fiber_diam_mean + (fiber_diam_sdev * np.random.randn())
            #if (x_loc > -100):
            #    diam *= 2   # for model checking
            fiber_diameters.append(diam)
            w.writerow([str(diam), str(x_loc), str(y_loc)])
            
pop_file.close()

plt.figure() 
plt.hist(fiber_diameters, bins=10)
plt.xlabel("Fiber Diameters")
plt.ylabel("Count")
plt.show()