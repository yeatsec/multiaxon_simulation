import io_resources as io_r
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt

# have a list of filenames

levels = np.arange(0.60, 1.50, 0.10, float)
levels[0] = 0.0
cap_filenames = ["fit3_r250_" + str(int((x+0.001)*100)) + "_tempdataxz" for x in levels]
colors = ['k', 'b', 'g', 'r', 'c', 'm', 'y', '0.5']#, 'y']
labels = ['Peak Temp ' + str(round(lvl*20.84, 1) + 20) + 'C' for lvl in levels]
y_lims = None # (-0.5, 0.5)
timesteps = np.arange(0, 40, 0.025, dtype=float) # CHECK TSTO)P

caps = list()
for fi, fname in enumerate(cap_filenames):
    capreader = io_r.FileReader(fname+'_cap.csv')
    caps.append(list(map(lambda x: float(x[0]),capreader.filereader_read())))
    capreader.filereader_close()


# display CAPs
plt.figure()
for ci, cap in enumerate(caps):
    plt.plot(timesteps, cap, linewidth=2, color=colors[ci%len(colors)], label=labels[ci])
plt.ylim(y_lims)
plt.legend()
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.savefig("combined_cap2.png", dpi=600)
plt.show()

aocs = list()

for ci, cap in enumerate(caps):
    aocs.append(sum(np.abs(cap))*0.025)

# read in the inhibition information
inhibs = list()
actives = list()
for fi, fname in enumerate(cap_filenames):
    actreader = io_r.FileReader(fname + '_stat.csv')
    unproc = list(map(lambda x: float(x[0]), actreader.filereader_read()))
    active = 0
    inhib = 0
    
    for x in unproc:
        if (int(x) == 1):
            active += 1
        else:
            inhib += 1

    inhibs.append(inhib)
    actives.append(active)

actprops = [float(actives[i])/(float(actives[i])+float(inhibs[i])) for i in range(len(cap_filenames))]
aocmax = max(aocs)
actmax = max(actprops)

normaocs = [aoc/aocmax for aoc in aocs]
normacts = [act/actmax for act in actprops]

plt.figure()
plt.scatter(normaocs, normacts)
plt.title("Comparison of Normalized AUC and Uninhibited Axon Proportion")
plt.ylabel("Uninhibited Proportion of Axons")
plt.xlabel("Normalized Area Under the Curve (AUC)")
plt.savefig("auc_comparison.png", dpi=600)
plt.show()

print aocs


