import io_resources as io_r
import numpy as np
import matplotlib.pyplot as plt

dpi_spec = 600

statname = "fit2_r150_3000_80_tempdataxz_stat"
statfile = statname + ".csv"
bins = np.arange(0, 25, step=0.5, dtype=float)
crosssection_size = (8,8)
# read in statfile and disjstatfile
r = io_r.FileReader(statfile)
noaplist = r.filereader_read()
print len(noaplist)
r.filereader_close()
onlynoaplist = list(noaplist)
# separate
aplist = list() 
for i in range(len(noaplist)-1, -1, -1):
    fibdata = noaplist[i]
    if (fibdata[0] == "1"):
        aplist.append(fibdata)
        del onlynoaplist[i]
# amazing
# for each, make a stacked barchart
plt.figure()

napb, bins2, pat2 = plt.hist(list(map(lambda x: float(x[1]), noaplist)), bins=bins, color='r', histtype='barstacked')
apb, bins1, pat1 = plt.hist(list(map(lambda x: float(x[1]), aplist)), bins=bins, color='b', histtype='barstacked')

plt.savefig(statname + "_stackedhist.png", dpi=dpi_spec)

plt.figure()
plt.hist(list(map(lambda x: float(x[1]), noaplist)), bins=bins, color='gray')

plt.savefig(statname+ "_grayhist.png", dpi=dpi_spec)

plt.figure(figsize=crosssection_size)
nerve_x = list([float(item[2]) for item in onlynoaplist])
nerve_y = list([float(item[3]) for item in onlynoaplist])
plt.scatter(nerve_x, nerve_y, s=[np.pi*((float(item[1])/2+2)**2) for item in onlynoaplist], c='r', alpha=0.5)
nerve_x = list([float(item[2]) for item in aplist])
nerve_y = list([float(item[3]) for item in aplist])
plt.scatter(nerve_x, nerve_y, s=[np.pi*((float(item[1])/2+2)**2) for item in aplist], c='b', alpha=0.5)
plt.savefig(statname+"_activescatter.png", dpi=dpi_spec)


plt.figure(figsize=crosssection_size)
nerve_x = list([float(item[2]) for item in noaplist])
nerve_y = list([float(item[3]) for item in noaplist])
plt.scatter(nerve_x, nerve_y, s=[np.pi*((float(item[1])/2+2)**2) for item in noaplist], c='gray', alpha=0.5)

plt.savefig(statname+"_grayscatter.png", dpi=dpi_spec)

print statfile
print '\n'
print 'active'
print apb
print '\nnot active'
print napb


plt.show()


# colorplots of inhibition based on location