from neuron import h
import numpy as np

h.tstop = 20.0
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop


class Fiber:
    """This object will package all of the
    data and relevant operations on 
    unmyelinated axons"""

    def __init__(self, diameter, location, length, section_count, record_begin, record_end):
        self.diam = diameter
        self.loc = location 
        self.l = length
        self.section_count = section_count 
        self.section_length = (length/section_count)
        self.section_sa = np.pi * self.diam * self.section_length / ((10000)**2)    # /cm2
        # initialize nrn sections
        self.sections = list()
        self.points = list()    # parallel list of points
        self.na_vectors = list()
        self.k_vectors = list()
        self.vector_points = list()
        self.vector_count = 0
        for section in range(section_count):
            self.points.append(Point([self.loc.getLoc()[0], self.loc.getLoc()[1], self.loc.getLoc()[2] + (self.section_length/2) + (section*self.section_length)]))
            self.sections.append(h.Section())
            self.sections[section].diam = self.diam
            self.sections[section].nseg = 1
            self.sections[section].insert("hh")
            self.sections[section].L = self.section_length
            if self.points[section].getLoc()[2] >= record_begin and self.points[section].getLoc()[2] <= record_end:
                # section is within recording area
                self.na_vectors.append(h.Vector(timesteps))
                self.na_vectors[-1].record(self.sections[section](0.5)._ref_ina) # accesses last element of list
                self.k_vectors.append(h.Vector(timesteps))
                self.k_vectors[-1].record(self.sections[section](0.5)._ref_ik)
                self.vector_points.append(self.points[section])
                self.vector_count += 1

            if section > 0: # connect section to previous section
                self.sections[section].connect(self.sections[section-1])
        self.stim = h.IClamp(0.5, sec=self.sections[5])
        self.stim.amp = 10000.0
        self.stim.delay = 0.0
        self.stim.dur = 0.5

    def getLoc(self):
        return self.loc

    def getDiam(self):
        return self.diam 

    def getLen(self):
        return self.l 
    
    def getSectionCount(self):
        return self.section_count 

    def get_na_vectors(self):
        return self.na_vectors

    def get_vector_count(self):
        return self.vector_count

    def get_k_vectors(self):
        return self.k_vectors

    def get_vector_points(self):
        return self.vector_points

    def getSectionSA(self):
        return self.section_sa

class Point:
    """This object packages 3D location info"""

    def __init__(self, location):
        self.x = location[0] 
        self.y = location[1] 
        self.z = location[2] 

    def getLoc(self):
        return [self.x, self.y, self.z]

    def getDist(self, other_point):
        return ((self.x - other_point.getLoc()[0])**2 + (self.y - other_point.getLoc()[1])**2 + (self.z - other_point.getLoc()[2])**2)**0.5