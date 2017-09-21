from neuron import h, gui
import model_resources as m_r 
import numpy as np
from matplotlib import pyplot as plt 


resistivity = (300.0 * 10000.0) # ohm * um
h.celsius = 37
h.tstop = 2.0
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop

t_vals = np.arange(0, h.tstop, step=h.dt, dtype=float)

# model parameters
nerve_radius = 250  # um
fiber_density = 0.016   # fibers/um2
fiber_spacing = (fiber_density)**(-0.5)  # um
fiber_diam = 10  # um
fiber_length = 15000
stim_to_record = 10000
recording_radius = 100
point_of_ref = m_r.Point([0, nerve_radius + 10, stim_to_record])

# set up population in coordinate format, need prodanov statistics
fibers = list()
x_locations = np.arange(-nerve_radius, nerve_radius, step=fiber_spacing, dtype=float)
y_locations = np.arange(-nerve_radius, nerve_radius, step=fiber_spacing, dtype=float)
print "arranging fibers"
count = 0
nerve_x = list()
nerve_y = list()
for x_loc in x_locations:
    for y_loc in y_locations:
        if (x_loc**2 + y_loc**2)**0.5 <= nerve_radius:
            nerve_x.append(x_loc)
            nerve_y.append(y_loc)
            fibers.append(m_r.Fiber((3*np.random.randn()) + fiber_diam, m_r.Point([x_loc, y_loc, 0]), fiber_length, 150, stim_to_record - recording_radius, stim_to_record + recording_radius))
            count += 1
            print count
plt.scatter(nerve_x, nerve_y, c='b', alpha=0.3)
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
            cap_signal[dt_index] += fiber_sa_vals[fiber_index] * (fiber_i_na_vals[fiber_index][section_index][dt_index] + fiber_i_k_vals[fiber_index][section_index][dt_index]) * resistivity / (4 * np.pi * r)

plt.plot(t_vals, cap_signal)
plt.title("Extracellular Voltage due to a Compound Action Potential")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.show()

