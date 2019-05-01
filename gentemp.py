import numpy as np
import csv
import io_resources as io_r
from scipy.interpolate import griddata


temperature_distribution = "SingleFiberInContact_Eric_BMES_5sec_41_7mW_200Hz_200us.txt"

tempfilename = 'temps_bilinear'
popfilename = 'fit2_r150.csv'
pop_path = './populations/' + popfilename

default_temp = 20
tempfilename = tempfilename + '_dtemp'+str(default_temp)
nerve_length = 30000
section_length = 100
block_length = 3000
block_location = 15000
block_start = block_location - (block_length/2) + (section_length/2)
block_end_past = block_location + (block_length/2) + (section_length/2)
temp_z_locs = np.arange(start=block_start, stop=block_end_past, step=section_length, dtype=float)
nerve_z_locs = np.arange(start=(section_length/2), stop=nerve_length + (section_length/2), step=section_length, dtype=float)

# load in the temperature distribution
reader = io_r.tempReader(temperature_distribution, splitstring=' ')
headers, points, temps = reader.tempdistread(pointscale=1000.0, tempscale=1.0, x=block_location, y=0, z=650, swapxz=True)
reader.tempreader_close()

points, temps = np.array(points), np.array(temps)

temp_file = open(tempfilename+'.csv', 'wb')
w = csv.writer(temp_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

pop_file = open(pop_path, mode='r')
read = csv.reader(pop_file, delimiter='\t', quotechar='|')
count = 0
for row in read:
    print str(count)
    count += 1
    dist_sec_points = list()
    for z in temp_z_locs:
        dist_sec_points.append([float(row[1]), float(row[2]), z])
    temperatures = griddata(points, temps, dist_sec_points, method='linear', fill_value=default_temp)
    sectemps = list()
    dist_i = 0
    for i,z in enumerate(nerve_z_locs):
        if (z < block_start or z > block_end_past - section_length):
            sectemps.append(default_temp)
        else:
            sectemps.append(temperatures[dist_i])
            dist_i += 1
    # now we have temperatures for each section: default temp if outside dist
    w.writerow(sectemps)

temp_file.close()
pop_file.close()
 # all donezo
