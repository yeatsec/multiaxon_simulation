from neuron import h, gui
import csv
import model_resources as m_r 
import numpy as np
from matplotlib import pyplot as plt 


resistance = (300.0 * 10000.0) # ohm * um
h.celsius = 25  #6.3 CHECK
h.tstop = 20.0
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop
m_r.init_model(h.tstop, dt, resistance) # ensure that the fiber resources have the same time dimensions

print "model demo timesteps: ", timesteps

pop_filename = "apl4_r125.csv" # CHECK
mod_name = "apl"
output_filename = "apl4_r125_25c.csv" # CHECK

t_vals = np.arange(0, h.tstop, step=h.dt, dtype=float)

# model parameters
nerve_radius = 125  # um
fiber_length = 12000
stim_to_record = 10000
recording_radius = 2000 # this gets complicated with multiple electrodes....
section_count = 30
#bipol_width = 2000
p_point = m_r.Point([0, nerve_radius + 5, stim_to_record])
p_ref = m_r.voltPoint(p_point, timesteps)

# fetch and read population file
fibers = list()
fiber_diameters = list()
nerve_x = list()
nerve_y = list()

temperatures = section_count * [timesteps * [45]]

pop_file = open(pop_filename, mode='r')
read = csv.reader(pop_file, delimiter='\t', quotechar='|')
for row in read:
    fiber_diameters.append(float(row[0]))
    print str(len(fiber_diameters))
    nerve_x.append(float(row[1]))
    nerve_y.append(float(row[2]))
    fibers.append(m_r.Fiber(float(row[0]), m_r.Point([float(row[1]), float(row[2]), 0]), fiber_length, section_count, stim_to_record - recording_radius, stim_to_record + recording_radius, mod_name, temperatures))
pop_file.close()


plt.scatter(nerve_x, nerve_y, s=[np.pi*((diam/2)**2) for diam in fiber_diameters], c='b', alpha=0.3)
# plt.show()
print "population size: ", len(fibers)
# package fibers, activation, recording


h.finitialize(-80.0)
h.fcurrent()
h.init()
print "running simulation"
for tstep in range(timesteps):
    print "current time step: ", str(tstep + 1), " of ", str(timesteps)
    for fib in fibers:
        fib.updateTempTime()
    h.fadvance()


for fib in fibers:
    p_ref.addVoltFromFiber(fib)

p_signal = p_ref.getSignal()

# for i in range(timesteps):
#     volt_signal.append(p_signal[i]-n_signal[i])


file = open(output_filename, 'w')
w = csv.writer(file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

w.writerow([str(x) for x in p_signal])

file.close()
print "file saved\n"

plt.figure()
plt.plot(t_vals, p_signal)
plt.title("(+) Terminal")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.show()

