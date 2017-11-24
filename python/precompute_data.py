import numpy as np
import os
import subprocess
import random
import glob


def save_hypercube(fname, sample_points):
    """
    Save a Latin hypercube to disk as a text file. Parameter columns will be 
    ordered alphabetically by name.
    
    Parameters
    ----------
    fname : str
        Filename for output file.
    sample_points : dict
        Dictionary containing parameter names (keys) and array of parameter 
        values for all sample points (values).
    """
    # Get parameter names and build header
    pnames = sample_points.keys()
    pnames.sort()
    hdr = " ".join(pnames)
    
    # Build array
    dat = np.column_stack([sample_points[p] for p in pnames])
    np.savetxt(fname, dat, header=hdr, fmt="%4.4e")
    print("Saved hypercube to '%s'." % fname)
    

def generate_latin_hypercube(samples, param_dict, class_root, seed=10):
    """
    Generate a Latin hypercube for a given set of parameters.
    
    Parameters
    ----------
    samples : int
        Number of samples points to draw from the hypercube.
        
    param_dict : dict
        Dictionary containing parameter names (keys) and tuple with min/max. 
        values (values).
        
    class_root : str
        Path to directory containing 'class' executable.
        
    seed : int, optional
        Random seed to use when sampling from hypercube.
    
    Returns
    -------
    sample_points : dict
        Dictionary containing parameter names (keys) and array of parameter 
        values for all sample points (values).
    """
    # Set random seed
    random.seed(seed)
    
    # Create dictionary to hold sampled parameter values
    sample_points = {}
    for key in param_dict.keys():
        sample_points[key] = np.zeros(samples)
    Ndim = len(param_dict.keys())
    pnames = [key for key in param_dict.keys()]
    
    # List of indices for each dimension
    l = [range(samples) for j in range(Ndim)]
    
    # Generate samples until there are no indices left to choose
    for i in range(samples):
        
        # Randomly choose index and then remove the number that was chosen 
        # (Latin hypercubes require at most one item per row and column)
        for j, p in enumerate(pnames):
            pmin, pmax = param_dict[p]
            idx = random.choice(l[j])
            
            # Get value at this sample point (add 0.5 to idx get bin centroid)
            sample_points[p][i] = pmin + (pmax - pmin) \
                                * (idx + 0.5) / float(samples)
            l[j].remove(idx) # Remove choice from list (sampling w/o replacement)
    
    return sample_points


def generate_class_ini(sample_points, root, nonlinear=False,
                       redshifts=np.arange(0., 3., 0.5)):
    """
    Generate CLASS .ini files for a set of parameters.
    
    Parameters
    ----------
    sample_points : dict
        Dictionary containing parameter names (keys) and array of parameter 
        values for all sample points (values).
        
    root : str
        Path of directory in which .ini files should be stored.
    
    nonlinear : bool, optional
        Whether CLASS should return the linear or nonlinear (halofit) power 
        spectrum. Default: False.
    
    redshifts : array_like, optional
        Array of redshift values at which P(k) should be calculated. Default: 
        Five bins from 0.0 to 2.5 in increments of 0.5.
    """
    # Get user-defined parameter names
    pnames = sample_points.keys()
    Nsamp = sample_points[pnames[0]].size
    
    # Loop over sample points
    for i in range(Nsamp):
        if i % 10 == 0: print("  Writing CLASS .ini file %d / %d" % (i, Nsamp))
        
        # Open file for writing
        f = open("%s_%05d.ini" % (root, i), 'w')
        
        # Write output location into file (will be same as .ini file location)
        f.write('root = %s_%05d\n' % (root, i))
        
        # Write user-defined cosmo parameters into file
        for p in pnames:
            # Handle commonly-used params that CLASS uses different names for
            if p == 'w0' or p == 'w_0':
                f.write("w0_fld = %e\n" % sample_points[p][i])
            elif p == 'wa' or p == 'w_a':
                f.write("wa_fld = %e\n" % sample_points[p][i])
            else:
                # Generic user-defined parameters
                f.write("%s = %e\n" % (p, sample_points[p][i]))
        
        # Write output redshifts to file
        f.write("z_pk = %s\n" % (",".join(["%3.3f" % z for z in redshifts])))
        
        # Write nonlinear switch to file, if specified
        if nonlinear: f.write("non linear = halofit\n")
        
        # Write curvature parameter
        if 'Omega_k' not in pnames: f.write('Omega_k = 0.0\n')
        
        # Add various default CLASS settings to file
        defaults = "T_cmb = 2.7255\n \
N_ur = 3.046\n\
Omega_dcdmdr = 0.0\n\
Gamma_dcdm = 0.0 \n\
N_ncdm = 0\n\
Omega_fld = 0\n\
Omega_scf = 0\n\
a_today = 1.\n\
YHe = BBN\n\
recombination = RECFAST\n\
reio_parametrization = reio_camb\n\
z_reio = 11.357\n\
reionization_exponent = 1.5\n\
reionization_width = 0.5\n\
helium_fullreio_redshift = 3.5\n\
helium_fullreio_width = 0.5\n\
annihilation = 0.\n\
annihilation_variation = 0.\n\
annihilation_z = 1000\n\
annihilation_zmax = 2500\n\
annihilation_zmin = 30\n\
annihilation_f_halo = 20\n\
annihilation_z_halo = 8\n\
on the spot = yes\n\
decay = 0.\n\
output = mPk\n\
modes = s\n\
lensing = no\n\
ic = ad\n\
gauge = synchronous\n\
P_k_ini type = analytic_Pk\n\
k_pivot = 0.05\n\
alpha_s = 0.\n\
P_k_max_h/Mpc = 10.\n\
l_max_scalars = 2500\n\
headers = yes\n\
format = class\n\
write background = no\n\
write thermodynamics = no\n\
write primordial = no\n\
write parameters = yeap\n\
input_verbose = 1\n\
background_verbose = 1\n\
thermodynamics_verbose = 1\n\
perturbations_verbose = 1\n\
transfer_verbose = 1\n\
primordial_verbose = 1\n\
spectra_verbose = 1\n\
nonlinear_verbose = 1\n\
lensing_verbose = 1\n\
output_verbose = 1\n"
        f.write(defaults)
        f.close()


def run_class(fname_pattern, precision=False):
    """
    Run CLASS on a set of .ini files.
    
    Parameters
    ----------
    fname_pattern : str
        
        
    precision : bool, optional
        Whether to run CLASS in high-precision mode (using the pk_ref.pre 
        precision file).
    """
    # Get CLASS .ini files that will be run
    #fname_pattern = '../class/ini_files/wcdm/*_lin_0*.ini'
    fnames = [f for f in glob.iglob(fname_pattern)]

    for i, filename in enumerate(fnames):
        print("CLASS run %d / %d (%s)" % (i, len(fnames), filename))
        #Calls the class executable for the files
        #subprocess.call(['./class', '%s' % filename])#, stdout = subprocess.PIPE)
        
        # Get and save the output
        cmd = ['%s/class' % CLASS_ROOT, filename]
        if precision: cmd += ['pk_ref.pre',]
        stdout = subprocess.check_output(cmd)
        basefile = os.path.splitext('%s' % filename)[0]
        file = open('%s.txt' % basefile, 'w')
        file.write(stdout)
        file.close()

if __name__ == '__main__':
    run_class()
