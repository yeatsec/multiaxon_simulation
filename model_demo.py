from neuron import h, gui
import csv
import model_resources as m_r 
import numpy as np
from matplotlib import pyplot as plt 
import io_resources as io_r

# NEURON/physical parameters
resistance = (300.0 * 10000.0) # ohm * um
# h.celsius = 6.3  #6.3 CHECK
h.tstop = 15.0
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop

print "model demo timesteps: ", timesteps

pop_file = "fit0_r125" # no file extension
pop_path = "./populations/" + pop_file + ".csv" # CHECK
mod_name = "apl"

t_vals = np.arange(0.0, h.tstop, step=h.dt, dtype=float)

# model parameters
nerve_radius = 125  # um
fiber_length = 6000.0
stim_to_record = 4000.0
recording_radius = 2000.0 # this gets complicated with multiple electrodes....
block_temp = 35.0
block_location = 2000.0 # um
block_length = 150.0 # um

output_filename = pop_file + "_" + str(int(block_length)) + "_" + str(int(block_temp)) + "_cap.csv" # CHECK
stat_out_filename = pop_file + "_" + str(int(block_length)) + "_" + str(int(block_temp)) + "_stat.csv"

block_length/=2

section_count = 60
section_length = float(fiber_length)/float(section_count)
#bipol_width = 2000
p_point = m_r.Point([0, nerve_radius + 5, stim_to_record])
p_ref = m_r.voltPoint(p_point, timesteps)

# fetch and read population file
fibers = list()
fiber_diameters = list()
nerve_x = list()
nerve_y = list()

temperatures = section_count * [timesteps * [block_temp]] # create list of list of temps at timesteps for each section; apply same to all axons

print "block_length is set to: ", block_length

# overwrite sections in block radius with block temp
temperatures = list()
for sec_num in range(section_count):
    sec_center = sec_num * section_length + (section_length/2)
    if (sec_center >= block_location - block_length and sec_center <= block_location + block_length): # within blocking area
        temperatures.append(timesteps * [block_temp]) # set temps at this location for all time_val to block_temp
        print "setting temp at length ", sec_center
    else:
        temperatures.append(timesteps * [6.3])

m_r.init_model(h.tstop, dt, resistance, uniformTempVecs=temperatures) # ensure that the fiber resources have the same time dimensions


pop_file = open(pop_path, mode='r')
read = csv.reader(pop_file, delimiter='\t', quotechar='|')
for row in read:
    fiber_diameters.append(float(row[0]))
    if (len(fiber_diameters) % 100 == 0):
        print str(len(fiber_diameters))
    nerve_x.append(float(row[1]))
    nerve_y.append(float(row[2]))
    fibers.append(m_r.Fiber(float(row[0]), m_r.Point([float(row[1]), float(row[2]), 0]), fiber_length, section_count, stim_to_record - recording_radius, stim_to_record + recording_radius, mod_name, temperatures))
pop_file.close()


plt.scatter(nerve_x, nerve_y, s=[np.pi*((diam/2)**2) for diam in fiber_diameters], c='b', alpha=0.3)
# plt.show()
print "population size: ", len(fibers)
# package fibers, activation, recording

print "running simulation"
h.finitialize(-80.0)
h.fcurrent()
h.init()
h.run()
print "simulation finished"

# for tstep in range(timesteps):
#     if (tstep % 100 == 0):
#         print "current time step: ", str(tstep + 1), " of ", str(timesteps)
#     for fib in fibers:
#         fib.updateTempTime()
#     h.fadvance()


for fib in fibers:
    p_ref.addVoltFromFiber(fib)

p_signal = p_ref.getSignal()

# for i in range(timesteps):
#     volt_signal.append(p_signal[i]-n_signal[i])


w = io_r.FileWriter(output_filename)
w.filewriter_write(list(map(lambda x: [str(x)], p_signal))) # expect list of lists
w.filewriter_close()
print "file saved\n"

aplist = list()
for fib in fibers:
    aplist.append((["1"] if fib.apDetect() else ["0"]) + [fib.getDiam()] + fib.getLoc().getLoc())

w = io_r.FileWriter(stat_out_filename)
w.filewriter_write(aplist)
w.filewriter_close()


plt.figure()
plt.plot(t_vals, p_signal)
plt.title("(+) Terminal")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.show()

quit()