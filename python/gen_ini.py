from __future__ import print_function ##Note: This is a Python 2 script
from subprocess import call
import numpy as np
import pdb

#Define a function that loads the txt file and iterates over the number of trials
#Creating a different .ini file per trial

#Call the files as string, make the rest floats later
data = np.genfromtxt('/Users/penafiel/JPL/data/par_stan1.csv', dtype='str', skip_header=1)

#This gets the trial number into an arr
trial_arr = data[:,0]

#These generate the ini files
#This ones for the linear case
#If you want it to output specific stuff look at output
#If lensing == yes, make sure your output includes TCl and the others
for i in range(len(trial_arr)):
    trial = data[i,0]
    file = open('../class/ini_files/lhs_lin_%s.ini' %trial, 'w')
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])

    #Put these in
    file.write('h = %s\n' %h)
    file.write('Omega_b = %s\n' %Omega_b)
    file.write('Omega_cdm = %s\n' %Omega_cdm)
    file.write('A_s = %s\n' %A_s)
    file.write('n_s = %s\n' %n_s)
    file.write('root = output/lin/lhs_lin_%s\n' %trial)

    #Placing the constants, pardon the syntax, figuring out some more
    file.write('T_cmb = 2.7255\n \
N_ur = 3.046\n\
Omega_dcdmdr = 0.0\n\
Gamma_dcdm = 0.0 \n\
N_ncdm = 0\n\
Omega_k = 0.\n\
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
z_pk = 0.,0.5,1.,1.5,2.,2.5\n\
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
output_verbose = 1\n')
    file.close()


#This is for the nonlinear case
for i in range(len(trial_arr)):
    trial = data[i,0]
    file = open('../class/ini_files/lhs_nonlin_%s.ini' %trial, 'w')
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])

    #Put these in
    file.write('h = %s\n' %h)
    file.write('Omega_b = %s\n' %Omega_b)
    file.write('Omega_cdm = %s\n' %Omega_cdm)
    file.write('A_s = %s\n' %A_s)
    file.write('n_s = %s\n' %n_s)
    file.write('root = output/nonlin/lhs_nonlin_%s\n' %trial)

    #Placing the constants, pardon the syntax, figuring out some more
    file.write('T_cmb = 2.7255\n \
N_ur = 3.046\n\
Omega_dcdmdr = 0.0\n\
Gamma_dcdm = 0.0 \n\
N_ncdm = 0\n\
Omega_k = 0.\n\
Omega_fld = 0\n\
Omega_scf = 0\n\
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
non linear = halofit\n\
modes = s\n\
lensing = no\n\
ic = ad\n\
gauge = synchronous\n\
P_k_ini type = analytic_Pk\n\
k_pivot = 0.05\n\
alpha_s = 0.\n\
P_k_max_h/Mpc = 10.\n\
l_max_scalars = 2500\n\
z_pk = 0.,0.5,1.,1.5,2.,2.5\n\
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
output_verbose = 1\n')
    file.close()

#Now do the same for precision measurements

for i in range(len(trial_arr)):
    trial = data[i,0]
    file = open('../class/ini_files/lhs_lin_pk_%s.ini' %trial, 'w')
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])

    #Put these in
    file.write('h = %s\n' %h)
    file.write('Omega_b = %s\n' %Omega_b)
    file.write('Omega_cdm = %s\n' %Omega_cdm)
    file.write('A_s = %s\n' %A_s)
    file.write('n_s = %s\n' %n_s)
    file.write('root = output/lin/lhs_lin_pk_%s\n' %trial)

    #Placing the constants, pardon the syntax, figuring out some more
    file.write('T_cmb = 2.7255\n \
N_ur = 3.046\n\
Omega_dcdmdr = 0.0\n\
Gamma_dcdm = 0.0 \n\
N_ncdm = 0\n\
Omega_k = 0.\n\
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
z_pk = 0.,0.5,1.,1.5,2.,2.5\n\
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
output_verbose = 1\n')
    file.close()


#This is for the nonlinear case
for i in range(len(trial_arr)):
    trial = data[i,0]
    file = open('../class/ini_files/lhs_nonlin_pk_%s.ini' %trial, 'w')
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])

    #Put these in
    file.write('h = %s\n' %h)
    file.write('Omega_b = %s\n' %Omega_b)
    file.write('Omega_cdm = %s\n' %Omega_cdm)
    file.write('A_s = %s\n' %A_s)
    file.write('n_s = %s\n' %n_s)
    file.write('root = output/nonlin/lhs_nonlin_pk_%s\n' %trial)

    #Placing the constants, pardon the syntax, figuring out some more
    file.write('T_cmb = 2.7255\n \
N_ur = 3.046\n\
Omega_dcdmdr = 0.0\n\
Gamma_dcdm = 0.0 \n\
N_ncdm = 0\n\
Omega_k = 0.\n\
Omega_fld = 0\n\
Omega_scf = 0\n\
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
non linear = halofit\n\
modes = s\n\
lensing = no\n\
ic = ad\n\
gauge = synchronous\n\
P_k_ini type = analytic_Pk\n\
k_pivot = 0.05\n\
alpha_s = 0.\n\
P_k_max_h/Mpc = 10.\n\
l_max_scalars = 2500\n\
z_pk = 0.,0.5,1.,1.5,2.,2.5\n\
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
output_verbose = 1\n')
    file.close()

