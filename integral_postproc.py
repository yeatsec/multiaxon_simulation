import numpy as np 
import csv
from matplotlib import pyplot as plt 

filename = "last_run.csv"

sim_file = open(filename, 'r')
read = csv.reader(sim_file, delimiter='\t', quotechar='|')
input_list = read.next()
sim_file.close()

dt = 0.025
tstop = 20.0

abs_v_signal = [abs(float(v)) for v in input_list]
integral = 0.0
for v in abs_v_signal:
	integral += v*dt
print str(integral)

integral/=2
i = 0
while integral >= 0:
	integral -= abs_v_signal[i]*dt
	i += 1

print str(float(i)*dt)

plt.figure()
plt.plot(np.arange(0, tstop, step=dt, dtype=float), abs_v_signal)
plt.show()

