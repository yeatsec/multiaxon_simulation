import numpy as np 
import csv
from matplotlib import pyplot as plt

filename = "apl4"

# nerve statistics
nerve_radius = 150 #um
fiber_density = 1.0/50.96 # fibers/um2 #35.37

def lpac_diam():
	fib_t = np.random.uniform()
	if (fib_t <= 0.5314):
		return np.random.uniform(low=0.8, high=2.0)
	elif (fib_t <= 0.9797):
		return np.random.uniform(low=2.0, high=10.0)
	else:
		return np.random.uniform(low=10.0, high=25.0)

pop_file = open(filename+"_r"+str(nerve_radius)+".csv", 'wb')

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
plt.hist(fiber_diameters, bins=20)
plt.title("Fiber Count: " + str(len(fiber_diameters)))
plt.xlabel("Fiber Diameters")
plt.ylabel("Count")
plt.show()