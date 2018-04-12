from neuron import h
import numpy as np

print "\n i see model_resources\n"

h.tstop = 20.0
dt = 0.025
timesteps = int(h.tstop/dt)
duration = h.tstop

resistance = 300.0 * 10000.0 # ohm * um

# ^^ these are redeclared eventually 

def init_model(t_stop, delta_t, resist):
    h.tstop = t_stop
    dt = delta_t
    timesteps = int(h.tstop/dt) 
    duration = h.tstop 
    resistance = resist
    print "m_r timesteps: ", timesteps

def rModel(distance): # returns scalar that should be multiplied by a current value
    return resistance / (4 * np.pi * distance)


class Fiber:
    """This object will package all of the
    data and relevant operations on 
    unmyelinated axons"""

    def __init__(self, diameter, location, length, section_count, record_begin, record_end, mod_name):
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
            self.sections[section].insert(mod_name)
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
        self.stim.amp = 20.0
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

    def getCurrentSignalAt(self, index): # returns current signal for section at given index
        na_cur_signal = self.na_vectors[index]
        k_cur_signal = self.k_vectors[index]
        sig_len = len(na_cur_signal)
        current_signal = [0.0] * sig_len
        for i in range(sig_len):
            current_signal[i] = self.section_sa * (na_cur_signal[i] + k_cur_signal[i])
        return current_signal

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

class voltPoint:
    """This class packages 3D location with a signal waveform component.
    To be used for recording the extracellular potential of a CAP"""

    def __init__(self, pt, sigSize):
        """initializes a vPoint at Point pt with empty signal vector of size size"""
        self.loc = pt
        self.signal = [0.0] * sigSize

    def clearSignal(self):
        for i in range(len(self.signal)):
            self.signal[i] = 0.0

    def getSignal(self):
        return self.signal

    def addSignalAt(self, index, value):
        try:
            self.signal[index] += value
        except:
            print "\nexception generated from index: ", index

    def addVoltFromPoint(self, srcPoint, srcSignal):
        sigLength = len(srcSignal) - 1 # vectors seem to have an extra empty value at end
        dist = self.loc.getDist(srcPoint)
        for index in range(sigLength):
            self.addSignalAt(index, srcSignal[index]*rModel(dist))

    def addVoltFromFiber(self, fib):
        fib_vec_points = fib.get_vector_points()
        for i in range(len(fib.get_vector_points())):
            print "vector size: ", len(fib.getCurrentSignalAt(i))
            self.addVoltFromPoint(fib_vec_points[i], fib.getCurrentSignalAt(i))



class voltCuff:
    """This class packages a set of vPoints together in a ring fomation to resemble
    a Monopolar cuff. can use multiple to resemble Bipolar and Tripolar recording schemes"""
    def __init__(self, centerPoint, sigSize, radius, numPoints):
        self.rec_points = list()
        self.sigSize = sigSize
        terminal = voltPoint(centerPoint, sigSize)
        radians = np.linspace(0, 2*np.pi, numpoints, endpoint=False)
        for rad in radians: # arrange voltage points in circle
            self.rec_points.append(voltPoint([radius*np.cos(rad) + centerPoint.getLoc()[0], 
                radius*np.sin(rad) + centerPoint.getLoc()[1],
                centerPoint.getLoc()[2]]))

    def calculateSignal(self):
        self.terminal.clearSignal()
        for rPoint in self.rec_points:
            r_sig = rPoint.getSignal()
            for i in self.sigSize:
                self.terminal.addSignalAt(i, r_sig[i]/self.numPoints)


    def getSignal(self):
        return terminal.getSignal()
            

    def addVoltFromSrc(self, srcPoint, srcSignal):
        # incorporate resistive model here
        for rPoint in self.rec_points:
            rPoint.addVoltFromPoint(srcPoint, srcSignal)

    def addVoltFromFiber(self, fib):
        # iterate through sections and call addVoltFromSrc
        for rPoint in self.rec_points:
            rPoint.addVoltFromFiber(self, fib)

