import io_resources as io_r
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt

# have a list of filenames

#cap_filenames = ["fit2_r150_0_35_cap.csv", "fit2_r150_300_35_cap.csv", "fit2_r150_600_35_cap.csv", "fit2_r150_1200_35_cap.csv"]#
cap_filenames = ["fit2_r150_0_35_cap.csv", "fit2_r150_3000_90_tempdataxz_cap.csv", "fit2_r150_3000_95_tempdataxz_cap.csv", "fit2_r150_3000_100_tempdataxz_cap.csv"]
levels = [0, 80, 85, 90, 95, 100]
colors = ['k', 'b', 'g', 'r', 'y']
labels = ['No Heat Distribution', '38.76 $^\circ$C', '39.80 $^\circ$C', '40.84 $^\circ$C']
y_lims = (-4.0, 6.0)
timesteps = np.arange(0, 15, 0.025, dtype=float)

caps = list()
for fi, fname in enumerate(cap_filenames):
    capreader = io_r.FileReader(fname)
    caps.append(list(map(lambda x: float(x[0]),capreader.filereader_read())))
    capreader.filereader_close()


# display CAPs
plt.figure()
for ci, cap in enumerate(caps):
    plt.plot(timesteps, cap, linewidth=3, color=colors[ci], label=labels[ci])
plt.ylim(y_lims)
plt.legend()
plt.savefig("combined_cap2.png", dpi=600)
plt.show()
