#### Simulation of optic IR inhibition on an Aplysia Fascinata LPAC nerve

The population_generator scripts create lists of randomly placed axons generated from a lognormal distribution of fiber diameters and saves them to a file.
The model_demo script reads in a population file and temperature distribution. The heat distribution is applied to the center of the simulated nerve and inhibition occurs. The inhibition of the axons is recorded and the corresponding CAP is calculated at the end of the nerve.

The model_demo script outputs the inhibition record and the calculated CAP signal. statscript.py visualizes the inhibition record and statcap.py visualizes the calculated CAP signal. Example data are available.
