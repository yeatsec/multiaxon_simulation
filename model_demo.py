from neuron import h, gui
import csv
import model_resources as m_r 
import numpy as np
from matplotlib import pyplot as plt 


resistance = (300.0 * 10000.0) # ohm * um
h.celsius = 6.3
h.tstop = 5
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop

pop_filename = "output2_r250.csv"

t_vals = np.arange(0, h.tstop, step=h.dt, dtype=float)

# model parameters
nerve_radius = 250  # um
fiber_length = 15000
stim_to_record = 15000
recording_radius = 100
point_of_ref = m_r.Point([0, nerve_radius + 10, stim_to_record])

# fetch and read population file
fibers = list()
fiber_diameters = list()
nerve_x = list()
nerve_y = list()

pop_file = open(pop_filename, mode='r')
read = csv.reader(pop_file, delimiter='\t', quotechar='|')
for row in read:
    fiber_diameters.append(float(row[0]))
    nerve_x.append(float(row[1]))
    nerve_y.append(float(row[2]))
    fibers.append(m_r.Fiber(float(row[0]), m_r.Point([float(row[1]), float(row[2]), 0]), fiber_length, 150, stim_to_record - recording_radius, stim_to_record + recording_radius))
pop_file.close()


plt.scatter(nerve_x, nerve_y, s=[np.pi*((diam/2)**2) for diam in fiber_diameters], c='b', alpha=0.3)
plt.show()
print "population size: ", len(fibers)
# package fibers, activation, recording


h.finitialize(-80.0)
h.fcurrent()
h.init()
print "running simulation"
h.run()

# extract i_na and i_k information, sum each into single list, keep surface area in mind
# parallel lists of i_na, i_k, sa, points
fiber_i_na_vals = list()    # 3D list
fiber_i_k_vals = list()     # 3D
fiber_section_current_vals = list()
fiber_sa_vals = list()      # 1D
fiber_points_vals = list()  # 2D
for fiber in fibers:
    fiber_i_na_vals.append(fiber.get_na_vectors())
    fiber_i_k_vals.append(fiber.get_k_vectors())
    fiber_points_vals.append(fiber.get_vector_points())
    fiber_sa_vals.append(fiber.getSectionSA())
# calculate extracellular voltage due to sum of values
print "calculating voltage values"
cap_signal = [0.0] * int(h.tstop/h.dt)
for fiber_index in range(len(fibers)):  # iterate fibers within population
    for section_index in range(fibers[fiber_index].get_vector_count()):  # iterate sections within fiber
        section_point = fiber_points_vals[fiber_index][section_index]
        r = section_point.getDist(point_of_ref)
        for dt_index in range(int(h.tstop/h.dt)):   # iterate time values within section var
            cap_signal[dt_index] += fiber_sa_vals[fiber_index] * (fiber_i_na_vals[fiber_index][section_index][dt_index] + fiber_i_k_vals[fiber_index][section_index][dt_index]) * resistance / (4 * np.pi * r)

plt.plot(t_vals, cap_signal)
plt.title("Extracellular Voltage due to a Compound Action Potential")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.show()

