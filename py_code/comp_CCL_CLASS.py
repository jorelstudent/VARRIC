import numpy as np
import matplotlib.pyplot as plt
import pdb
import glob
from matplotlib import gridspec

#This program is to get each trial, and plot the differences for each thing
#While also trying to show the different parameter values
#Also plots the statistics, i.e. how precise our these calculations

#Call the original par_var file, so we can get the trial # easier in the long run, trust
# (Unless there's a more efficient way of calling files)

data = np.genfromtxt('/Users/penafiel/JPL/data/par_stan1.csv', dtype='str', skip_header=1)

#Gets the trial number into an arr
trial_arr = data[:,0]

#Iterates over the trial #
for i in range(len(trial_arr)):
	trial = data[i,0]
	print 'Performing trial %s' %trial

	z_vals = ['1', '2', '3', '4', '5', '6']
	for j in range(len(z_vals)):
		z_val = z_vals[j]
		z_path = 'z%s_pk.dat' %z_val
		z_nl_path = 'z%s_pk_nl.dat' %z_val
		print 'Performing z_val = ', z_val
		#For ease in iterating over different z values we use string manipulation (best manipulation)
		ccl_lin_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_%s' %trial
		ccl_nl_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_%s' %trial
		class_lin_path = '/Users/penafiel/JPL/class/output/lin/lhs_lin_%s' %trial
		class_nl_path = '/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_%s' %trial

		ccl_lin_path += z_path
		ccl_nl_path += z_path
		class_lin_path += z_path
		class_nl_path += z_nl_path


		#Call the CCL data
		ccl_lin_data = np.loadtxt(ccl_lin_path, skiprows=1)
		ccl_nl_data = np.loadtxt(ccl_nl_path, skiprows=1)
		#Call the CLASS lin data
		class_lin_data = np.loadtxt(class_lin_path, skiprows=4)

		#Call the CLASS nl data
		class_nl_data = np.loadtxt(class_nl_path, skiprows=4)

		k_lin = ccl_lin_data[:,0]
		k_nl = ccl_nl_data[:,0]
		ccl_lin = ccl_lin_data[:,1]
		ccl_nl = ccl_nl_data[:,1]

		class_k_lin = class_lin_data[:,0]
		class_lin = class_lin_data[:,1]
		class_k_nl = class_nl_data[:,0]
		class_nl = class_nl_data[:,1]

		#Multiply by factors
		#multiply k by some factor of h, CLASS and CCL use different units, ugh
		h = float(data[i,1])

		class_k_lin *= h
		class_lin /= h**3
		class_k_nl *= h
		class_nl /= h**3
		#For lin case
		#Get the error
		ccl_lin_err = (ccl_lin - class_lin) / class_lin

		#3 to 1 ratio between sizes of plots
		gs = gridspec.GridSpec(2,1, height_ratios=[3,1])

#		fig = plt.figure()
#		ax1 = plt.subplot(gs[0])#, rowspan = 2)
#		ax1.plot(k_lin, ccl_lin, 'r', label='CCL')
#		ax1.plot(class_k_lin ,class_lin, 'b', label='CLASS')
#		ax1.tick_params(labeltop=False, labelright=True)
#		plt.xscale('log')
#		plt.yscale('log')
#		plt.legend()
#		ax2 = plt.subplot(gs[1])
#		ax2.plot(k_lin, np.abs(ccl_lin_err))
#		plt.xscale('log')
#		plt.yscale('log')

		#String manipulation
#		plot_lin_path = '/Users/penafiel/JPL/plots/lhs_stats_lin_%s' %trial
#		z_save_path = '_z%s.png' %z_val
#		plot_lin_path += z_save_path
		
#		plt.savefig(plot_lin_path, format='png')

#		plt.clf()

		#For the nonlin case
		#Get the error
		ccl_nl_err = (ccl_nl - class_nl) / class_nl
#		
#		fig = plt.figure()
#		gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
#		ax1 = plt.subplot(gs[0])#, rowspan=2)
#		ax1.plot(k_nl, ccl_nl, 'r', label='CCL')
#		ax1.plot(class_k_nl , class_nl , 'b', label='CLASS')
#		plt.xscale('log')
#		plt.yscale('log')
#		plt.legend()
#		ax2 = plt.subplot(gs[1])
#		ax2.plot(k_nl, np.abs(ccl_nl_err))
#
#
#		plt.xscale('log')
#		plt.yscale('log')

		#String manipulation
#		plot_nl_path = '/Users/penafiel/JPL/plots/lhs_stats_nl_%s' %trial
#		plot_nl_path += z_save_path
#		plt.savefig(plot_nl_path, format='png')

		k_lin_list = k_lin.tolist()
		k_lin_list = ['k'] + k_lin_list

		ccl_lin_err_list = ccl_lin_err.tolist()
		ccl_lin_err_list = ['CCL lin error'] + ccl_lin_err_list

		k_nl_list = k_nl.tolist()
		k_nl_list = ['k'] + k_nl_list

		ccl_nl_err_list = ccl_nl_err.tolist()
		ccl_nl_err_list = ['CCL nl error'] + ccl_nl_err_list

		#more string manipulation
		err_lin_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_%s' %trial
		err_nl_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_%s' %trial

		z_stats_path = '_z%s.dat' %z_val
		err_lin_path += z_stats_path
		err_nl_path += z_stats_path
		#Saves a txt file with he k values and the errors
		np.savetxt(err_lin_path, np.transpose([k_lin_list, ccl_lin_err_list]), fmt='%-25s')
		np.savetxt(err_nl_path, np.transpose([k_nl_list, ccl_nl_err_list]), fmt='%-25s')
		#plt.clf()

#Do this for the precision files as well

#Iterates over the trial #
for i in range(len(trial_arr)):
	trial = data[i,0]
	print 'Performing trial %s' %trial

	z_vals = ['1', '2', '3', '4', '5', '6']
	for j in range(len(z_vals)):
		z_val = z_vals[j]
		z_path = 'z%s_pk.dat' %z_val
		z_nl_path = 'z%s_pk_nl.dat' %z_val
		print 'Performing z_val = ', z_val
		#For ease in iterating over different z values we use string manipulation (best manipulation)
		ccl_lin_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_lin_pk_%s' %trial
		ccl_nl_path = '/Users/penafiel/JPL/CCL-master/data_files/lhs_mpk_nl_pk_%s' %trial
		class_lin_path = '/Users/penafiel/JPL/class/output/lin/lhs_lin_pk_%s' %trial
		class_nl_path = '/Users/penafiel/JPL/class/output/nonlin/lhs_nonlin_pk_%s' %trial

		ccl_lin_path += z_path
		ccl_nl_path += z_path
		class_lin_path += z_path
		class_nl_path += z_nl_path


		#Call the CCL data
		ccl_lin_data = np.loadtxt(ccl_lin_path, skiprows=1)
		ccl_nl_data = np.loadtxt(ccl_nl_path, skiprows=1)
		#Call the CLASS lin data
		class_lin_data = np.loadtxt(class_lin_path, skiprows=4)

		#Call the CLASS nl data
		class_nl_data = np.loadtxt(class_nl_path, skiprows=4)

		k_lin = ccl_lin_data[:,0]
		k_nl = ccl_nl_data[:,0]
		ccl_lin = ccl_lin_data[:,1]
		ccl_nl = ccl_nl_data[:,1]

		class_k_lin = class_lin_data[:,0]
		class_lin = class_lin_data[:,1]
		class_k_nl = class_nl_data[:,0]
		class_nl = class_nl_data[:,1]

		#Multiply by factors
		#multiply k by some factor of h, CLASS and CCL use different units, ugh
		h = float(data[i,1])

		class_k_lin *= h
		class_lin /= h**3
		class_k_nl *= h
		class_nl /= h**3
		#For lin case
		#Get the error
		ccl_lin_err = (ccl_lin - class_lin) / class_lin

		#3 to 1 ratio between sizes of plots
		gs = gridspec.GridSpec(2,1, height_ratios=[3,1])

		fig = plt.figure()
		ax1 = plt.subplot(gs[0])#, rowspan = 2)
		ax1.plot(k_lin, ccl_lin, 'r', label='CCL')
		ax1.plot(class_k_lin ,class_lin, 'b', label='CLASS')
		ax1.tick_params(labeltop=False, labelright=True)
		plt.xscale('log')
		plt.yscale('log')
		plt.legend()
		ax2 = plt.subplot(gs[1])
		ax2.plot(k_lin, np.abs(ccl_lin_err))
		plt.xscale('log')
		plt.yscale('log')

		#String manipulation
		plot_lin_path = '/Users/penafiel/JPL/plots/lhs_stats_lin_pk_%s' %trial
		z_save_path = '_z%s.png' %z_val
		plot_lin_path += z_save_path
		
		plt.savefig(plot_lin_path, format='png')

		plt.clf()
		#For the nonlin case
		#Get the error
		ccl_nl_err = (ccl_nl - class_nl) / class_nl

#		fig = plt.figure()
#		gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
#		ax1 = plt.subplot(gs[0])#, rowspan=2)
#		ax1.plot(k_nl, ccl_nl, 'r', label='CCL')
#		ax1.plot(class_k_nl , class_nl , 'b', label='CLASS')
#		plt.xscale('log')
#		plt.yscale('log')
#		plt.legend()
#		ax2 = plt.subplot(gs[1])
#		ax2.plot(k_nl, np.abs(ccl_nl_err))


#		plt.xscale('log')
#		plt.yscale('log')

		#String manipulation
#		plot_nl_path = '/Users/penafiel/JPL/plots/lhs_stats_nl_pk_%s' %trial
#		plot_nl_path += z_save_path
#		plt.savefig(plot_nl_path, format='png')
		k_lin_list = k_lin.tolist()
		k_lin_list = ['k'] + k_lin_list

		ccl_lin_err_list = ccl_lin_err.tolist()
		ccl_lin_err_list = ['CCL lin error'] + ccl_lin_err_list

		k_nl_list = k_nl.tolist()
		k_nl_list = ['k'] + k_nl_list

		ccl_nl_err_list = ccl_nl_err.tolist()
		ccl_nl_err_list = ['CCL nl error'] + ccl_nl_err_list

		#more string manipulation
		err_lin_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_lin_pk_%s' %trial
		err_nl_path = '/Users/penafiel/JPL/stats/lhs_mpk_err_nl_pk_%s' %trial

		z_stats_path = '_z%s.dat' %z_val
		err_lin_path += z_stats_path
		err_nl_path += z_stats_path
		#Saves a txt file with he k values and the errors
		np.savetxt(err_lin_path, np.transpose([k_lin_list, ccl_lin_err_list]), fmt='%-25s')
		np.savetxt(err_nl_path, np.transpose([k_nl_list, ccl_nl_err_list]), fmt='%-25s')
		#plt.clf()
