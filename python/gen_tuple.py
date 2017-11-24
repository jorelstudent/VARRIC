import numpy as np
import numpy.random as npr
import pdb
import itertools
import random

#This will generate sets of parameters as well as the ini files

#This Python script aims to generate parameter values UTILIZING Latin hypercubes
#Latin hypercube sampling is a constrained sampling scheme, which in theory should
#	yield more precise estimates compared to Monte Carlo sampling
#A simple case is the Latin square. It is a Latin square if there exists only one point in each row, column
#	based on the binning (i.e. number of samples)
#Might make a jupyter notebook to make it more easily seen, since that has picture


#Generates a list that looks like 00000, 00001, ..., xxxxx
#Change that second value if you want to have larger amount of trials
#Currently max is 99999
def num_trials(n_trials):
    n_trials_arr = []
    for i in range(n_trials):
        num = '{0:05}'.format(i)
        num = str(num)
        n_trials_arr.append(num)

    return np.asarray(n_trials_arr)

#This is for the standard set of parameters
def lhs_par_tuple(n_trials):

	N_trials = n_trials

	#List of parameters that will be varied
	param = ['h', 'Omega_cdm', 'Omega_b', 'A_s', 'n_s']
	param_min = np.array([0.5, 0.1, 0.02, 1.5e-9, 0.93])
	param_max = np.array([0.9, 0.4, 0.05, 2.5e-9, 0.99])
	weights = (param_max - param_min) / N_trials
	default = [0.67, 0.27, 0.045, 2.1e-9, 0.96]

	max_par = len(param) - 1 #Max number of plots on the x/y axis
	for i in range(max_par):
		y_ax = np.copy(i) + 1 #Parameter for the y values
		x_ax = 0 #Parameter for the x values
		while (x_ax < y_ax) & (x_ax < max_par):
			param_copy =  ['h', 'Omega_cdm', 'Omega_b', 'A_s', 'n_s']#Copies this so we can easily make our ini files
			default_copy = [0.67, 0.27, 0.045, 2.1e-9, 0.96]
			
			list_x = []
			list_y = []
			string_x = param[x_ax]
			string_y = param[y_ax]
			w_x = weights[x_ax]
			w_y = weights[y_ax]
			min_x = param_min[x_ax]
			min_y = param_min[y_ax]

			print string_x, 'vs', string_y
			#Generate a list of Ndim
			l = [range(N_trials) for j in range(2)] #2 dimensions
			
			while len(l[0]) != 0:
				x = random.choice(l[0])
				y = random.choice(l[1])

				list_x.append(x)
				list_y.append(y)

				#Removes the numbers that were already chosen, since Latin hypercubes want one item
				#per row
				l[0].remove(x)
				l[1].remove(y)
			
			#Make into arrays to do some stuff to it
			list_x_arr = np.asarray(list_x)
			list_y_arr = np.asarray(list_y)

			#We then center these values, don't forget to add by the min value
			val_x = ((list_x_arr + 0.5) * w_x) + min_x
			val_y = ((list_y_arr + 0.5) * w_y) + min_y

			#Put these back into the list, so we can add some headers
			val_x_list = val_x.tolist()
			val_y_list = val_y.tolist()

			val_x_list = ['%s' %string_x] + val_x_list
			val_y_list = ['%s' %string_y] + val_y_list
			
			#Get the number of trials
			num_trials_arr = num_trials(n_trials)
			num_trials_list = num_trials_arr.tolist()
			num_trials_list = ['Trial #'] + num_trials_list

			np.savetxt('/Users/penafiel/JPL/data/tuple/' + string_x + '_vs_' + string_y + '.csv', np.transpose([num_trials_list, val_x_list, val_y_list]), fmt='%-20s')
			
			#make the ini files
			#Removes the ones that we varied
			ind_x = param_copy.index(string_x)
			ind_y = param_copy.index(string_y)
			def_x = default_copy[ind_x]
			def_y = default_copy[ind_y]
			param_copy.remove(string_x)
			param_copy.remove(string_y)
			default_copy.remove(def_x)
			default_copy.remove(def_y)

			#Now we make the ini files
			#For the linear case
			for i in range(len(num_trials_arr)):
				trial = num_trials_arr[i]
				x_val = val_x[i]
				y_val = val_y[i]

				file = open('../class/ini_files/tuple/' + string_x + '_vs_' + string_y + '_lin_%s.ini' %trial, 'w')
				
				#Put the values in
				file.write(string_x + ' = %s\n' %x_val)
				file.write(string_y + ' = %s\n' %y_val)
				file.write('root = output/tuple/' + string_x + '_vs_' + string_y + '_lin_%s\n' %trial)
				
				#The cosmological parameters we didn't change in the combinations
				for j in param_copy:
					index = param_copy.index(j)
					j_val = default_copy[index]
					file.write(j + ' = %s\n' %j_val)
				
				#Placing the constants, pardon the syntax
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

			#For the nonlinear case
			for i in range(len(num_trials_arr)):
				trial = num_trials_arr[i]
				x_val = val_x[i]
				y_val = val_y[i]

				file = open('../class/ini_files/tuple/' + string_x + '_vs_' + string_y + '_nl_%s.ini' %trial, 'w')
				
				#Put the values in
				file.write(string_x + ' = %s\n' %x_val)
				file.write(string_y + ' = %s\n' %y_val)
				file.write('root = output/tuple/' + string_x + '_vs_' + string_y + '_nl_%s\n' %trial)
				
				#The cosmological parameters we didn't change in the combinations
				for j in param_copy:
					index = param_copy.index(j)
					j_val = default_copy[index]
					file.write(j + ' = %s\n' %j_val)
				
				#Placing the constants, pardon the syntax
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

			#For the linear, precision case
			for i in range(len(num_trials_arr)):
				trial = num_trials_arr[i]
				x_val = val_x[i]
				y_val = val_y[i]

				file = open('../class/ini_files/tuple/' + string_x + '_vs_' + string_y + '_lin_pre_%s.ini' %trial, 'w')
				
				#Put the values in
				file.write(string_x + ' = %s\n' %x_val)
				file.write(string_y + ' = %s\n' %y_val)
				file.write('root = output/tuple/' + string_x + '_vs_' + string_y + '_lin_pre_%s\n' %trial)
				
				#The cosmological parameters we didn't change in the combinations
				for j in param_copy:
					index = param_copy.index(j)
					j_val = default_copy[index]
					file.write(j + ' = %s\n' %j_val)
				
				#Placing the constants, pardon the syntax
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

			#For the nonlinear, precision case
			for i in range(len(num_trials_arr)):
				trial = num_trials_arr[i]
				x_val = val_x[i]
				y_val = val_y[i]

				file = open('../class/ini_files/tuple/' + string_x + '_vs_' + string_y + '_nl_pre_%s.ini' %trial, 'w')
				
				#Put the values in
				file.write(string_x + ' = %s\n' %x_val)
				file.write(string_y + ' = %s\n' %y_val)
				file.write('root = output/tuple/' + string_x + '_vs_' + string_y + '_nl_pre_%s\n' %trial)
				
				#The cosmological parameters we didn't change in the combinations
				for j in param_copy:
					index = param_copy.index(j)
					j_val = default_copy[index]
					file.write(j + ' = %s\n' %j_val)
				
				#Placing the constants, pardon the syntax
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


			x_ax += 1	
#Running the code
if __name__ == "__main__":
	n_trials = 100
	lhs_par_tuple(n_trials)
