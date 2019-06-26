# User Manual for Multiaxon Simulation

Eric Yeats

Vanderbilt Class of 2019

B.E. Computer Engineering with a Minor in Interdisciplinary Neuroscience

May 23, 2019

eric.c.yeats@vanderbilt.edu

## Introduction

### Goals

The goals of the simulation are:
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
    
## Setup Manual

### Preparing the NEURON Environment with Python 2.7

The NEURON environment was acquired via the Anaconda package manager. In the future, package management with a dedicated virtual environment is recommended. The necessary python packages are:

* neuron
* numpy
* scipy
* matplotlib
* csv (should be out-of-the-box)

A few custom modules were also written in order to simplify the simulation scripts and to make reuseable code for IO operations. These scripts are io_resources.py and model_resources.py, and they're included in the repository.

### Compiling the NEURON NMODL File

Follow instructions online (specific to your OS) on how to compile NMODL files. NMODL files become relevant in the code in model_resources.py, where the NEURON mechanism defined by the compiled NMODL file is inserted into each section of each axon.

IMPORTANT: If you want to change the name of the mechanism that NEURON uses, you must go into model_resources and change the suffix of the accessed state variables associated with the mechanism. This code can be found in model_resources.py in Fiber::init. FYI, the TITLE field of the NMODL file is what determines this suffix, not the name of the NMODL file itself. Could save you a headache down the line..

## Script Manual

### Generating an Axon Population: _populations/fit_pop_gen.py_

This script is used to generate an evenly-spaced 2D grid of axons of varying diameter arranged in a nerve shape. The grid represents a 'cross section' of the nerve, with each of the axons in the 2D grid perpendicular to the plane of the 2D grid.

The axon diameter pdf is enclosed in *lpac_diam()*, a function which returns a random sample of the pdf. The continuous pdf was fit to discrete data reported in Bedini *et al.* 2000. 

The script will generate a file of all diameters and their specific location wrt to the simulation origin. This file will need to be paired with a temperature distribution in the next step, a process in which the anticipated locations of NEURON segments, given a population, are interpolated with raw temperature distribution data.


### Pairing an Axon Population with a Tmeperature Distribution for Simulation Prep: *gentemp.py*

This script, given a raw temperature distribution and a population layout, produces a list of interpolated temperatures for NEURON segments associated with each axon in a population.

Important Parameters:
* default_temp - this defines the base temperature of the fluid the nerve is immersed in
* nerve_length - is the length of the anticipated simulated nerve, make sure this matches that in the simulation script
* section_length - the length of each NEURON section used to compose the axons in the simulation, make sure this matches that in the simulation script. this will also determine the number of sections used to compose each axon and thus the number of temperatures interpolated from the temperature distribution for each axon
* block_length - the length along the axon of which the NEURON sections have temperatures interpolated from the raw temperature distribution data (further explained in the 'Geometry' section). All sections located outside of the block_length assume the default_temp parameter as their temperature.

This will generate a file used by the simulation itself.

IMPORTANT: This script only needs to be run if the temperature distribution or the *geometry* of a simulation changes. For example, if the number of sections in each axon, the nerve length, the block length, or the spacing between axons is changed, this script needs to be re-run. The script DOES NOT need to be run if the only thing different between simulations is the diamter of each axon used to compose the nerve. The sections would all be located in the same spots wrt the temperature distribution in that case.