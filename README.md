# User Manual for Multiaxon Simulation

Eric Yeats
Vanderbilt Class of 2019
B.E. Computer Engineering with a Minor in Interdisciplinary Neuroscience
eric.c.yeats@vanderbilt.edu

May 23, 2019

## Introduction

### Goals

The goal of the simulation is:
    * to use a pdf of axon diameters to generate axons of varying diameter arranged in space in order to approximate a 3d morphology of the Left-Pleural-Abdominal-Connective (LPAC) nerve of Aplysia californica
    * to apply a 3d temperature distribution from simulated data (or from simple parameters) to the 3d LPAC nerve
    * to excite all axons in the population proximally, record their activity as they conduct action potentials through the region of the nerve immersed in the 3d temperature distribution, and to establish which axons are still 'active' and which are completely inhibited in the distal portion (post 3d-temp distribution)
    * to calculate the resultant compound neural action potential (CNAP) recorded at an arbitrary point in 3d isotropic space with respect to the nerve

### Required Tools and Intended Workflow

This simulation suite is written in Python 2.7, but the core of the biophysical simulation is powered by NEURON. This means that to run this simulation, Python 2.7 must have the NEURON module installed. Additionally, the simulation suite requires that the csv, matplotlib, numpy, and scipy modules are installed.
More detailed explanations of the scripts are provided later, but the main components of the simulation are:
    * a pre-simulated temperature distribution represented as a cloud of temperature values within space
    * a set of axon population generation scripts (/populations/fit_pop_gen.py, /populations/uni_pop_gen.py)
    * a script (gentemp.py) which generates a temperature distribution file readable by the simulation by specifying a generated axon population file and a pre-simulated temperature distribution file
    * the NEURON-integrated simulation (apl_inhib_model.py) which uses the population file and output of gentemp.py to generate a full nerve morphology immersed in a temperature simulation. the output of the simulation is a file specifying the diameter of each axon, the axon's location, and whether or not it was inhibited ('..._tempdataxz_stat.csv'), and a file containing the recorded CNAP for the simulation ('..._tempdataxz_cap.csv')
    * a script ('..._statscript.py') which reads a '..._tempdataxz_stat.csv' file and generates figures of the cross-section of the nerve which depict the morphology of the nerve and whether or not an axon at a certain location is inhibited
    * a script ('..._statcap.py') which reads a '..._tempdataxz_cap.csv' file (or multiple) and generates a plot of all CNAPs specified in the '..._tempdataxz_cap.csv' file list. the script also generates a scatterplot which compares the inhibition level of each nerve in each simulation to the Area Under the Curve measurement of the corresponding CNAP


### Geometry

The geometry of the simulation is configurable, but it follows this general formula:
    * The proximal end of the nerve is centered at (0, 0, 0) (um). Imagine that the nerve is a cylinder - the central point of the circle that makes up the base of the cylinder is located at (0, 0, 0) (um). The lengthwise axis of the nerve stretches along the z axis from (0, 0, 0) to (0, 0, fiber_length) (um)
    * The axons are arranged within an equally-spaced grid structure within the cylindrical nerve. The grid is positioned in the xy plane which intersects the nerve orthogonally (length of nerve is in z direction). The axons arranged in the grid structure within the nerve are parallel for the entire length of the nerve.
    * Each axon in the nerve is stimulated via current injection at 'stim_z' distance along the nerve such that the current injection point would be at (fib_x, fib_y, stim_z) for each fiber with cross-sectional nerve coordinates fib_x and fib_y (um).
    * The temperature distribution is centered at (0, 0, block_location) (um). This means that the center of the temperature distribution is located along the length of the nerve at a distance 'block_location' from the proximal end of the nerve.
    * On either side of the center of the temperature distribution located at 'block_length' along the central axis of the nerve, the temperature distribution is applied to all sections that are within 'block_length/2' of that location, with 'block_length' specifying the _*total length*_ from the start of the temperture distribution applied to the nerve to the end of the temperature distribution applied to the nerve. If the block_length is less than the original temperature simulation data's length, only the portion of the temperature distribution within block_length of the center of the temperature distribution is used.
    * The membrane current, a metric used to compute the CNAP, of each of the NEURON sections is recorded near the distal end of the nerve, centered around 'record_z'. Sections within 'recording_radius' around 'record_z' are used.
    * The membrane potential of each of the axons is measured at their distal end to determine whether there is still an action potential. Simple thresholding is used to determine this. 
    * The point for which the resultant CNAP is calculated is located at (0, nerve_radius + rec_dist, record_z) (um), where nerve_radius is the radius of the cylindrical nerve model and the rec_dist is the orthogonal distance away from the nerve surface to the recording point.
    
