import csv
import numpy as np
from matplotlib import pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

t_alpha_df = 2.77644 # alpha = 0.05, df = 4, two-tailed

t_stop = 20.0 # ms
dt = 0.025 # ms
timesteps = np.arange(0, t_stop, step=dt, dtype=float)

temperatures = [5, 15, 25]
populations = [0, 1, 2, 3, 4]
colors = ['b', 'g', 'r', 'c', 'm', 'k']
num_temps = len(temperatures)
num_pops = len(populations)

temp_pop = list() # temp_pop[temp_lvl][pop_num][cap_index]

temp_index = 0
for temp in temperatures:
	temp_pop.append(list())
	for pop in populations:
		filename = "apl"+str(pop)+"_r125_"+str(temp)+"c.csv"
		sim_file = open(filename, 'r')
		read = csv.reader(sim_file, delimiter='\t', quotechar='|')
		input_list = read.next()
		sim_file.close()
		temp_pop[temp_index].append([float(val) for val in input_list])
	temp_index += 1

sig_size = int(t_stop/dt)
# calculate mean for each temperature level
mean_cap_at_temp = list()
sd_cap_at_temp = list()
for temp_index in range(num_temps):
	mean_cap_at_temp.append([0.0] * sig_size) # will add each pop's CAP at this temp
	sd_cap_at_temp.append([0.0] * sig_size)
	for pop in populations:
		for i in range(sig_size):
			mean_cap_at_temp[temp_index][i] = mean_cap_at_temp[temp_index][i] + (temp_pop[temp_index][pop][i]/num_pops)
	for pop in populations:
		for i in range(sig_size):
			sd_cap_at_temp[temp_index][i] = sd_cap_at_temp[temp_index][i] + (((mean_cap_at_temp[temp_index][i]-temp_pop[temp_index][pop][i])**2)/(num_pops-1))
	for sd_index in range(sig_size):
		sd_cap_at_temp[temp_index][i] = (sd_cap_at_temp[temp_index][i])**(0.5)

# plot it all
plt.figure()
plt.title("Temperature Dependent CAP Evolution", fontsize=28)
plt.ylabel("Extracellular Voltage (mV)", fontsize=28)
plt.xlabel("Time (ms)", fontsize=28)
ax = plt.gca()
for temp_index in range(num_temps):
	plt.plot(timesteps, mean_cap_at_temp[temp_index], color=colors[temp_index], linewidth=2, label=str(temperatures[temp_index])+' $^\circ$C')
	ax.fill_between(timesteps, [mean_cap_at_temp[temp_index][i] + sd_cap_at_temp[temp_index][i] for i in range(sig_size)], [mean_cap_at_temp[temp_index][i] - sd_cap_at_temp[temp_index][i] for i in range(sig_size)], color=colors[temp_index], alpha=0.3)
ax.legend(fontsize=22)
ax.grid(axis='both')
plt.show()