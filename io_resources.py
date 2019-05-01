import csv
import numpy as np
from scipy.interpolate import griddata

class FileWriter:
    """This csv-based file writer will package all relevant filewriting information"""
    def __init__(self, filename, path='./'):
        self.filename = filename
        self.filepath = path + filename
        self.file = open(self.filepath, 'wb')
        self.w = csv.writer(self.file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def filewriter_close(self):
        self.file.close()

    def filewriter_write(self, myiter):
        for line in myiter:
            self.w.writerow(line)

class FileReader:
    """This csv-based file reader will package all relevant filereading information"""
    def __init__(self, filename, path='./', delimeter='\t'):
        self.filename = filename
        self.filepath = path + filename
        self.file = open(self.filepath, 'r')
        self.r = csv.reader(self.file, delimiter=delimeter, quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def filereader_close(self):
        self.file.close()

    def filereader_read(self):
        output = list()
        for row in self.r:
            output.append(row)
        return output


class tempReader:

    def __init__(self, filename, path='./', splitstring='\t'):
        self.filename = filename
        self.filepath = path + filename
        self.r = open(self.filepath, 'r')
        self.splitstring = splitstring

    def readfile(self):
        data = list()
        for line in self.r:
            data.append(list(filter(lambda x: x != "",line.split(self.splitstring))))
        return data

    def tempdistread(self, pointscale=1.0, tempscale=1.0, x=0, y=0, z=0, swapxz=False):
        data = self.readfile()
        headers = list(data[:9])
        data = list(data[9:])
        points = list()
        temps = list()
        for line in data:
            points.append(list(map(lambda x: float(x) * pointscale,line[:3])))
            points[-1][0] += x
            points[-1][1] += y
            points[-1][2] += z
            if swapxz:
                temp_val = points[-1][0]
                points[-1][0] = points[-1][2]
                points[-1][2] = temp_val
            temps.append((float(line[3])-273.15))
        tempmin = min(temps)
        for i, temp in enumerate(temps):
            temps[i] = ((temp-tempmin)*tempscale) + tempmin # scale the gradient, not the whole dist
        return headers, points, temps

    def tempreader_close(self):
        self.r.close()
