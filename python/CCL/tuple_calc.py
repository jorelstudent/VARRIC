import numpy as np
import pyccl as ccl
import glob
import matplotlib.pyplot as plt
import pdb

#Get the parameters we are varing
#List of parameters that will be varied
param = ['h', 'Omega_cdm', 'Omega_b', 'A_s', 'n_s']
param_min = np.array([0.5, 0.1, 0.018, 1.5e-9, 0.93])
param_max = np.array([0.9, 0.4, 0.052, 2.5e-9, 0.99])
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

		print string_x, 'vs', string_y
		#Get the index value, form here we will replace our default_copy
		ind_x = param_copy.index(string_x)
		ind_y = param_copy.index(string_y)
		#Load our parameter values
		param_data = np.genfromtxt('/users/penafiel/JPL/data/tuple/' + string_x + '_vs_' + string_y + '.csv', skip_header=1)
		trial_arr = param_data[:,0] #Load the trial numbers
		for i in range(len(trial_arr)):
			trial = param_data[i,0]
			print 'Trial', trial
			x = float(param_data[i,1])
			y = float(param_data[i,2])
			default_copy[ind_x] = x
			default_copy[ind_y] = y

			#Run our pyccl Comsology
			cosmo = ccl.Cosmology(Omega_c=default_copy[1], Omega_b=default_copy[2], h=default_copy[0], A_s=default_copy[3], n_s=default_copy[4], transfer_function='boltzmann')

			#The 'simple' way I believe is to make a strings of the paths and just concatenate them
			#depending on which z values we're looking at
			#Probably a simpler way of generating an array of strings
			z_vals = ['1', '2', '3', '4', '5', '6']


			for j in range(len(z_vals)):
				z_val = z_vals[j]
				class_path_lin = '/Users/penafiel/JPL/class/output/tuple/' + string_x + '_vs_' + string_y + '_lin_%05d' %trial
				class_path_nl = '/Users/penafiel/JPL/class/output/tuple/' + string_x + '_vs_' + string_y + '_nl_%05d' %trial
				#iterating over the z_vals
				#Then concatenating our string files
				z_path = 'z%s_pk.dat' %z_val
				z_nl_path = 'z%s_pk_nl.dat' %z_val
				class_path_lin += z_path
				class_path_nl += z_nl_path

				k_lin_data = np.loadtxt(class_path_lin, skiprows=4)
				k_nl_data = np.loadtxt(class_path_nl, skiprows=4)
				k_lin = k_lin_data[:,0]
				k_nl = k_nl_data[:,0]
				k_lin *= default_copy[0]
				k_nl *= default_copy[0]
				
				#Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
				z = j * 0.5
				print 'Check z = %d' %z
				a = 1. / (1. + z)
				#Matter power spectrum for lin and nonlin
				pk_lin = ccl.linear_matter_power(cosmo, k_lin, a)

				pk_nl = ccl.nonlin_matter_power(cosmo, k_nl, a)

				#Transform these into lists and add header lines
				k_lin_list = k_lin.tolist()
				k_lin_list = ['k'] + k_lin_list

				k_nl_list = k_nl.tolist()
				k_nl_list = ['z=%d k' %z] + k_nl_list
				pk_lin_list = pk_lin.tolist()
				pk_nl_list = pk_nl.tolist()
				pk_lin_list =['pk_lin'] + pk_lin_list
				pk_nl_list = ['pk_nl'] + pk_nl_list
				ccl_path_lin = '/Users/penafiel/JPL/CCL-master/data_files/tuple/'  + string_x + '_vs_' + string_y + '_lin_%05d' %trial
				ccl_path_nl = '/Users/penafiel/JPL/CCL-master/data_files/tuple/'  + string_x + '_vs_' + string_y + '_nl_%05d' %trial
				ccl_path_lin += z_path
				ccl_path_nl += z_path
				np.savetxt(ccl_path_lin, np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')
				np.savetxt(ccl_path_nl, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')
				del pk_lin_list[:]
				del pk_nl_list[:]
				del pk_lin
				del pk_nl	
		x_ax += 1

#Do this for nonlinear case
print 'PERFORMING NONLINEAR'
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

		print string_x, 'vs', string_y
		#Get the index value, form here we will replace our default_copy
		ind_x = param_copy.index(string_x)
		ind_y = param_copy.index(string_y)
		#Load our parameter values
		param_data = np.genfromtxt('/users/penafiel/JPL/data/tuple/' + string_x + '_vs_' + string_y + '.csv', skip_header=1)
		trial_arr = param_data[:,0] #Load the trial numbers
		for i in range(len(trial_arr)):
			trial = param_data[i,0]
			print 'Trial', trial
			x = float(param_data[i,1])
			y = float(param_data[i,2])
			default_copy[ind_x] = x
			default_copy[ind_y] = y

			#Run our pyccl Comsology
			cosmo = ccl.Cosmology(Omega_c=default_copy[1], Omega_b=default_copy[2], h=default_copy[0], A_s=default_copy[3], n_s=default_copy[4], transfer_function='boltzmann')

			#The 'simple' way I believe is to make a strings of the paths and just concatenate them
			#depending on which z values we're looking at
			#Probably a simpler way of generating an array of strings
			z_vals = ['1', '2', '3', '4', '5', '6']

			#Do this for nonlinear case
			for j in range(len(z_vals)):
				z_val = z_vals[j]
				class_path_nl = '/Users/penafiel/JPL/class/output/tuple/' + string_x + '_vs_' + string_y + '_nl_%05d' %trial
				#iterating over the z_vals
				#Then concatenating our string files
				z_nl_path = 'z%s_pk_nl.dat' %z_val
				class_path_nl += z_nl_path

				k_nl_data = np.loadtxt(class_path_nl, skiprows=4)
				k_nl = k_nl_data[:,0]
				k_nl *= default_copy[0]
				
				#Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
				z = j * 0.5
				print 'Check z = %d' %z
				a = 1. / (1. + z)
				#Matter power spectrum for lin and nonlin

				pk_nl = ccl.nonlin_matter_power(cosmo, k_nl, a)

				#Transform these into lists and add header lines
				k_nl_list = k_nl.tolist()
				k_nl_list = ['z=%d k' %z] + k_nl_list
				pk_nl_list = pk_nl.tolist()
				pk_nl_list = ['pk_nl'] + pk_nl_list
				ccl_path_nl = '/Users/penafiel/JPL/CCL-master/data_files/tuple/'  + string_x + '_vs_' + string_y + '_nl_%05d' %trial
				ccl_path_nl += z_path
				np.savetxt(ccl_path_nl, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')
				del pk_nl_list[:]
				del pk_nl	
		x_ax += 1

#Do this for linear, precision
print 'PERFORMING LINEAR,PRECISION'
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

		print string_x, 'vs', string_y
		#Get the index value, form here we will replace our default_copy
		ind_x = param_copy.index(string_x)
		ind_y = param_copy.index(string_y)
		#Load our parameter values
		param_data = np.genfromtxt('/users/penafiel/JPL/data/tuple/' + string_x + '_vs_' + string_y + '.csv', skip_header=1)
		trial_arr = param_data[:,0] #Load the trial numbers
		for i in range(len(trial_arr)):
			trial = param_data[i,0]
			print 'Trial', trial
			x = float(param_data[i,1])
			y = float(param_data[i,2])
			default_copy[ind_x] = x
			default_copy[ind_y] = y

			#Run our pyccl Comsology
			cosmo = ccl.Cosmology(Omega_c=default_copy[1], Omega_b=default_copy[2], h=default_copy[0], A_s=default_copy[3], n_s=default_copy[4], transfer_function='boltzmann')

			#The 'simple' way I believe is to make a strings of the paths and just concatenate them
			#depending on which z values we're looking at
			#Probably a simpler way of generating an array of strings
			z_vals = ['1', '2', '3', '4', '5', '6']

			#Do this for the precision measurements
			for j in range(len(z_vals)):
				z_val = z_vals[j]
				print 'Precision measurements'
				class_path_lin = '/Users/penafiel/JPL/class/output/tuple/' + string_x + '_vs_' + string_y + '_lin_pre_%05d' %trial
				#iterating over the z_vals
				#Then concatenating our string files
				z_path = 'z%s_pk.dat' %z_val
				class_path_lin += z_path

				k_lin_data = np.loadtxt(class_path_lin, skiprows=4)
				k_lin = k_lin_data[:,0]
				k_lin *= default_copy[0]
				
				#Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
				z = j * 0.5
				print 'Check z = %d' %z
				a = 1. / (1. + z)
				#Matter power spectrum for lin and nonlin
				pk_lin = ccl.linear_matter_power(cosmo, k_lin, a)

				#Transform these into lists and add header lines
				k_lin_list = k_lin.tolist()
				k_lin_list = ['k'] + k_lin_list

				pk_lin_list = pk_lin.tolist()
				pk_lin_list =['pk_lin'] + pk_lin_list
				ccl_path_lin = '/Users/penafiel/JPL/CCL-master/data_files/tuple/' + string_x + '_vs_' + string_y + '_lin_pre_%05d' %trial
				ccl_path_lin += z_path
				np.savetxt(ccl_path_lin, np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')
		x_ax += 1
#Do this for nonlinear precision,
print 'PERFORMING NON LINEAR PRECISION'
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

		print string_x, 'vs', string_y
		#Get the index value, form here we will replace our default_copy
		ind_x = param_copy.index(string_x)
		ind_y = param_copy.index(string_y)
		#Load our parameter values
		param_data = np.genfromtxt('/users/penafiel/JPL/data/tuple/' + string_x + '_vs_' + string_y + '.csv', skip_header=1)
		trial_arr = param_data[:,0] #Load the trial numbers
		for i in range(len(trial_arr)):
			trial = param_data[i,0]
			print 'Trial', trial
			x = float(param_data[i,1])
			y = float(param_data[i,2])
			default_copy[ind_x] = x
			default_copy[ind_y] = y

			#Run our pyccl Comsology
			cosmo = ccl.Cosmology(Omega_c=default_copy[1], Omega_b=default_copy[2], h=default_copy[0], A_s=default_copy[3], n_s=default_copy[4], transfer_function='boltzmann')

			#The 'simple' way I believe is to make a strings of the paths and just concatenate them
			#depending on which z values we're looking at
			#Probably a simpler way of generating an array of strings
			z_vals = ['1', '2', '3', '4', '5', '6']

			for j in range(len(z_vals)):
				z_val = z_vals[j]
				print 'Precision measurements'
				class_path_nl = '/Users/penafiel/JPL/class/output/tuple/' + string_x + '_vs_' + string_y + '_nl_pre_%05d' %trial
				#iterating over the z_vals
				#Then concatenating our string files
				z_nl_path = 'z%s_pk_nl.dat' %z_val
				class_path_nl += z_nl_path

				k_nl_data = np.loadtxt(class_path_nl, skiprows=4)
				k_nl = k_nl_data[:,0]
				k_nl *= default_copy[0]
				
				#Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
				z = j * 0.5
				print 'Check z = %d' %z
				a = 1. / (1. + z)
				#Matter power spectrum for lin and nonlin
				pk_nl = ccl.nonlin_matter_power(cosmo, k_nl, a)

				#Transform these into lists and add header lines
				k_nl_list = k_nl.tolist()
				k_nl_list = ['z=%d k' %z] + k_nl_list
				pk_nl_list = pk_nl.tolist()
				pk_nl_list = ['pk_nl'] + pk_nl_list
				ccl_path_nl = '/Users/penafiel/JPL/CCL-master/data_files/tuple/' + string_x + '_vs_' + string_y + '_nl_pre_%05d' %trial
				ccl_path_nl += z_path
				np.savetxt(ccl_path_nl, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')


		x_ax += 1



		
