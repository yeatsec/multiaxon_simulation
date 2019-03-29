import csv
import model_resources as m_r

pop_file = ""

pop_path = ""

section_length = 100 # um

pop_file = open(pop_path, mode='rU')
read = csv.reader(pop_file, delimiter='\t', quotechar='|')
interp_file = open(out_name, mode='wU')
write = csv.writer(interp_file, delimiter='\t', quotechar='|')


for row in read:
    nerve_x.append(float(row[1]))
    nerve_y.append(float(row[2]))
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
pop_file.close()