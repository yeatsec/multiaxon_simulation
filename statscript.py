import io_resources as io_r
import numpy as np
import matplotlib.pyplot as plt

statfile = "fit0_r125_150_35_stat.csv"
bins = np.arange(0, 25, step=0.5, dtype=float)
# read in statfile and disjstatfile
r = io_r.FileReader(statfile)
noaplist = r.filereader_read()
r.filereader_close()
# separate
aplist = list()
for i in range(len(noaplist)-1, -1, -1):
    fibdata = noaplist[i]
    if (fibdata[0] == "1"):
        aplist.append(fibdata)
        #del noaplist[i]
# amazing
# for each, make a stacked barchart
plt.figure()
plt.title("Activation")

napb, bins2, pat2 = plt.hist(list(map(lambda x: float(x[1]), noaplist)), bins=bins, color='r', histtype='barstacked')
apb, bins1, pat1 = plt.hist(list(map(lambda x: float(x[1]), aplist)), bins=bins, color='b', histtype='barstacked')

plt.figure()
nerve_x = list([float(item[2]) for item in noaplist])
nerve_y = list([float(item[3]) for item in noaplist])
plt.scatter(nerve_x, nerve_y, s=[np.pi*((float(item[1])/2+1)**2) for item in noaplist], c='r', alpha=0.5)
nerve_x = list([float(item[2]) for item in aplist])
nerve_y = list([float(item[3]) for item in aplist])
plt.scatter(nerve_x, nerve_y, s=[np.pi*((float(item[1])/2+1)**2) for item in aplist], c='b', alpha=0.5)

print statfile
print '\n'
print 'active'
print apb
print '\nnot active'
print napb


plt.show()


# colorplots of inhibition based on location