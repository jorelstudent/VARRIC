import numpy as np
import numpy.random as npr
import pdb
import itertools
import random

#This Python script aims to generate parameter values UTILIZING Latin hypercubes
#Latin hypercube sampling is a constrained sampling scheme, which in theory should
#	yield more precise estimates compared to Monte Carlo sampling
#A simple case is the Latin square. It is a Latin square if there exists only one point in each row, column
#	based on the binning (i.e. number of samples)
#Might make a jupyter notebook to make it more easily seen, since that has pictures

#LEARN FROM MY MISTAKES

#To generate columns with different values in each row
#Fuck itertools.permutations, since it gives you all possible permutations, goes to shit even at n = 10
#	Not computationally efficient
#Fuck trying to generate it yourself, not even 30 000 tries will help you there, dont even try to shuffle them
#Fuck trying to Sudoku this thing, I don't even know where I was going with that one
#Create cyclic permutations of a given range of numbers
#Randomly choose these cyclic permutations, then you're good to go
#Fuck trying to do cyclic permutations shit, you can use a diagoanal hypercube 

#THIS IS HOW YOU DO IT

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
def lhs_par_stan(n_trials):

	N_trials = n_trials
	Ndim = 5 #This is for the standard one

	#Create a list for you to append with bin values
	h_bin_list = []
	Omega_b_bin_list = []
	Omega_cdm_bin_list = []
	A_s_bin_list = []
	n_s_bin_list = []

	#Generate a list of Ndim
	l = [range(N_trials) for j in range(5)] #5 dimensions
	while len(l[0]) != 0:
		h = random.choice(l[0])
		Omega_b = random.choice(l[1])
		Omega_cdm = random.choice(l[2])
		A_s = random.choice(l[3])
		n_s = random.choice(l[4])

		h_bin_list.append(h)
		Omega_b_bin_list.append(Omega_b)
		Omega_cdm_bin_list.append(Omega_cdm)
		A_s_bin_list.append(A_s)
		n_s_bin_list.append(n_s)

		#Removes the numbers that were already chosen, since Latin hypercubes want one item per row and column
		#e.g. for a 2x5, we don't want two items in the same row or same column
		l[0].remove(h)
		l[1].remove(Omega_b)
		l[2].remove(Omega_cdm)
		l[3].remove(A_s)
		l[4].remove(n_s)

	#Now we have the bin lists
	#We now find the width of each bin using the range of our values
	h_w = (0.9 - 0.5) / N_trials
	Omega_cdm_w = (0.4 - 0.1) / N_trials
	Omega_b_w = (0.052 - 0.018) / N_trials
	A_s_w = (2.5e-9 - 1.5e-9) / N_trials
	n_s_w = (0.99 - 0.93) / N_trials

	#Now we take the center value from these bins
	#We first turn these into arrays
	h_bin_arr = np.asarray(h_bin_list)
	Omega_b_bin_arr = np.asarray(Omega_b_bin_list)
	Omega_cdm_bin_arr = np.asarray(Omega_cdm_bin_list)
	A_s_bin_arr = np.asarray(A_s_bin_list)
	n_s_bin_arr = np.asarray(n_s_bin_list)

	#We then get the center values, don't forget to add by the min value
	h_val = ((h_bin_arr + 0.5) * h_w) + 0.5
	Omega_b_val = (((Omega_b_bin_arr + 0.5) * Omega_b_w) + 0.018)# * h_val ** 2
	Omega_cdm_val = (((Omega_cdm_bin_arr + 0.5) * Omega_cdm_w) + 0.1)# * h_val**2
	A_s_val = ((A_s_bin_arr + 0.5) * A_s_w) + 1.5e-9
	n_s_val = ((n_s_bin_arr + 0.5) * n_s_w) + 0.93

	#Put these back to list so we can add some headers, This can be removed in the future
	h_val_list = h_val.tolist()
	Omega_b_val_list = Omega_b_val.tolist()
	Omega_cdm_val_list = Omega_cdm_val.tolist()
	A_s_val_list = A_s_val.tolist()
	n_s_val_list = n_s_val.tolist()

	h_val_list = ['h'] + h_val_list
	Omega_b_val_list = ['Omega_b'] + Omega_b_val_list
	Omega_cdm_val_list = ['Omega_cdm'] + Omega_cdm_val_list
	A_s_val_list = ['A_s'] + A_s_val_list
	n_s_val_list = ['n_s'] + n_s_val_list

	num_trials_arr = num_trials(n_trials)
	num_trials_list = num_trials_arr.tolist()
	num_trials_list = ['Trial #'] + num_trials_list
	np.savetxt('/Users/penafiel/JPL/data/par_stan1.csv', np.transpose([num_trials_list, h_val_list, Omega_b_val_list, Omega_cdm_val_list, A_s_val_list, n_s_val_list]), fmt='%-20s')

	return h_val_list, Omega_b_val_list, Omega_cdm_val_list, A_s_val_list, n_s_val_list


#Let's do the same for standard parameters + extensions
#Basically the same thing with added variables
#Could make this less lines if I called lhs_par_stan, Fuck it why not

def lhs_par_wcdm(n_trials):
	N_trials = n_trials

	Ndim = 8 #This is for the standard one

	#Create a list for you to append with bin values
	h_bin_list = []
	Omega_b_bin_list = []
	Omega_cdm_bin_list = []
	A_s_bin_list = []
	n_s_bin_list = []

	Omega_k_bin_list = []
	#M_nu_bin_list = []
	w_0_bin_list = []
	w_a_bin_list = []

	#Generate a list of Ndim
	l = [range(N_trials) for j in range(Ndim)] #8 dimensions
	#Latin hypercube sampling
	while len(l[0]) != 0:
		h = random.choice(l[0])
		Omega_b = random.choice(l[1])
		Omega_cdm = random.choice(l[2])
		A_s = random.choice(l[3])
		n_s = random.choice(l[4])

		
		Omega_k = random.choice(l[5])
		#M_nu = random.choice(l[])
		w_0 = random.choice(l[6])
		w_a = random.choice(l[7])
		
		h_bin_list.append(h)
		Omega_b_bin_list.append(Omega_b)
		Omega_cdm_bin_list.append(Omega_cdm)
		A_s_bin_list.append(A_s)
		n_s_bin_list.append(n_s)

		Omega_k_bin_list.append(Omega_k)
		#M_nu_bin_list.append(M_nu)
		w_0_bin_list.append(w_0)
		w_a_bin_list.append(w_a)


		#Removes the numbers that were already chosen, since Latin hypercubes want one item per row and column
		#e.g. for a 2x5, we don't want two items in the same row or same column

		l[0].remove(h)
		l[1].remove(Omega_b)
		l[2].remove(Omega_cdm)
		l[3].remove(A_s)
		l[4].remove(n_s)

		l[5].remove(Omega_k)
		#l[1].remove(M_nu)
		l[6].remove(w_0)
		l[7].remove(w_a)

	#Now we have the bin lists
	#We now find the width of each bin using the range of our values
	h_w = (0.9 - 0.5) / N_trials
	Omega_cdm_w = (0.4 - 0.1) / N_trials
	Omega_b_w = (0.05 - 0.02) / N_trials
	A_s_w = (2.5e-9 - 1.5e-9) / N_trials
	n_s_w = (0.99 - 0.93) / N_trials

	Omega_k_w = (0.05 - (-0.04)) / N_trials
	#M_nu_w = (1.0 - 0.06) / N_trials
	w_0_w = (-0.5 - (-2.)) / N_trials
	w_a_w = (0.1 - (-0.1)) / N_trials

	#Now we take the center value from these bins
	#We first turn these into arrays
	h_bin_arr = np.asarray(h_bin_list)
	Omega_b_bin_arr = np.asarray(Omega_b_bin_list)
	Omega_cdm_bin_arr = np.asarray(Omega_cdm_bin_list)
	A_s_bin_arr = np.asarray(A_s_bin_list)
	n_s_bin_arr = np.asarray(n_s_bin_list)

	Omega_k_bin_arr = np.asarray(Omega_k_bin_list)
	#M_nu_bin_arr = np.asarray(M_nu_bin_list)
	w_0_bin_arr = np.asarray(w_0_bin_list)
	w_a_bin_arr = np.asarray(w_a_bin_list)

	#We then get the center values, don't forget to add by the min value
	h_val = ((h_bin_arr + 0.5) * h_w) + 0.5
	Omega_b_val = (((Omega_b_bin_arr + 0.5) * Omega_b_w) + 0.02)# * h_val ** 2
	Omega_cdm_val = (((Omega_cdm_bin_arr + 0.5) * Omega_cdm_w) + 0.1)# * h_val**2
	A_s_val = ((A_s_bin_arr + 0.5) * A_s_w) + 1.5e-9
	n_s_val = ((n_s_bin_arr + 0.5) * n_s_w) + 0.93

	Omega_k_val = ((Omega_k_bin_arr + 0.5) * Omega_k_w) + (-0.04)
	#M_nu_val = ((M_nu_bin_arr + 0.5) * M_nu_w) + 0.06
	w_0_val = ((w_0_bin_arr + 0.5) * w_0_w) + (-2.)
	w_a_val = ((w_a_bin_arr + 0.5) * w_a_w) + (-0.1)

	#Put these back to list so we can add some headers, This can be removed in the future
	h_val_list = h_val.tolist()
	Omega_b_val_list = Omega_b_val.tolist()
	Omega_cdm_val_list = Omega_cdm_val.tolist()
	A_s_val_list = A_s_val.tolist()
	n_s_val_list = n_s_val.tolist()

	Omega_k_val_list = Omega_k_val.tolist()
	#M_nu_val_list = M_nu_val.tolist()
	w_0_val_list = w_0_val.tolist()
	w_a_val_list = w_a_val.tolist()

	#Add the titles
	h_val_list = ['h'] + h_val_list
	Omega_b_val_list = ['Omega_b'] + Omega_b_val_list
	Omega_cdm_val_list = ['Omega_cdm'] + Omega_cdm_val_list
	A_s_val_list = ['A_s'] + A_s_val_list
	n_s_val_list = ['n_s'] + n_s_val_list

	Omega_k_val_list = ['Omega_k'] + Omega_k_val_list
	#M_nu_val_list = ['M_nu'] + M_nu_val_list
	w_0_val_list = ['w_0'] + w_0_val_list
	w_a_val_list = ['w_a'] + w_a_val_list


	num_trials_arr = num_trials(n_trials)
	num_trials_list = num_trials_arr.tolist()
	num_trials_list = ['Trial #'] + num_trials_list
	np.savetxt('/Users/penafiel/JPL/data/par_wcdm.txt', np.transpose([num_trials_list, h_val_list, Omega_b_val_list, Omega_cdm_val_list,
				A_s_val_list, n_s_val_list, Omega_k_val_list, w_0_val_list, w_a_val_list]), fmt='%-20s')
		
		
#Running the code
if __name__ == "__main__":
	n_trials = 100
	lhs_par_wcdm(n_trials)
	#lhs_par_ext(n_trials)


#pdb.set_trace()
