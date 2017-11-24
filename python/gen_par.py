import numpy as np
import numpy.random as npr
import pdb

#Define a function that gives an output of 00000,00001, ...., xxxxx
#Where xxxx is an arbitrary 5-digit number

def num_trials(n_trials):
    n_trials_arr = []
    for i in range(n_trials):
        num = '{0:05}'.format(i)
        num = str(num)
        n_trials_arr.append(num)

    return np.asarray(n_trials_arr)

def gen_par(n_trials):
    #Initialize all the variables that we are going to vary
    #These are the default values

    #Hubble Constant, present day
    h_def = 0.67556
    omega_b_def = 0.022032
    omega_cdm_def = 0.12038
    A_s_def = 2.215e-9
    n_s_def = 0.9619
    #root_def = output/trial_00000_

    num_trials_arr= num_trials(n_trials)

    #Randomly generate numbers for the parameters
    i = 0
    h_arr = []
    omega_b_arr = []
    omega_cdm_arr = []
    A_s_arr = []
    n_s_arr = []

    for i in range(len(num_trials_arr)):
        h_var = str(npr.uniform(0.9 * h_def, 1.1 * h_def))
        h_arr.append(h_var)
        omega_b_var = str(npr.uniform(0.9 * omega_b_def, 1.1 * omega_b_def))
        omega_b_arr.append(omega_b_var)
        omega_cdm_var = str(npr.uniform(0.9 * omega_cdm_def, 1.1 * omega_cdm_def))
        omega_cdm_arr.append(omega_cdm_var)
        A_s_var = str(npr.uniform(0.9 * A_s_def, 1.1 * A_s_def))
        A_s_arr.append(A_s_var)
        n_s_var = str(npr.uniform(0.9 * n_s_def, 1.1 * n_s_def))
        n_s_arr.append(n_s_var)

    h_arr = ['h values'] + h_arr
    omega_b_arr = ['omega_b values'] + omega_b_arr
    omega_cdm_arr = ['omega_cdm values'] + omega_cdm_arr
    A_s_arr = ['A_s values'] + A_s_arr
    n_s_arr = ['n_s values'] + n_s_arr
    num_trials_arr = num_trials_arr.tolist()
    num_trials_arr = ['Trial'] + num_trials_arr

    np.savetxt('par_var.txt', np.transpose([num_trials_arr, h_arr, omega_b_arr, omega_cdm_arr, A_s_arr, n_s_arr]), fmt='%-20s')

if __name__ == "__main__":
    n_trials = 100
    gen_par(100)
    pdb.set_trace()
# Create a for loop for some n amount of trials, to create a .ini files

#for i in n_trials_arr:
#    ini = open(trial%s.ini % i, 'w')
#    

