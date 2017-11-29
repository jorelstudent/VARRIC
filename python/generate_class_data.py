#!/usr/bin/env python
"""
Generate a set of CLASS power spectra across a set of sample points in 
cosmological parameter space.
"""
from precompute_data import *
from load_data import load_hypercube
import os

# Directory containing 'class' executable
CLASS_ROOT = "/home/phil/jpl/software/class_public/"

PREFIX = "std" # Prefix to use for this run
NSAMP = 100 # No. of sample points in parameter space
SEED = 10 # Random seed to use for sampling
ZVALS = np.arange(0., 3., 0.5) # Redshifts to evaluate P(k) at

# Define parameter space to sample over
param_dict = {
    'h':            (0.55, 0.8),
    'Omega_cdm':    (0.35, 0.15),
    'Omega_b':      (0.018, 0.052),
    'A_s':          (1.5e-9, 2.5e-9),
    'n_s':          (0.94, 0.98)
}

# Get root for CLASS and CCL filenames
root = "%s/data/class/%s" % (os.path.abspath(".."), PREFIX)
ccl_root = "%s/data/ccl/%s" % (os.path.abspath(".."), PREFIX)

# Generate sample points on Latin hypercube
sample_points = generate_latin_hypercube( samples=NSAMP, param_dict=param_dict,
                                          class_root=CLASS_ROOT, seed=SEED )
save_hypercube("%s_params.dat" % root, sample_points)

"""
# Generate CLASS .ini files
print("Writing CLASS linear .ini files")
generate_class_ini(sample_points, root="%s_lin_std" % root, 
                   nonlinear=False, redshifts=ZVALS)
generate_class_ini(sample_points, root="%s_lin_pre" % root, 
                   nonlinear=False, redshifts=ZVALS)

print("Writing CLASS nonlinear .ini files")
generate_class_ini(sample_points, root="%s_nl_std" % root, 
                   nonlinear=True, redshifts=ZVALS)
generate_class_ini(sample_points, root="%s_nl_pre" % root, 
                   nonlinear=True, redshifts=ZVALS)

# Run CLASS on generated .ini files
print("Running CLASS on .ini files")
run_class(fname_pattern="%s_*_std_?????.ini" % root, 
          class_root=CLASS_ROOT, precision=False)
run_class(fname_pattern="%s_*_pre_?????.ini" % root, 
          class_root=CLASS_ROOT, precision=True)
"""

# Run CCL for the same sets of parameters
generate_ccl_pspec(sample_points, ccl_root, class_data_root="%s_lin_std" % root, 
                   zvals=ZVALS)

