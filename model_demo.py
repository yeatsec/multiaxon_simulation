from neuron import h, gui
import csv
import model_resources as m_r 
import numpy as np
from matplotlib import pyplot as plt 
import io_resources as io_r
from scipy.interpolate import griddata

# NEURON/physical parameters
resistance = (300.0 * 10000.0) # ohm * um
# h.celsius = 6.3  #6.3 CHECK
default_temp = 20.0
h.tstop = 15.0
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop

print "model demo timesteps: ", timesteps

pop_file = "uni24_r150" # no file extension
pop_path = "./populations/" + pop_file + ".csv" # CHECK
mod_name = "hhlt"

tempfilename = "SingleFiberInContact_Eric_BMES_5sec_41_7mW_200Hz_200us.txt"

t_vals = np.arange(0.0, h.tstop, step=h.dt, dtype=float)

use_temp_dist = True

# model parameters
nerve_radius = 150  # um
fiber_length = 7000.0
stim_to_record = 5000.0
recording_radius = 2000.0 # this gets complicated with multiple electrodes....
scale_temp = 1.00
block_temp = 35.0
block_location = 2000.0 # um
block_length = 3000.0 # um

output_filename = pop_file + "_" + str(int(block_length)) + "_" + str(int(block_temp)) + "_cap.csv" # CHECK
stat_out_filename = pop_file + "_" + str(int(block_length)) + "_" + str(int(block_temp)) + "_stat.csv"
if use_temp_dist:
    output_filename = pop_file + "_" + str(int(block_length))+ "_"+ str(int(scale_temp*100)) +"_tempdataxz_cap.csv"
    stat_out_filename = pop_file + "_" + str(int(block_length))+ "_" + str(int(scale_temp*100)) + "_tempdataxz_stat.csv"
block_length/=2

section_count = 70
section_length = float(fiber_length)/float(section_count)
#bipol_width = 2000
p_point = m_r.Point([0, nerve_radius + 5, stim_to_record])
p_ref = m_r.voltPoint(p_point, timesteps)

# fetch and read population file
fibers = list()
fiber_diameters = list()
nerve_x = list()
nerve_y = list()

print "block_length is set to: ", block_length

# forward declarations
temperatures = list()
fiber_temps = list()
headers = list()
points = list()
temps = list()
if use_temp_dist:
    # load in temperature data
    reader = io_r.tempReader(tempfilename, splitstring=' ')
    headers, points, temps = reader.tempdistread(pointscale=1000.0, tempscale=scale_temp, x=block_location, y=0, z=650, swapxz=True)
    reader.tempreader_close()
    points, temps = np.array(points), np.array(temps)
    m_r.init_model(h.tstop, dt, resistance)
else:
    for sec_num in range(section_count):
        sec_center = sec_num * section_length + (section_length/2)
        if (sec_center >= block_location - block_length and sec_center <= block_location + block_length): # within blocking area
            temperatures.append(timesteps * [block_temp]) # set temps at this location for all time_val to block_temp
            print "setting temp at length ", sec_center
        else:
            temperatures.append(timesteps * [default_temp])
    m_r.init_model(h.tstop, dt, resistance, uniformTempVecs=temperatures) # ensure that the fiber resources have the same time dimensions

if use_temp_dist:
    default_temp = np.amin(temps)

pop_file = open(pop_path, mode='r')
read = csv.reader(pop_file, delimiter='\t', quotechar='|')
for row in read:
    fiber_diameters.append(float(row[0]))
    if (len(fiber_diameters) % 100 == 0):
        print str(len(fiber_diameters))
    nerve_x.append(float(row[1]))
    nerve_y.append(float(row[2]))
    if use_temp_dist:
        print "interpolating for fiber ", len(fiber_diameters)
        sec_locs = m_r.getSecLocs(section_count, section_length)
        sec_points = list()
        for loc in sec_locs:
            sec_points.append([float(row[1]), float(row[2]), float(loc)])
        temperatures = griddata(points, temps, sec_points, method='nearest', fill_value=default_temp)
        temp_temps = list()
        for i, temp_val in enumerate(temperatures):
            if sec_locs[i] >= block_location - block_length and sec_locs[i] <= block_location + block_length:
                temp_temps.append(timesteps * [temp_val])
            else:
                temp_temps.append(timesteps * [default_temp])
        temperatures = temp_temps
    fibers.append(m_r.Fiber(float(row[0]), m_r.Point([float(row[1]), float(row[2]), 0]), fiber_length, section_count, stim_to_record - recording_radius, stim_to_record + recording_radius, mod_name, temp_time=temperatures))
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