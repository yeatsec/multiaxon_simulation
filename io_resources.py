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
    def __init__(self, filename, path='./'):
        self.filename = filename
        self.filepath = path + filename
        self.file = open(self.filepath, 'r')
        self.r = csv.reader(self.file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def filereader_close(self):
        self.file.close()

    def filereader_read(self):
        output = list()
        for row in self.r:
            output.append(row)
        return output

    def filereader_tempdistread(self):
        data = np.array(self.filereader_read())
        headers = data[:9,:]
        data = data[10:,:]
        data = np.vectorize(float, otypes=[float])(data)
        return headers, data[:,:3], data[:,3:]