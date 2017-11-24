import numpy as np
import pyccl as ccl
import glob
import matplotlib.pyplot as plt
import pdb

#We are going to get the numbers generated from the gen_par.py file for CLASS
#They are the same variables, so all we need to do is rename them to the proper name

#Cal the files as string, make the rest floats later
data = np.genfromtxt('/Users/penafiel/JPL/data/par_stan1.csv', dtype='str', skip_header=1)

#This gets the trial number into an arr
trial_arr = data[:,0]

#Perform the calculation for each set of parameters
#We will store both the linear and nonlinear cases

#Initialize variables that won't change

#k = np.logspace(-5., 1., 100) #Wavenumber

#k_list = k.tolist()
#k_list = ['k'] + k_list

#pdb.set_trace()
for i in range(len(trial_arr)):
	trial = data[i,0]
	print 'Performing trial %s' %trial
	h = float(data[i,1])
	omega_b = float(data[i,2]) #/ h**2
	omega_cdm = float(data[i,3]) #/ h**2
	A_s = float(data[i,4])
	n_s = float(data[i,5])
	cosmo = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
	#Get the k values, directly from CLASS
	#Has to be a simpler way of automating this
	#The 'simple' way I believe is to make a strings of the paths and just concatenate them
	#depending on which z values we're looking at
	#Probably a simpler way of generating an array of strings
	z_vals = ['1', '2', '3', '4', '5', '6']
	for j in range(len(z_vals)):
		z_val = z_vals[j]
		class_path_lin = '/Users/penafiel/JPL/class/output/lin/lhs_lin_%s' %trial
		class_path_nl = '/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_%s' %trial
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
		k_lin *= h
		k_nl *= h
		
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
		ccl_path_lin = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_%s' %trial
		ccl_path_nl = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_%s' %trial
		ccl_path_lin += z_path
		ccl_path_nl += z_path
		np.savetxt(ccl_path_lin, np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')
		np.savetxt(ccl_path_nl, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')
    

		del pk_lin_list[:]
		del pk_nl_list[:]
		del pk_lin
		del pk_nl



#Do this for the precision values

for i in range(len(trial_arr)):
	trial = data[i,0]
	print 'Performing trial %s' %trial
	h = float(data[i,1])
	omega_b = float(data[i,2]) #/ h**2
	omega_cdm = float(data[i,3]) #/ h**2
	A_s = float(data[i,4])
	n_s = float(data[i,5])
	cosmo = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
	#Get the k values, directly from CLASS
	#Has to be a simpler way of automating this
	#The 'simple' way I believe is to make a strings of the paths and just concatenate them
	#depending on which z values we're looking at
	#Probably a simpler way of generating an array of strings
	z_vals = ['1', '2', '3', '4', '5', '6']
	for j in range(len(z_vals)):
		z_val = z_vals[j]
		class_path_lin = '/Users/penafiel/JPL/class/output/lin/lhs_lin_pk_%s' %trial
		class_path_nl = '/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_pk_%s' %trial
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
		k_lin *= h
		k_nl *= h
		
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
		ccl_path_lin = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_pk_%s' %trial
		ccl_path_nl = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_pk_%s' %trial
		ccl_path_lin += z_path
		ccl_path_nl += z_path
		np.savetxt(ccl_path_lin, np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')
		np.savetxt(ccl_path_nl, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')
    

		del pk_lin_list[:]
		del pk_nl_list[:]
		del pk_lin
		del pk_nl
