#!/usr/bin/env python
"""
Generate a set of CLASS power spectra across a set of sample points in 
cosmological parameter space.
"""
from precompute_data import *
import os

# Directory containing 'class' executable
CLASS_ROOT = "/home/phil/jpl/software/class_public/"

PREFIX = "std" # Prefix to use for this run
NSAMP = 100 # No. of sample points in parameter space
SEED = 10 # Random seed to use for sampling
ZVALS = np.arange(0., 3., 0.5) # Redshifts to evaluate P(k) at

# Define parameter space to sample over
param_dict = {
    'h':            (0.5, 0.9),
    'Omega_cdm':    (0.4, 0.1),
    'Omega_b':      (0.018, 0.052),
    'A_s':          (1.5e-9, 2.5e-9),
    'n_s':          (0.93, 0.99)
}

# Get filename root
root = "%s/data/class/%s" % (os.path.abspath(".."), PREFIX)

# Generate sample points on Latin hypercube
sample_points = generate_latin_hypercube( samples=NSAMP, param_dict=param_dict,
                                          class_root=CLASS_ROOT, seed=SEED )
save_hypercube("%s_params.dat" % root, sample_points)

# Generate CLASS .ini files
print("Writing CLASS linear .ini files")
generate_class_ini(sample_points, root="%s_lin" % root, 
                   nonlinear=False, redshifts=ZVALS)
print("Writing CLASS nonlinear .ini files")
generate_class_ini(sample_points, root="%s_nl" % root, 
                   nonlinear=True, redshifts=ZVALS)

#fname_pattern = '../class/ini_files/wcdm/*_lin_0*.ini'

#run_class(fname_pattern=None, precision=False)
