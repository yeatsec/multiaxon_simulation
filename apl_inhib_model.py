from neuron import h, gui
import csv
import model_resources as m_r 
import numpy as np
from matplotlib import pyplot as plt 
import io_resources as io_r

# Developed 4/1/19
# NEURON/physical parameters
resistance = (300.0 * 10000.0) # ohm * um
default_temp = 20.0
h.tstop = 40.0
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop

pop_file = "fit2_r150" # no file extension
temp_path = "temps_bilinear_dtemp20.csv"
pop_path = "./populations/" + pop_file + ".csv" # check
# assoc temperature dist files will be paired with axons in pop, but will have own section length
mod_name = "hhlt"

t_vals = np.arange(0.0, h.tstop, step = h.dt, dtype=float)

### nerve model parameters
nerve_radius = 150 #um
fiber_length = 30000 # um, is the length of all fibers which compose the nerve, and hence the nerve length
section_length = 100 # um, the length of each NEURON section used to compose the fiber. make sure this dividese fiber_length with an integer rersult.
section_count = int(fiber_length/section_length)
stim_z = 1000 # um, the location along the length of the nerve where current is injected for axon excitation
record_z = 28000 # um, the location along the length of the nerve where membrane current recording is **centered**
recording_radius = 2000.0 # um, the maximum distance along the length of the nerve in the +/- z direction from which the membrane current is recorded
# thus, the sections which contribute to the CNAP recording are at locations [:, :, record_z-recording_radius:record_z+recording_radius]
# recording_radius empirically determined (in simulation; is saturation point of recorded signal)
scale_temp = 0.65
fill=None   # make sure is None if scale_temp is important
block_location = 15000
block_length = 3000 # um (1500 um on each side of block_location)
rec_dist = 3000 # um, dist orthogonal from nerve surface to recording ()

# recording parameters

p_point = m_r.Point([0, nerve_radius + rec_dist, record_z])
p_ref = m_r.voltPoint(p_point, timesteps)

output_filename = pop_file + "_"+ str(int(scale_temp*100)) +"_tempdataxz_cap.csv"
stat_out_filename = pop_file + "_" + str(int(scale_temp*100)) + "_tempdataxz_stat.csv"
block_length/=2

aplist = list()

def scaleTemp(temp, scale, baseline, fill=None):
    if fill is None:
        return (temp - baseline) * scale + baseline
    return fill

m_r.init_model(h.tstop, dt, resistance)
# read in each axon
# for new fiber in population, temperature info attached - apply scaling factor
pop_file_csv = open(pop_path, mode='rU')
readpop = csv.reader(pop_file_csv, delimiter='\t', quotechar='|')
temp_file_csv = open(temp_path, mode='rU')
readtemp = csv.reader(temp_file_csv, delimiter='\t', quotechar='|')
temps = list()
for row in readtemp:
    temps.append(list(map(lambda x: scaleTemp(float(x), scale_temp, default_temp, fill=fill), row)))

for i, fps in enumerate(readpop): # new axon, temperature file linked
    print str(i)
    temperatures = temps[i]
    fiber = m_r.Fiber(float(fps[0]), m_r.Point([float(fps[1]), float(fps[2]), 0]), fiber_length, section_count, record_z-recording_radius, record_z+recording_radius, mod_name, temp_time=[[x]*timesteps for x in temperatures])

    h.finitialize(-80.0)
    h.fcurrent()
    h.init()
    h.run()
    aplist.append((["1"] if fiber.apDetect() else ["0"]) + [fiber.getDiam()] + fiber.getLoc().getLoc())
    p_ref.addVoltFromFiber(fiber)
    

pop_file_csv.close()
temp_file_csv.close()

p_signal = p_ref.getSignal()


w = io_r.FileWriter(output_filename)
w.filewriter_write(list(map(lambda x: [str(x)], p_signal))) # expect list of lists
w.filewriter_close()
print "file saved\n"

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