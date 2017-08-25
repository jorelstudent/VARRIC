import numpy as np
import pyccl as ccl
import glob
import matplotlib.pyplot as plt
import pdb

#We are going to get the numbers generated from the gen_par.py file for CLASS
#They are the same variables, so all we need to do is rename them to the proper name

#Cal the files as string, make the rest floats later
data = np.genfromtxt('/Users/penafiel/JPL/data/par_wcdm.txt', dtype='str', skip_header=1)

#This gets the trial number into an arr
trial_arr = data[:,0]
h_arr = data[:,1]
omega_b_arr = data[:,2]
omega_cdm_arr = data[:,3]
A_s_arr = data[:,4]
n_s_arr = data[:,5]
Omega_k_arr = data[:,6]
w0_arr = data[:,7]
wa_arr = data[:,8]

#Perform the calculation for each set of parameters
#We will store both the linear and nonlinear cases

#Initialize variables that won't change

#k = np.logspace(-5., 1., 100) #Wavenumber

#k_list = k.tolist()
#k_list = ['k'] + k_list
#pdb.set_trace()
for i in range(len(trial_arr)):
    trial = trial_arr[i]
    #if (trial != '00080'): #| (trial == '00008') |(trial == '00009'):
    #    continue
    print 'Performing trial %s' %trial
    h = float(h_arr[i])
    omega_b = float(omega_b_arr[i]) #/ h**2
    omega_cdm = float(omega_cdm_arr[i]) #/ h**2
    A_s = float(A_s_arr[i])
    n_s = float(n_s_arr[i])
    Omega_k = float(Omega_k_arr[i])
    w0 = float(w0_arr[i])
    wa = float(wa_arr[i])
    print 'getting cosmology'
    cosmo = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s,Omega_k=Omega_k, w0=w0, wa=wa, transfer_function='boltzmann')
    #Get the k values, directly from CLASS
    #Has to be a simpler way of automating this
    #The 'simple' way I believe is to make a strings of the paths and just concatenate them
    #depending on which z values we're looking at
    #Probably a simpler way of generating an array of strings
    z_vals = ['1', '2', '3', '4', '5', '6']
    for j in range(len(z_vals)):
        z_val = z_vals[j]
        if z_val=='1':
            continue
        class_path_lin = '/Users/penafiel/JPL/class/output/wcdm/lin/lhs_lin_%s' %trial
        #class_path_nl = '/Users/penafiel/JPL/class/output/wcdm/nonlin/lhs_nonlin_%s' %trial
        #iterating over the z_vals
        #Then concatenating our string files
        z_path = 'z%s_pk.dat' %z_val
        #z_nl_path = 'z%s_pk_nl.dat' %z_val
        class_path_lin += z_path
        #class_path_nl += z_nl_path

        k_lin_data = np.loadtxt(class_path_lin, skiprows=4)
        #k_nl_data = np.loadtxt(class_path_nl, skiprows=4)
        k_lin = k_lin_data[:,0]
        #k_nl = k_nl_data[:,0]
        k_lin *= h
        #k_nl *= h
        
        #Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
        z = j * 0.5
        
        print 'Check z = %d' %z
        a = 1. / (1. + z)
        #Matter power spectrum for lin and nonlin

        pk_lin = ccl.linear_matter_power(cosmo, k_lin, a)
        print 'Check for linear'
        #pk_nl = ccl.nonlin_matter_power(cosmo, k_nl, a)
        #print 'Check for nl'
        #Transform these into lists and add header lines
        k_lin_list = k_lin.tolist()
        k_lin_list = ['k'] + k_lin_list

        #k_nl_list = k_nl.tolist()
        #k_nl_list = ['z=%d k' %z] + k_nl_list
        pk_lin_list = pk_lin.tolist()
        #pk_nl_list = pk_nl.tolist()
        pk_lin_list =['pk_lin'] + pk_lin_list
        #pk_nl_list = ['pk_nl'] + pk_nl_list
        ccl_path_lin = '/Users/penafiel/JPL/CCL-master/data_files/wcdm/lhs_mpk_lin_%s' %trial
        #ccl_path_nl = '/Users/penafiel/JPL/CCL-master/data_files/wcdm/lhs_mpk_nl_%s' %trial
        ccl_path_lin += z_path
        #ccl_path_nl += z_path
        np.savetxt(ccl_path_lin, np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')
        #np.savetxt(ccl_path_nl, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')
   
        del k_lin_data
        #del k_nl_data
        del k_lin_list[:]
        #del k_nl_list[:]
        del k_lin
        #del k_nl
        del pk_lin_list[:]
        #del pk_nl_list[:]
        del pk_lin
        #del pk_nl
    del cosmo



"""
#Do this for the precision values

for i in range(len(trial_arr)):
    print 'doing precision'
    trial = trial_arr[i]
    #if (trial == '00008') | (trial =='00009'):
    #    continue
    print 'Performing trial %s' %trial
    h = float(h_arr[i])
    omega_b = float(omega_b_arr[i]) #/ h**2
    omega_cdm = float(omega_cdm_arr[i]) #/ h**2
    A_s = float(A_s_arr[i])
    n_s = float(n_s_arr[i])
    Omega_k = float(Omega_k_arr[i])
    w0 = float(w0_arr[i])
    wa = float(wa_arr[i])
    cosmo = ccl.Cosmology(Omega_c=omega_cdm, Omega_b=omega_b, h=h, A_s=A_s, n_s=n_s, Omega_k=Omega_k, w0=w0, wa=wa, transfer_function='boltzmann')
    #Get the k values, directly from CLASS
    #Has to be a simpler way of automating this
    #The 'simple' way I believe is to make a strings of the paths and just concatenate them
    #depending on which z values we're looking at
    #Probably a simpler way of generating an array of strings
    z_vals = ['1', '2', '3', '4', '5', '6']
    for j in range(len(z_vals)):
        z_val = z_vals[j]
        class_path_lin = '/Users/penafiel/JPL/class/output/wcdm/lin/lhs_lin_pk_%s' %trial
        class_path_nl = '/Users/penafiel/JPL/class/output/wcdm/nonlin/lhs_nonlin_pk_%s' %trial
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
        ccl_path_lin = '/Users/penafiel/JPL/CCL-master/data_files/wcdm/lhs_mpk_lin_pk_%s' %trial
        ccl_path_nl = '/Users/penafiel/JPL/CCL-master/data_files/wcdm/lhs_mpk_nl_pk_%s' %trial
        ccl_path_lin += z_path
        ccl_path_nl += z_path
        np.savetxt(ccl_path_lin, np.transpose([k_lin_list, pk_lin_list]), fmt='%-25s')
        np.savetxt(ccl_path_nl, np.transpose([k_nl_list, pk_nl_list]), fmt='%-25s')
    

        del pk_lin_list[:]
        del pk_nl_list[:]
        del pk_lin
        del pk_nl
"""
