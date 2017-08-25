from flask import Flask, render_template, request
import pandas as pd
from bokeh.embed import components

from bokeh.palettes import Spectral6
from bokeh.layouts import column, widgetbox, WidgetBox, layout
from bokeh.models import CustomJS, Button, HoverTool, ColumnDataSource, LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, OpenURL, TapTool#For the button and a hovertool
from bokeh.models.widgets import Paragraph, PreText, CheckboxGroup, Slider, Dropdown, Select, RangeSlider #For the sliders and dropdown
from bokeh.plotting import figure, curdoc, show
from bokeh.io import gridplot, output_file, show #allows you to make gridplots
from bokeh.charts import HeatMap, bins, output_file, show #Allows you to craete heatmaps
from bokeh.models import Rect

import numpy as np
import pdb
from random import random

app = Flask(__name__)
#creates hover tool
indices = range(100)


#LETS IMPLEMENT A CLICK
@app.route('/')
def home():
    #load the data
    data = np.loadtxt('../data/par_stan1.csv', skiprows=1)

    #Load the parameter values and total failures, since it will be easier to load
    trial_arr = data[:,0]
    h_arr = data[:,1]
    Omega_b_arr = data[:,2]
    Omega_cdm_arr = data[:,3]
    A_s_arr = data[:,4]
    n_s_arr = data[:,5]
    #Gets the extension depending on which mode you choose
    #tot_tot_lin = tot_tot[:,0]
    #tot_tot_nl = tot_tot[:,1]
    #tot_tot_lin_pre = tot_tot[:,2]
    #tot_tot_nl_pre = tot_tot[:,3]

    ####################################################
    #CALCULATE THE VALUES FOR HOW BADLY SOMETHING FAILS#
    ####################################################

    #Also the number for failures can either include clustering regime only or not
    thres_val = [5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2] #Threshold for the failures
    thres = 1.e-4 #Threshold for number of failures
    clustering_only = False #Only counts failures if inside the clustering regime

    ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
    ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
    lin_scale_min = 1e-2 #Min for the linear scales
    lin_scale_max = 1e-1 #Max for the linear scales
    quasi_scale_min = 1e-1 #Min for the quasi-lin scales
    quasi_scale_max = 1.0 #Max for the quasi-lin scales


    cluster_reg_min = 1e-2 #Min for the cluster regime
    cluster_reg_max = 0.2 # Max for the cluster regime


    #Create arrays that will be filled in the loop over trials
    #Total of the wights
    tot_tot_lin = []
    tot_tot_nl = []
    tot_tot_lin_pre = []
    tot_tot_nl_pre = []

    #Get the totals for the different thresholds
    #For now, we'll denote it as 1,2,3,4,5,6
    #1 = 5e-5
    #2 = 1e-4
    #3 = 5e-4
    #4 = 1e-3
    #5 = 5e-3
    #6 = 1e-2

    #Get the totals for different k_ranges
    #We have 3 k_ranges, denote by 1,2,3
    #1 = Ultra Large Scales
    #2 = Linear scales
    #3 = Nonlinear scales

    #But we have to do this for different z_values as well
    #Probably a more efficient way of writing this, but I think this will suffice
    tot_lin_k1_z1_ll = []
    tot_lin_k2_z1_ll = []
    tot_lin_k3_z1_ll = []
    
    tot_lin_k1_z2_ll = []
    tot_lin_k2_z2_ll = []
    tot_lin_k3_z2_ll = []
    
    tot_lin_k1_z3_ll = []
    tot_lin_k2_z3_ll = []
    tot_lin_k3_z3_ll = []
    
    tot_lin_k1_z4_ll = []
    tot_lin_k2_z4_ll = []
    tot_lin_k3_z4_ll = []
    
    tot_lin_k1_z5_ll = []
    tot_lin_k2_z5_ll = []
    tot_lin_k3_z5_ll = []
    
    tot_lin_k1_z6_ll = []
    tot_lin_k2_z6_ll = []
    tot_lin_k3_z6_ll = []
    
    tot_nl_k1_z1_ll = []
    tot_nl_k2_z1_ll = []
    tot_nl_k3_z1_ll = []

    tot_nl_k1_z2_ll = []
    tot_nl_k2_z2_ll = []
    tot_nl_k3_z2_ll = []

    tot_nl_k1_z3_ll = []
    tot_nl_k2_z3_ll = []
    tot_nl_k3_z3_ll = []

    tot_nl_k1_z4_ll = []
    tot_nl_k2_z4_ll = []
    tot_nl_k3_z4_ll = []

    tot_nl_k1_z5_ll = []
    tot_nl_k2_z5_ll = []
    tot_nl_k3_z5_ll = []

    tot_nl_k1_z6_ll = []
    tot_nl_k2_z6_ll = []
    tot_nl_k3_z6_ll = []

    tot_lin_pre_k1_z1_ll = []
    tot_lin_pre_k2_z1_ll = []
    tot_lin_pre_k3_z1_ll = []

    tot_lin_pre_k1_z2_ll = []
    tot_lin_pre_k2_z2_ll = []
    tot_lin_pre_k3_z2_ll = []

    tot_lin_pre_k1_z3_ll = []
    tot_lin_pre_k2_z3_ll = []
    tot_lin_pre_k3_z3_ll = []

    tot_lin_pre_k1_z4_ll = []
    tot_lin_pre_k2_z4_ll = []
    tot_lin_pre_k3_z4_ll = []

    tot_lin_pre_k1_z5_ll = []
    tot_lin_pre_k2_z5_ll = []
    tot_lin_pre_k3_z5_ll = []

    tot_lin_pre_k1_z6_ll = []
    tot_lin_pre_k2_z6_ll = []
    tot_lin_pre_k3_z6_ll = []

    tot_nl_pre_k1_z1_ll = []
    tot_nl_pre_k2_z1_ll = []
    tot_nl_pre_k3_z1_ll = []

    tot_nl_pre_k1_z2_ll = []
    tot_nl_pre_k2_z2_ll = []
    tot_nl_pre_k3_z2_ll = []

    tot_nl_pre_k1_z3_ll = []
    tot_nl_pre_k2_z3_ll = []
    tot_nl_pre_k3_z3_ll = []

    tot_nl_pre_k1_z4_ll = []
    tot_nl_pre_k2_z4_ll = []
    tot_nl_pre_k3_z4_ll = []

    tot_nl_pre_k1_z5_ll = []
    tot_nl_pre_k2_z5_ll = []
    tot_nl_pre_k3_z5_ll = []

    tot_nl_pre_k1_z6_ll = []
    tot_nl_pre_k2_z6_ll = []
    tot_nl_pre_k3_z6_ll = []

    #Iterate over different threshold values
    for m in thres_val:
        thres = m

        tot_lin_k1_z1 = []
        tot_lin_k2_z1 = []
        tot_lin_k3_z1 = []
    
        tot_lin_k1_z2 = []
        tot_lin_k2_z2 = []
        tot_lin_k3_z2 = []
    
        tot_lin_k1_z3 = []
        tot_lin_k2_z3 = []
        tot_lin_k3_z3 = []
    
        tot_lin_k1_z4 = []
        tot_lin_k2_z4 = []
        tot_lin_k3_z4 = []
    
        tot_lin_k1_z5 = []
        tot_lin_k2_z5 = []
        tot_lin_k3_z5 = []
    
        tot_lin_k1_z6 = []
        tot_lin_k2_z6 = []
        tot_lin_k3_z6 = []
    
        tot_nl_k1_z1 = []
        tot_nl_k2_z1 = []
        tot_nl_k3_z1 = []

        tot_nl_k1_z2 = []
        tot_nl_k2_z2 = []
        tot_nl_k3_z2 = []
    
        tot_nl_k1_z3 = []
        tot_nl_k2_z3 = []
        tot_nl_k3_z3 = []

        tot_nl_k1_z4 = []
        tot_nl_k2_z4 = []
        tot_nl_k3_z4 = []

        tot_nl_k1_z5 = []
        tot_nl_k2_z5 = []
        tot_nl_k3_z5 = []

        tot_nl_k1_z6 = []
        tot_nl_k2_z6 = []
        tot_nl_k3_z6 = []

        tot_lin_pre_k1_z1 = []
        tot_lin_pre_k2_z1 = []
        tot_lin_pre_k3_z1 = []
    
        tot_lin_pre_k1_z2 = []
        tot_lin_pre_k2_z2 = []
        tot_lin_pre_k3_z2 = []

        tot_lin_pre_k1_z3 = []
        tot_lin_pre_k2_z3 = []
        tot_lin_pre_k3_z3 = []

        tot_lin_pre_k1_z4 = []
        tot_lin_pre_k2_z4 = []
        tot_lin_pre_k3_z4 = []

        tot_lin_pre_k1_z5 = []
        tot_lin_pre_k2_z5 = []
        tot_lin_pre_k3_z5 = []

        tot_lin_pre_k1_z6 = []
        tot_lin_pre_k2_z6 = []
        tot_lin_pre_k3_z6 = []

        tot_nl_pre_k1_z1 = []
        tot_nl_pre_k2_z1 = []
        tot_nl_pre_k3_z1 = []

        tot_nl_pre_k1_z2 = []
        tot_nl_pre_k2_z2 = []
        tot_nl_pre_k3_z2 = []

        tot_nl_pre_k1_z3 = []
        tot_nl_pre_k2_z3 = []
        tot_nl_pre_k3_z3 = []

        tot_nl_pre_k1_z4 = []
        tot_nl_pre_k2_z4 = []
        tot_nl_pre_k3_z4 = []

        tot_nl_pre_k1_z5 = []
        tot_nl_pre_k2_z5 = []
        tot_nl_pre_k3_z5 = []

        tot_nl_pre_k1_z6 = []
        tot_nl_pre_k2_z6 = []
        tot_nl_pre_k3_z6 = []

        ###########################
        #                         #
        #GETTING THE SUMMARY STATS#
        #                         #
        ###########################
        for i in range(len(trial_arr)):
            trial = data[i,0]
            print 'Performing trial %05d' %trial

            z_vals = ['1', '2', '3', '4', '5', '6']

            #Gonna generate an array of arrays, with each row corresponding to a different z value
            #Each columns will correspond to a different bins of k_values
            tot_lin = []

            #For list of lists
            tot_lin_ll = []
    
            for j in range(len(z_vals)):
                z_val = z_vals[j]
                z_path ='_z%s.dat' %z_val
                print 'Performing z_val = ', z_val
        
                #For ease in iterating over different z values we use string manipulation
                stats_lin_path = '../stats/lhs_mpk_err_lin_%05d' %trial

                #Adds the z_path
                stats_lin_path += z_path

                #Calls the data 
                stats_lin_data = np.loadtxt(stats_lin_path, skiprows=1)

                stats_lin_k = stats_lin_data[:,0]
                stats_lin_err = stats_lin_data[:,1]

                #Create arrays that will be used to fill the complete summary arrays
                tot_lin_z = []

                #For list of lists
                tot_lin_z_ll = []

                #We perform a loop that looks into the bins for k
                #Doing this for lin
                #Much easier than doing a for loop because of list comprehension ALSO FASTER
                tot_ultrasc = 0 #initialize value for ultra large scales
                tot_linsc = 0 #initialize for lin scales
                tot_quasisc = 0 #initialize for quasi lin scales

                #k has to fall in the proper bins
                aux_k_ultra = (stats_lin_k >= ultra_scale_min) & (stats_lin_k < ultra_scale_max)
                aux_k_lin = (stats_lin_k >= lin_scale_min) & (stats_lin_k < lin_scale_max)
                aux_k_quasi = (stats_lin_k >= quasi_scale_min) & (stats_lin_k <= quasi_scale_max)

                #Looks at only the regime where clustering affects it
                if clustering_only == True:
                    aux_cluster_ultra = (stats_lin_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_k[aux_k_ultra] < cluster_reg_max)
                    aux_cluster_lin = (stats_lin_k[aux_k_lin] > cluster_reg_min) & (stats_lin_k[aux_k_lin] < cluster_reg_max)
                    aux_cluster_quasi = (stats_lin_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_k[aux_k_quasi] < cluster_reg_max)
            
                   #Calculate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs((stats_lin_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
                    w_lin = np.log10(np.abs((stats_lin_err[aux_k_lin])[aux_cluster_lin]) / thres)
                    w_quasi = np.log10(np.abs((stats_lin_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.

                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0

                    tot_ultrasc = np.sum(w_ultra)
                    tot_linsc = np.sum(w_lin)
                    tot_quasisc = np.sum(w_quasi)
                #calculates imprecision in any regime
                if clustering_only == False:
                    #caluclate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs(stats_lin_err[aux_k_ultra]) / thres)
                    w_lin = np.log10(np.abs(stats_lin_err[aux_k_lin]) / thres)
                    w_quasi = np.log10(np.abs(stats_lin_err[aux_k_quasi]) / thres)
    
                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.

                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0

                    #calculate the totals
                    tot_ultrasc = np.sum(w_ultra)
                    tot_linsc = np.sum(w_lin)
                    tot_quasisc = np.sum(w_quasi)
        
        
                #Append these values to our z summary stat
                #For list only
                tot_lin_z = np.append(tot_lin_z, tot_ultrasc)
                tot_lin_z = np.append(tot_lin_z, tot_linsc)
                tot_lin_z = np.append(tot_lin_z, tot_quasisc)

                #For list of lists
                tot_lin_z_ll.append(tot_ultrasc)
                tot_lin_z_ll.append(tot_linsc)
                tot_lin_z_ll.append(tot_quasisc)

                #Append these values for the general z stat
                #For list only
                tot_lin = np.append(tot_lin, tot_lin_z)
                #For list of lists
                tot_lin_ll.append(tot_lin_z_ll)

            #Appending the values for the k ranges
            tot_lin_k1_z1 = np.append(tot_lin_k1_z1, tot_lin_ll[0][0])
            tot_lin_k2_z1 = np.append(tot_lin_k2_z1, tot_lin_ll[0][1])
            tot_lin_k3_z1 = np.append(tot_lin_k3_z1, tot_lin_ll[0][2])

            tot_lin_k1_z2 = np.append(tot_lin_k1_z2, tot_lin_ll[1][0])
            tot_lin_k2_z2 = np.append(tot_lin_k2_z2, tot_lin_ll[1][1])
            tot_lin_k3_z2 = np.append(tot_lin_k3_z2, tot_lin_ll[1][2])

            tot_lin_k1_z3 = np.append(tot_lin_k1_z3, tot_lin_ll[2][0])
            tot_lin_k2_z3 = np.append(tot_lin_k2_z3, tot_lin_ll[2][1])
            tot_lin_k3_z3 = np.append(tot_lin_k3_z3, tot_lin_ll[2][2])

            tot_lin_k1_z4 = np.append(tot_lin_k1_z4, tot_lin_ll[3][0])
            tot_lin_k2_z4 = np.append(tot_lin_k2_z4, tot_lin_ll[3][1])
            tot_lin_k3_z4 = np.append(tot_lin_k3_z4, tot_lin_ll[3][2])

            tot_lin_k1_z5 = np.append(tot_lin_k1_z5, tot_lin_ll[4][0])
            tot_lin_k2_z5 = np.append(tot_lin_k2_z5, tot_lin_ll[4][1])
            tot_lin_k3_z5 = np.append(tot_lin_k3_z5, tot_lin_ll[4][2])

            tot_lin_k1_z6 = np.append(tot_lin_k1_z6, tot_lin_ll[5][0])
            tot_lin_k2_z6 = np.append(tot_lin_k2_z6, tot_lin_ll[5][1])
            tot_lin_k3_z6 = np.append(tot_lin_k3_z6, tot_lin_ll[5][2])

            tot_tot_lin = np.append(tot_tot_lin, np.sum(tot_lin))

            print 'Performing this for nonlin'
            #Gonna generate an array of arrays, with each row corresponding to a different z value
            #Each columns will correspond to a different bins of k_values
            tot_nl = []

            #For list of lists
            tot_nl_ll = []

            for j in range(len(z_vals)):
                z_val = z_vals[j]
                z_path ='_z%s.dat' %z_val
                print 'Performing z_val = ', z_val
        
                #For ease in iterating over different z values we use string manipulation
                stats_nl_path = '../stats/lhs_mpk_err_nl_%05d' %trial

                #Adds the z_path
                stats_nl_path += z_path

                #Calls the data 
                stats_nl_data = np.loadtxt(stats_nl_path, skiprows=1)
    
                stats_nl_k = stats_nl_data[:,0]
                stats_nl_err = stats_nl_data[:,1]

                #Create arrays that will be used to fill the complete summary arrays
                tot_nl_z = []

                #For list of lists
                tot_nl_z_ll = []

                #We perform a loop that looks into the bins for k
                #Doing this for lin
                #Much easier than doing a for loop because of list comprehension ALSO FASTER
                tot_ultra = 0 #initialize value for ultra large scales
                tot_lin = 0 #initialize for lin scales
                tot_quasi = 0 #initialize for quasi lin scales

                #k has to fall in the proper bins
                aux_k_ultra = (stats_nl_k >= ultra_scale_min) & (stats_nl_k < ultra_scale_max)
                aux_k_lin = (stats_nl_k >= lin_scale_min) & (stats_nl_k < lin_scale_max)
                aux_k_quasi = (stats_nl_k >= quasi_scale_min) & (stats_nl_k <= quasi_scale_max)

                #Looks at only the regime where clustering affects it
                if clustering_only == True:
                    aux_cluster_ultra = (stats_nl_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_k[aux_k_ultra] < cluster_reg_max)
                    aux_cluster_lin = (stats_nl_k[aux_k_lin] > cluster_reg_min) & (stats_nl_k[aux_k_lin] < cluster_reg_max)
                    aux_cluster_quasi = (stats_nl_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_k[aux_k_quasi] < cluster_reg_max)
            
                    #Calculate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs((stats_nl_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
                    w_lin = np.log10(np.abs((stats_nl_err[aux_k_lin])[aux_cluster_lin]) / thres)
                    w_quasi = np.log10(np.abs((stats_nl_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.
    
                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0

                    tot_ultra = np.sum(w_ultra)
                    tot_lin = np.sum(w_lin)
                    tot_quasi = np.sum(w_quasi)
                #calculates imprecision in any regime
                if clustering_only == False:
                    #caluclate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs(stats_nl_err[aux_k_ultra]) / thres)
                    w_lin = np.log10(np.abs(stats_nl_err[aux_k_lin]) / thres)
                    w_quasi = np.log10(np.abs(stats_nl_err[aux_k_quasi]) / thres)

                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.

                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0
    
                    #calculate the totals
                    tot_ultra = np.sum(w_ultra)
                    tot_lin = np.sum(w_lin)
                    tot_quasi = np.sum(w_quasi)
        
        
                #Append these values to our z summary stat
                #For list only
                tot_nl_z = np.append(tot_nl_z, tot_ultra)
                tot_nl_z = np.append(tot_nl_z, tot_lin)
                tot_nl_z = np.append(tot_nl_z, tot_quasi)

                #For list of lists
                tot_nl_z_ll.append(tot_ultra)
                tot_nl_z_ll.append(tot_lin)
                tot_nl_z_ll.append(tot_quasi)

                #Append these values for the general z stat
                #For list only
                tot_nl = np.append(tot_nl, tot_nl_z)
                #For list of lists
                tot_nl_ll.append(tot_nl_z_ll)

            #Appending the values for the k ranges
            tot_nl_k1_z1 = np.append(tot_nl_k1_z1, tot_nl_ll[0][0])
            tot_nl_k2_z1 = np.append(tot_nl_k2_z1, tot_nl_ll[0][1])
            tot_nl_k3_z1 = np.append(tot_nl_k3_z1, tot_nl_ll[0][2])

            tot_nl_k1_z2 = np.append(tot_nl_k1_z2, tot_nl_ll[1][0])
            tot_nl_k2_z2 = np.append(tot_nl_k2_z2, tot_nl_ll[1][1])
            tot_nl_k3_z2 = np.append(tot_nl_k3_z2, tot_nl_ll[1][2])

            tot_nl_k1_z3 = np.append(tot_nl_k1_z3, tot_nl_ll[2][0])
            tot_nl_k2_z3 = np.append(tot_nl_k2_z3, tot_nl_ll[2][1])
            tot_nl_k3_z3 = np.append(tot_nl_k3_z3, tot_nl_ll[2][2])

            tot_nl_k1_z4 = np.append(tot_nl_k1_z4, tot_nl_ll[3][0])
            tot_nl_k2_z4 = np.append(tot_nl_k2_z4, tot_nl_ll[3][1])
            tot_nl_k3_z4 = np.append(tot_nl_k3_z4, tot_nl_ll[3][2])

            tot_nl_k1_z5 = np.append(tot_nl_k1_z5, tot_nl_ll[4][0])
            tot_nl_k2_z5 = np.append(tot_nl_k2_z5, tot_nl_ll[4][1])
            tot_nl_k3_z5 = np.append(tot_nl_k3_z5, tot_nl_ll[4][2])

            tot_nl_k1_z6 = np.append(tot_nl_k1_z6, tot_nl_ll[5][0])
            tot_nl_k2_z6 = np.append(tot_nl_k2_z6, tot_nl_ll[5][1])
            tot_nl_k3_z6 = np.append(tot_nl_k3_z6, tot_nl_ll[5][2])

            tot_tot_nl = np.append(tot_tot_nl,np.sum(tot_nl))
            print 'Performing this for lin precise'
            #Gonna generate an array of arrays, with each row corresponding to a different z value
            #Each columns will correspond to a different bins of k_values
            tot_lin_pre = []

            #For list of lists
            tot_lin_pre_ll = []

            for j in range(len(z_vals)):
                z_val = z_vals[j]
                z_path ='_z%s.dat' %z_val
                print 'Performing z_val = ', z_val
        
                #For ease in iterating over different z values we use string manipulation
                stats_lin_pre_path = '../stats/lhs_mpk_err_lin_pk_%05d' %trial

                #Adds the z_path
                stats_lin_pre_path += z_path

                #Calls the data 
                stats_lin_pre_data = np.loadtxt(stats_lin_pre_path, skiprows=1)

                stats_lin_pre_k = stats_lin_pre_data[:,0]
                stats_lin_pre_err = stats_lin_pre_data[:,1]

                #Create arrays that will be used to fill the complete summary arrays
                tot_lin_pre_z = []

                #For list of lists
                tot_lin_pre_z_ll = []

                #We perform a loop that looks into the bins for k
                #Doing this for lin
                #Much easier than doing a for loop because of list comprehension ALSO FASTER
                tot_ultra = 0 #initialize value for ultra large scales
                tot_lin = 0 #initialize for lin scales
                tot_quasi = 0 #initialize for quasi lin scales

                #k has to fall in the proper bins
                aux_k_ultra = (stats_lin_pre_k >= ultra_scale_min) & (stats_lin_pre_k < ultra_scale_max)
                aux_k_lin = (stats_lin_pre_k >= lin_scale_min) & (stats_lin_pre_k < lin_scale_max)
                aux_k_quasi = (stats_lin_pre_k >= quasi_scale_min) & (stats_lin_pre_k <= quasi_scale_max)

                #Looks at only the regime where clustering affects it
                if clustering_only == True:
                    aux_cluster_ultra = (stats_lin_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_pre_k[aux_k_ultra] < cluster_reg_max)
                    aux_cluster_lin = (stats_lin_pre_k[aux_k_lin] > cluster_reg_min) & (stats_lin_pre_k[aux_k_lin] < cluster_reg_max)
                    aux_cluster_quasi = (stats_lin_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_pre_k[aux_k_quasi] < cluster_reg_max)
                
                    #Calculate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs((stats_lin_pre_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
                    w_lin = np.log10(np.abs((stats_lin_pre_err[aux_k_lin])[aux_cluster_lin]) / thres)
                    w_quasi = np.log10(np.abs((stats_lin_pre_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.

                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0

                    tot_ultra = np.sum(w_ultra)
                    tot_lin = np.sum(w_lin)
                    tot_quasi = np.sum(w_quasi)
                #calculates imprecision in any regime
                if clustering_only == False:
                    #caluclate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs(stats_lin_pre_err[aux_k_ultra]) / thres)
                    w_lin = np.log10(np.abs(stats_lin_pre_err[aux_k_lin]) / thres)
                    w_quasi = np.log10(np.abs(stats_lin_pre_err[aux_k_quasi]) / thres)
        
                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.

                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0

                    #calculate the totals
                    tot_ultra = np.sum(w_ultra)
                    tot_lin = np.sum(w_lin)
                    tot_quasi = np.sum(w_quasi)
            
            
                #Append these values to our z summary stat
                #For list only
                tot_lin_pre_z = np.append(tot_lin_pre_z, tot_ultra)
                tot_lin_pre_z = np.append(tot_lin_pre_z, tot_lin)
                tot_lin_pre_z = np.append(tot_lin_pre_z, tot_quasi)

                #For list of lists
                tot_lin_pre_z_ll.append(tot_ultra)
                tot_lin_pre_z_ll.append(tot_lin)
                tot_lin_pre_z_ll.append(tot_quasi)

                #Append these values for the general z stat
                #For list only
                tot_lin_pre = np.append(tot_lin_pre, tot_lin_pre_z)
                #For list of lists
                tot_lin_pre_ll.append(tot_lin_pre_z_ll)

            #Appending the values for the k ranges
            tot_lin_pre_k1_z1 = np.append(tot_lin_pre_k1_z1, tot_lin_pre_ll[0][0])
            tot_lin_pre_k2_z1 = np.append(tot_lin_pre_k2_z1, tot_lin_pre_ll[0][1])
            tot_lin_pre_k3_z1 = np.append(tot_lin_pre_k3_z1, tot_lin_pre_ll[0][2])

            tot_lin_pre_k1_z2 = np.append(tot_lin_pre_k1_z2, tot_lin_pre_ll[1][0])
            tot_lin_pre_k2_z2 = np.append(tot_lin_pre_k2_z2, tot_lin_pre_ll[1][1])
            tot_lin_pre_k3_z2 = np.append(tot_lin_pre_k3_z2, tot_lin_pre_ll[1][2])

            tot_lin_pre_k1_z3 = np.append(tot_lin_pre_k1_z3, tot_lin_pre_ll[2][0])
            tot_lin_pre_k2_z3 = np.append(tot_lin_pre_k2_z3, tot_lin_pre_ll[2][1])
            tot_lin_pre_k3_z3 = np.append(tot_lin_pre_k3_z3, tot_lin_pre_ll[2][2])

            tot_lin_pre_k1_z4 = np.append(tot_lin_pre_k1_z4, tot_lin_pre_ll[3][0])
            tot_lin_pre_k2_z4 = np.append(tot_lin_pre_k2_z4, tot_lin_pre_ll[3][1])
            tot_lin_pre_k3_z4 = np.append(tot_lin_pre_k3_z4, tot_lin_pre_ll[3][2])

            tot_lin_pre_k1_z5 = np.append(tot_lin_pre_k1_z5, tot_lin_pre_ll[4][0])
            tot_lin_pre_k2_z5 = np.append(tot_lin_pre_k2_z5, tot_lin_pre_ll[4][1])
            tot_lin_pre_k3_z5 = np.append(tot_lin_pre_k3_z5, tot_lin_pre_ll[4][2])

            tot_lin_pre_k1_z6 = np.append(tot_lin_pre_k1_z6, tot_lin_pre_ll[5][0])
            tot_lin_pre_k2_z6 = np.append(tot_lin_pre_k2_z6, tot_lin_pre_ll[5][1])
            tot_lin_pre_k3_z6 = np.append(tot_lin_pre_k3_z6, tot_lin_pre_ll[5][2])

            tot_tot_lin_pre = np.append(tot_tot_lin_pre, np.sum(tot_lin_pre))

            print 'Performing this for nonlin precision'
            #Gonna generate an array of arrays, with each row corresponding to a different z value
            #Each columns will correspond to a different bins of k_values
            tot_nl_pre = []

            #For list of lists
            tot_nl_pre_ll = []

            for j in range(len(z_vals)):
                z_val = z_vals[j]
                z_path ='_z%s.dat' %z_val
                print 'Performing z_val = ', z_val
            
                #For ease in iterating over different z values we use string manipulation
                stats_nl_pre_path = '../stats/lhs_mpk_err_nl_pk_%05d' %trial

                #Adds the z_path
                stats_nl_pre_path += z_path

                #Calls the data 
                stats_nl_pre_data = np.loadtxt(stats_nl_pre_path, skiprows=1)

                stats_nl_pre_k = stats_nl_pre_data[:,0]
                stats_nl_pre_err = stats_nl_pre_data[:,1]

                #Create arrays that will be used to fill the complete summary arrays
                tot_nl_pre_z = []

                #For list of lists
                tot_nl_pre_z_ll = []

                #We perform a loop that looks into the bins for k
                #Doing this for lin
                #Much easier than doing a for loop because of list comprehension ALSO FASTER
                tot_ultra = 0 #initialize value for ultra large scales
                tot_lin = 0 #initialize for lin scales
                tot_quasi = 0 #initialize for quasi lin scales

                #k has to fall in the proper bins
                aux_k_ultra = (stats_nl_pre_k >= ultra_scale_min) & (stats_nl_pre_k < ultra_scale_max)
                aux_k_lin = (stats_nl_pre_k >= lin_scale_min) & (stats_nl_pre_k < lin_scale_max)
                aux_k_quasi = (stats_nl_pre_k >= quasi_scale_min) & (stats_nl_pre_k <= quasi_scale_max)

                #Looks at only the regime where clustering affects it
                if clustering_only == True:
                    aux_cluster_ultra = (stats_nl_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_pre_k[aux_k_ultra] < cluster_reg_max)
                    aux_cluster_lin = (stats_nl_pre_k[aux_k_lin] > cluster_reg_min) & (stats_nl_pre_k[aux_k_lin] < cluster_reg_max)
                    aux_cluster_quasi = (stats_nl_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_pre_k[aux_k_quasi] < cluster_reg_max)
                
                    #Calculate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs((stats_nl_pre_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
                    w_lin = np.log10(np.abs((stats_nl_pre_err[aux_k_lin])[aux_cluster_lin]) / thres)
                    w_quasi = np.log10(np.abs((stats_nl_pre_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.

                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0

                    tot_ultra = np.sum(w_ultra)
                    tot_lin = np.sum(w_lin)
                    tot_quasi = np.sum(w_quasi)
                #calculates imprecision in any regime
                if clustering_only == False:
                    #caluclate the weights i.e. how badly has this bin failed
                    w_ultra = np.log10(np.abs(stats_nl_pre_err[aux_k_ultra]) / thres)
                    w_lin = np.log10(np.abs(stats_nl_pre_err[aux_k_lin]) / thres)
                    w_quasi = np.log10(np.abs(stats_nl_pre_err[aux_k_quasi]) / thres)

                    #Make all the negative values = 0, since that means they didn't pass the threshold
                    aux_ultra_neg = w_ultra < 0.
                    aux_lin_neg = w_lin < 0.
                    aux_quasi_neg = w_quasi < 0.

                    w_ultra[aux_ultra_neg] = 0
                    w_lin[aux_lin_neg] = 0
                    w_quasi[aux_quasi_neg] = 0

                    #calculate the totals
                    tot_ultra = np.sum(w_ultra)
                    tot_lin = np.sum(w_lin)
                    tot_quasi = np.sum(w_quasi)
            
            
                #Append these values to our z summary stat
                #For list only
                tot_nl_pre_z = np.append(tot_nl_pre_z, tot_ultra)
                tot_nl_pre_z = np.append(tot_nl_pre_z, tot_lin)
                tot_nl_pre_z = np.append(tot_nl_pre_z, tot_quasi)

                #For list of lists
                tot_nl_pre_z_ll.append(tot_ultra)
                tot_nl_pre_z_ll.append(tot_lin)
                tot_nl_pre_z_ll.append(tot_quasi)

                #Append these values for the general z stat
                #For list only
                tot_nl_pre = np.append(tot_nl_pre, tot_nl_pre_z)
                #For list of lists
                tot_nl_pre_ll.append(tot_nl_pre_z_ll)

            #Appending the values for the k ranges
            tot_nl_pre_k1_z1 = np.append(tot_nl_pre_k1_z1, tot_nl_pre_ll[0][0])
            tot_nl_pre_k2_z1 = np.append(tot_nl_pre_k2_z1, tot_nl_pre_ll[0][1])
            tot_nl_pre_k3_z1 = np.append(tot_nl_pre_k3_z1, tot_nl_pre_ll[0][2])

            tot_nl_pre_k1_z2 = np.append(tot_nl_pre_k1_z2, tot_nl_pre_ll[1][0])
            tot_nl_pre_k2_z2 = np.append(tot_nl_pre_k2_z2, tot_nl_pre_ll[1][1])
            tot_nl_pre_k3_z2 = np.append(tot_nl_pre_k3_z2, tot_nl_pre_ll[1][2])

            tot_nl_pre_k1_z3 = np.append(tot_nl_pre_k1_z3, tot_nl_pre_ll[2][0])
            tot_nl_pre_k2_z3 = np.append(tot_nl_pre_k2_z3, tot_nl_pre_ll[2][1])
            tot_nl_pre_k3_z3 = np.append(tot_nl_pre_k3_z3, tot_nl_pre_ll[2][2])

            tot_nl_pre_k1_z4 = np.append(tot_nl_pre_k1_z4, tot_nl_pre_ll[3][0])
            tot_nl_pre_k2_z4 = np.append(tot_nl_pre_k2_z4, tot_nl_pre_ll[3][1])
            tot_nl_pre_k3_z4 = np.append(tot_nl_pre_k3_z4, tot_nl_pre_ll[3][2])

            tot_nl_pre_k1_z5 = np.append(tot_nl_pre_k1_z5, tot_nl_pre_ll[4][0])
            tot_nl_pre_k2_z5 = np.append(tot_nl_pre_k2_z5, tot_nl_pre_ll[4][1])
            tot_nl_pre_k3_z5 = np.append(tot_nl_pre_k3_z5, tot_nl_pre_ll[4][2])

            tot_nl_pre_k1_z6 = np.append(tot_nl_pre_k1_z6, tot_nl_pre_ll[5][0])
            tot_nl_pre_k2_z6 = np.append(tot_nl_pre_k2_z6, tot_nl_pre_ll[5][1])
            tot_nl_pre_k3_z6 = np.append(tot_nl_pre_k3_z6, tot_nl_pre_ll[5][2])

            tot_tot_nl_pre = np.append(tot_tot_nl_pre, np.sum(tot_nl_pre))
    
        #For list of lists, will be useful in the future. TRUST
        tot_lin_k1_z1_ll.append(tot_lin_k1_z1)
        tot_lin_k2_z1_ll.append(tot_lin_k2_z1)
        tot_lin_k3_z1_ll.append(tot_lin_k3_z1)

        tot_lin_k1_z2_ll.append(tot_lin_k1_z2)
        tot_lin_k2_z2_ll.append(tot_lin_k2_z2)
        tot_lin_k3_z2_ll.append(tot_lin_k3_z2)

        tot_lin_k1_z3_ll.append(tot_lin_k1_z3)
        tot_lin_k2_z3_ll.append(tot_lin_k2_z3)
        tot_lin_k3_z3_ll.append(tot_lin_k3_z3)

        tot_lin_k1_z4_ll.append(tot_lin_k1_z4)
        tot_lin_k2_z4_ll.append(tot_lin_k2_z4)
        tot_lin_k3_z4_ll.append(tot_lin_k3_z4)

        tot_lin_k1_z5_ll.append(tot_lin_k1_z5)
        tot_lin_k2_z5_ll.append(tot_lin_k2_z5)
        tot_lin_k3_z5_ll.append(tot_lin_k3_z5)

        tot_lin_k1_z6_ll.append(tot_lin_k1_z6)
        tot_lin_k2_z6_ll.append(tot_lin_k2_z6)
        tot_lin_k3_z6_ll.append(tot_lin_k3_z6)

        tot_nl_k1_z1_ll.append(tot_nl_k1_z1)
        tot_nl_k2_z1_ll.append(tot_nl_k2_z1)
        tot_nl_k3_z1_ll.append(tot_nl_k3_z1)

        tot_nl_k1_z2_ll.append(tot_nl_k1_z2)
        tot_nl_k2_z2_ll.append(tot_nl_k2_z2)
        tot_nl_k3_z2_ll.append(tot_nl_k3_z2)

        tot_nl_k1_z3_ll.append(tot_nl_k1_z3)
        tot_nl_k2_z3_ll.append(tot_nl_k2_z3)
        tot_nl_k3_z3_ll.append(tot_nl_k3_z3)

        tot_nl_k1_z4_ll.append(tot_nl_k1_z4)
        tot_nl_k2_z4_ll.append(tot_nl_k2_z4)
        tot_nl_k3_z4_ll.append(tot_nl_k3_z4)

        tot_nl_k1_z5_ll.append(tot_nl_k1_z5)
        tot_nl_k2_z5_ll.append(tot_nl_k2_z5)
        tot_nl_k3_z5_ll.append(tot_nl_k3_z5)

        tot_nl_k1_z6_ll.append(tot_nl_k1_z6)
        tot_nl_k2_z6_ll.append(tot_nl_k2_z6)
        tot_nl_k3_z6_ll.append(tot_nl_k3_z6)

        tot_lin_pre_k1_z1_ll.append(tot_lin_pre_k1_z1)
        tot_lin_pre_k2_z1_ll.append(tot_lin_pre_k2_z1)
        tot_lin_pre_k3_z1_ll.append(tot_lin_pre_k3_z1)

        tot_lin_pre_k1_z2_ll.append(tot_lin_pre_k1_z2)
        tot_lin_pre_k2_z2_ll.append(tot_lin_pre_k2_z2)
        tot_lin_pre_k3_z2_ll.append(tot_lin_pre_k3_z2)

        tot_lin_pre_k1_z3_ll.append(tot_lin_pre_k1_z3)
        tot_lin_pre_k2_z3_ll.append(tot_lin_pre_k2_z3)
        tot_lin_pre_k3_z3_ll.append(tot_lin_pre_k3_z3)

        tot_lin_pre_k1_z4_ll.append(tot_lin_pre_k1_z4)
        tot_lin_pre_k2_z4_ll.append(tot_lin_pre_k2_z4)
        tot_lin_pre_k3_z4_ll.append(tot_lin_pre_k3_z4)

        tot_lin_pre_k1_z5_ll.append(tot_lin_pre_k1_z5)
        tot_lin_pre_k2_z5_ll.append(tot_lin_pre_k2_z5)
        tot_lin_pre_k3_z5_ll.append(tot_lin_pre_k3_z5)

        tot_lin_pre_k1_z6_ll.append(tot_lin_pre_k1_z6)
        tot_lin_pre_k2_z6_ll.append(tot_lin_pre_k2_z6)
        tot_lin_pre_k3_z6_ll.append(tot_lin_pre_k3_z6)

        tot_nl_pre_k1_z1_ll.append(tot_nl_pre_k1_z1)
        tot_nl_pre_k2_z1_ll.append(tot_nl_pre_k2_z1)
        tot_nl_pre_k3_z1_ll.append(tot_nl_pre_k3_z1)

        tot_nl_pre_k1_z2_ll.append(tot_nl_pre_k1_z2)
        tot_nl_pre_k2_z2_ll.append(tot_nl_pre_k2_z2)
        tot_nl_pre_k3_z2_ll.append(tot_nl_pre_k3_z2)

        tot_nl_pre_k1_z3_ll.append(tot_nl_pre_k1_z3)
        tot_nl_pre_k2_z3_ll.append(tot_nl_pre_k2_z3)
        tot_nl_pre_k3_z3_ll.append(tot_nl_pre_k3_z3)

        tot_nl_pre_k1_z4_ll.append(tot_nl_pre_k1_z4)
        tot_nl_pre_k2_z4_ll.append(tot_nl_pre_k2_z4)
        tot_nl_pre_k3_z4_ll.append(tot_nl_pre_k3_z4)

        tot_nl_pre_k1_z5_ll.append(tot_nl_pre_k1_z5)
        tot_nl_pre_k2_z5_ll.append(tot_nl_pre_k2_z5)
        tot_nl_pre_k3_z5_ll.append(tot_nl_pre_k3_z5)

        tot_nl_pre_k1_z6_ll.append(tot_nl_pre_k1_z6)
        tot_nl_pre_k2_z6_ll.append(tot_nl_pre_k2_z6)
        tot_nl_pre_k3_z6_ll.append(tot_nl_pre_k3_z6)


    #Creates a dictionary since that's what ColumnDataSource takes in
    #data_lin = {'tot_tot_lin':tot_tot_lin,
    data_lin = {'tot_lin_h1_k1_z1':tot_lin_k1_z1_ll[0],
                'tot_lin_h1_k2_z1':tot_lin_k2_z1_ll[0],
                'tot_lin_h1_k3_z1':tot_lin_k3_z1_ll[0],
                'tot_lin_h1_k1_z2':tot_lin_k1_z2_ll[0],
                'tot_lin_h1_k2_z2':tot_lin_k2_z2_ll[0],
                'tot_lin_h1_k3_z2':tot_lin_k3_z2_ll[0],
                'tot_lin_h1_k1_z3':tot_lin_k1_z3_ll[0],
                'tot_lin_h1_k2_z3':tot_lin_k2_z3_ll[0],
                'tot_lin_h1_k3_z3':tot_lin_k3_z3_ll[0],
                'tot_lin_h1_k1_z4':tot_lin_k1_z4_ll[0],
                'tot_lin_h1_k2_z4':tot_lin_k2_z4_ll[0],
                'tot_lin_h1_k3_z4':tot_lin_k3_z4_ll[0],
                'tot_lin_h1_k1_z5':tot_lin_k1_z5_ll[0],
                'tot_lin_h1_k2_z5':tot_lin_k2_z5_ll[0],
                'tot_lin_h1_k3_z5':tot_lin_k3_z5_ll[0],
                'tot_lin_h1_k1_z6':tot_lin_k1_z6_ll[0],
                'tot_lin_h1_k2_z6':tot_lin_k2_z6_ll[0],
                'tot_lin_h1_k3_z6':tot_lin_k3_z6_ll[0],
                'tot_lin_h2_k1_z1':tot_lin_k1_z1_ll[1],
                'tot_lin_h2_k2_z1':tot_lin_k2_z1_ll[1],
                'tot_lin_h2_k3_z1':tot_lin_k3_z1_ll[1],
                'tot_lin_h2_k1_z2':tot_lin_k1_z2_ll[1],
                'tot_lin_h2_k2_z2':tot_lin_k2_z2_ll[1],
                'tot_lin_h2_k3_z2':tot_lin_k3_z2_ll[1],
                'tot_lin_h2_k1_z3':tot_lin_k1_z3_ll[1],
                'tot_lin_h2_k2_z3':tot_lin_k2_z3_ll[1],
                'tot_lin_h2_k3_z3':tot_lin_k3_z3_ll[1],
                'tot_lin_h2_k1_z4':tot_lin_k1_z4_ll[1],
                'tot_lin_h2_k2_z4':tot_lin_k2_z4_ll[1],
                'tot_lin_h2_k3_z4':tot_lin_k3_z4_ll[1],
                'tot_lin_h2_k1_z5':tot_lin_k1_z5_ll[1],
                'tot_lin_h2_k2_z5':tot_lin_k2_z5_ll[1],
                'tot_lin_h2_k3_z5':tot_lin_k3_z5_ll[1],
                'tot_lin_h2_k1_z6':tot_lin_k1_z6_ll[1],
                'tot_lin_h2_k2_z6':tot_lin_k2_z6_ll[1],
                'tot_lin_h2_k3_z6':tot_lin_k3_z6_ll[1],
                'tot_lin_h3_k1_z1':tot_lin_k1_z1_ll[2],
                'tot_lin_h3_k2_z1':tot_lin_k2_z1_ll[2],
                'tot_lin_h3_k3_z1':tot_lin_k3_z1_ll[2],
                'tot_lin_h3_k1_z2':tot_lin_k1_z2_ll[2],
                'tot_lin_h3_k2_z2':tot_lin_k2_z2_ll[2],
                'tot_lin_h3_k3_z2':tot_lin_k3_z2_ll[2],
                'tot_lin_h3_k1_z3':tot_lin_k1_z3_ll[2],
                'tot_lin_h3_k2_z3':tot_lin_k2_z3_ll[2],
                'tot_lin_h3_k3_z3':tot_lin_k3_z3_ll[2],
                'tot_lin_h3_k1_z4':tot_lin_k1_z4_ll[2],
                'tot_lin_h3_k2_z4':tot_lin_k2_z4_ll[2],
                'tot_lin_h3_k3_z4':tot_lin_k3_z4_ll[2],
                'tot_lin_h3_k1_z5':tot_lin_k1_z5_ll[2],
                'tot_lin_h3_k2_z5':tot_lin_k2_z5_ll[2],
                'tot_lin_h3_k3_z5':tot_lin_k3_z5_ll[2],
                'tot_lin_h3_k1_z6':tot_lin_k1_z6_ll[2],
                'tot_lin_h3_k2_z6':tot_lin_k2_z6_ll[2],
                'tot_lin_h3_k3_z6':tot_lin_k3_z6_ll[2],
                'tot_lin_h4_k1_z1':tot_lin_k1_z1_ll[3],
                'tot_lin_h4_k2_z1':tot_lin_k2_z1_ll[3],
                'tot_lin_h4_k3_z1':tot_lin_k3_z1_ll[3],
                'tot_lin_h4_k1_z2':tot_lin_k1_z2_ll[3],
                'tot_lin_h4_k2_z2':tot_lin_k2_z2_ll[3],
                'tot_lin_h4_k3_z2':tot_lin_k3_z2_ll[3],
                'tot_lin_h4_k1_z3':tot_lin_k1_z3_ll[3],
                'tot_lin_h4_k2_z3':tot_lin_k2_z3_ll[3],
                'tot_lin_h4_k3_z3':tot_lin_k3_z3_ll[3],
                'tot_lin_h4_k1_z4':tot_lin_k1_z4_ll[3],
                'tot_lin_h4_k2_z4':tot_lin_k2_z4_ll[3],
                'tot_lin_h4_k3_z4':tot_lin_k3_z4_ll[3],
                'tot_lin_h4_k1_z5':tot_lin_k1_z5_ll[3],
                'tot_lin_h4_k2_z5':tot_lin_k2_z5_ll[3],
                'tot_lin_h4_k3_z5':tot_lin_k3_z5_ll[3],
                'tot_lin_h4_k1_z6':tot_lin_k1_z6_ll[3],
                'tot_lin_h4_k2_z6':tot_lin_k2_z6_ll[3],
                'tot_lin_h4_k3_z6':tot_lin_k3_z6_ll[3],
                'tot_lin_h5_k1_z1':tot_lin_k1_z1_ll[4],
                'tot_lin_h5_k2_z1':tot_lin_k2_z1_ll[4],
                'tot_lin_h5_k3_z1':tot_lin_k3_z1_ll[4],
                'tot_lin_h5_k1_z2':tot_lin_k1_z2_ll[4],
                'tot_lin_h5_k2_z2':tot_lin_k2_z2_ll[4],
                'tot_lin_h5_k3_z2':tot_lin_k3_z2_ll[4],
                'tot_lin_h5_k1_z3':tot_lin_k1_z3_ll[4],
                'tot_lin_h5_k2_z3':tot_lin_k2_z3_ll[4],
                'tot_lin_h5_k3_z3':tot_lin_k3_z3_ll[4],
                'tot_lin_h5_k1_z4':tot_lin_k1_z4_ll[4],
                'tot_lin_h5_k2_z4':tot_lin_k2_z4_ll[4],
                'tot_lin_h5_k3_z4':tot_lin_k3_z4_ll[4],
                'tot_lin_h5_k1_z5':tot_lin_k1_z5_ll[4],
                'tot_lin_h5_k2_z5':tot_lin_k2_z5_ll[4],
                'tot_lin_h5_k3_z5':tot_lin_k3_z5_ll[4],
                'tot_lin_h5_k1_z6':tot_lin_k1_z6_ll[4],
                'tot_lin_h5_k2_z6':tot_lin_k2_z6_ll[4],
                'tot_lin_h5_k3_z6':tot_lin_k3_z6_ll[4],
                'tot_lin_h6_k1_z1':tot_lin_k1_z1_ll[5],
                'tot_lin_h6_k2_z1':tot_lin_k2_z1_ll[5],
                'tot_lin_h6_k3_z1':tot_lin_k3_z1_ll[5],
                'tot_lin_h6_k1_z2':tot_lin_k1_z2_ll[5],
                'tot_lin_h6_k2_z2':tot_lin_k2_z2_ll[5],
                'tot_lin_h6_k3_z2':tot_lin_k3_z2_ll[5],
                'tot_lin_h6_k1_z3':tot_lin_k1_z3_ll[5],
                'tot_lin_h6_k2_z3':tot_lin_k2_z3_ll[5],
                'tot_lin_h6_k3_z3':tot_lin_k3_z3_ll[5],
                'tot_lin_h6_k1_z4':tot_lin_k1_z4_ll[5],
                'tot_lin_h6_k2_z4':tot_lin_k2_z4_ll[5],
                'tot_lin_h6_k3_z4':tot_lin_k3_z4_ll[5],
                'tot_lin_h6_k1_z5':tot_lin_k1_z5_ll[5],
                'tot_lin_h6_k2_z5':tot_lin_k2_z5_ll[5],
                'tot_lin_h6_k3_z5':tot_lin_k3_z5_ll[5],
                'tot_lin_h6_k1_z6':tot_lin_k1_z6_ll[5],
                'tot_lin_h6_k2_z6':tot_lin_k2_z6_ll[5],
                'tot_lin_h6_k3_z6':tot_lin_k3_z6_ll[5]}
    #data_nl = { 'tot_tot_nl':tot_tot_nl,
    data_nl = { 'tot_nl_h1_k1_z1':tot_nl_k1_z1_ll[0],
                'tot_nl_h1_k2_z1':tot_nl_k2_z1_ll[0],
                'tot_nl_h1_k3_z1':tot_nl_k3_z1_ll[0],
                'tot_nl_h1_k1_z2':tot_nl_k1_z2_ll[0],
                'tot_nl_h1_k2_z2':tot_nl_k2_z2_ll[0],
                'tot_nl_h1_k3_z2':tot_nl_k3_z2_ll[0],
                'tot_nl_h1_k1_z3':tot_nl_k1_z3_ll[0],
                'tot_nl_h1_k2_z3':tot_nl_k2_z3_ll[0],
                'tot_nl_h1_k3_z3':tot_nl_k3_z3_ll[0],
                'tot_nl_h1_k1_z4':tot_nl_k1_z4_ll[0],
                'tot_nl_h1_k2_z4':tot_nl_k2_z4_ll[0],
                'tot_nl_h1_k3_z4':tot_nl_k3_z4_ll[0],
                'tot_nl_h1_k1_z5':tot_nl_k1_z5_ll[0],
                'tot_nl_h1_k2_z5':tot_nl_k2_z5_ll[0],
                'tot_nl_h1_k3_z5':tot_nl_k3_z5_ll[0],
                'tot_nl_h1_k1_z6':tot_nl_k1_z6_ll[0],
                'tot_nl_h1_k2_z6':tot_nl_k2_z6_ll[0],
                'tot_nl_h1_k3_z6':tot_nl_k3_z6_ll[0],
                'tot_nl_h2_k1_z1':tot_nl_k1_z1_ll[1],
                'tot_nl_h2_k2_z1':tot_nl_k2_z1_ll[1],
                'tot_nl_h2_k3_z1':tot_nl_k3_z1_ll[1],
                'tot_nl_h2_k1_z2':tot_nl_k1_z2_ll[1],
                'tot_nl_h2_k2_z2':tot_nl_k2_z2_ll[1],
                'tot_nl_h2_k3_z2':tot_nl_k3_z2_ll[1],
                'tot_nl_h2_k1_z3':tot_nl_k1_z3_ll[1],
                'tot_nl_h2_k2_z3':tot_nl_k2_z3_ll[1],
                'tot_nl_h2_k3_z3':tot_nl_k3_z3_ll[1],
                'tot_nl_h2_k1_z4':tot_nl_k1_z4_ll[1],
                'tot_nl_h2_k2_z4':tot_nl_k2_z4_ll[1],
                'tot_nl_h2_k3_z4':tot_nl_k3_z4_ll[1],
                'tot_nl_h2_k1_z5':tot_nl_k1_z5_ll[1],
                'tot_nl_h2_k2_z5':tot_nl_k2_z5_ll[1],
                'tot_nl_h2_k3_z5':tot_nl_k3_z5_ll[1],
                'tot_nl_h2_k1_z6':tot_nl_k1_z6_ll[1],
                'tot_nl_h2_k2_z6':tot_nl_k2_z6_ll[1],
                'tot_nl_h2_k3_z6':tot_nl_k3_z6_ll[1],
                'tot_nl_h3_k1_z1':tot_nl_k1_z1_ll[2],
                'tot_nl_h3_k2_z1':tot_nl_k2_z1_ll[2],
                'tot_nl_h3_k3_z1':tot_nl_k3_z1_ll[2],
                'tot_nl_h3_k1_z2':tot_nl_k1_z2_ll[2],
                'tot_nl_h3_k2_z2':tot_nl_k2_z2_ll[2],
                'tot_nl_h3_k3_z2':tot_nl_k3_z2_ll[2],
                'tot_nl_h3_k1_z3':tot_nl_k1_z3_ll[2],
                'tot_nl_h3_k2_z3':tot_nl_k2_z3_ll[2],
                'tot_nl_h3_k3_z3':tot_nl_k3_z3_ll[2],
                'tot_nl_h3_k1_z4':tot_nl_k1_z4_ll[2],
                'tot_nl_h3_k2_z4':tot_nl_k2_z4_ll[2],
                'tot_nl_h3_k3_z4':tot_nl_k3_z4_ll[2],
                'tot_nl_h3_k1_z5':tot_nl_k1_z5_ll[2],
                'tot_nl_h3_k2_z5':tot_nl_k2_z5_ll[2],
                'tot_nl_h3_k3_z5':tot_nl_k3_z5_ll[2],
                'tot_nl_h3_k1_z6':tot_nl_k1_z6_ll[2],
                'tot_nl_h3_k2_z6':tot_nl_k2_z6_ll[2],
                'tot_nl_h3_k3_z6':tot_nl_k3_z6_ll[2],
                'tot_nl_h4_k1_z1':tot_nl_k1_z1_ll[3],
                'tot_nl_h4_k2_z1':tot_nl_k2_z1_ll[3],
                'tot_nl_h4_k3_z1':tot_nl_k3_z1_ll[3],
                'tot_nl_h4_k1_z2':tot_nl_k1_z2_ll[3],
                'tot_nl_h4_k2_z2':tot_nl_k2_z2_ll[3],
                'tot_nl_h4_k3_z2':tot_nl_k3_z2_ll[3],
                'tot_nl_h4_k1_z3':tot_nl_k1_z3_ll[3],
                'tot_nl_h4_k2_z3':tot_nl_k2_z3_ll[3],
                'tot_nl_h4_k3_z3':tot_nl_k3_z3_ll[3],
                'tot_nl_h4_k1_z4':tot_nl_k1_z4_ll[3],
                'tot_nl_h4_k2_z4':tot_nl_k2_z4_ll[3],
                'tot_nl_h4_k3_z4':tot_nl_k3_z4_ll[3],
                'tot_nl_h4_k1_z5':tot_nl_k1_z5_ll[3],
                'tot_nl_h4_k2_z5':tot_nl_k2_z5_ll[3],
                'tot_nl_h4_k3_z5':tot_nl_k3_z5_ll[3],
                'tot_nl_h4_k1_z6':tot_nl_k1_z6_ll[3],
                'tot_nl_h4_k2_z6':tot_nl_k2_z6_ll[3],
                'tot_nl_h4_k3_z6':tot_nl_k3_z6_ll[3],
                'tot_nl_h5_k1_z1':tot_nl_k1_z1_ll[4],
                'tot_nl_h5_k2_z1':tot_nl_k2_z1_ll[4],
                'tot_nl_h5_k3_z1':tot_nl_k3_z1_ll[4],
                'tot_nl_h5_k1_z2':tot_nl_k1_z2_ll[4],
                'tot_nl_h5_k2_z2':tot_nl_k2_z2_ll[4],
                'tot_nl_h5_k3_z2':tot_nl_k3_z2_ll[4],
                'tot_nl_h5_k1_z3':tot_nl_k1_z3_ll[4],
                'tot_nl_h5_k2_z3':tot_nl_k2_z3_ll[4],
                'tot_nl_h5_k3_z3':tot_nl_k3_z3_ll[4],
                'tot_nl_h5_k1_z4':tot_nl_k1_z4_ll[4],
                'tot_nl_h5_k2_z4':tot_nl_k2_z4_ll[4],
                'tot_nl_h5_k3_z4':tot_nl_k3_z4_ll[4],
                'tot_nl_h5_k1_z5':tot_nl_k1_z5_ll[4],
                'tot_nl_h5_k2_z5':tot_nl_k2_z5_ll[4],
                'tot_nl_h5_k3_z5':tot_nl_k3_z5_ll[4],
                'tot_nl_h5_k1_z6':tot_nl_k1_z6_ll[4],
                'tot_nl_h5_k2_z6':tot_nl_k2_z6_ll[4],
                'tot_nl_h5_k3_z6':tot_nl_k3_z6_ll[4],
                'tot_nl_h6_k1_z1':tot_nl_k1_z1_ll[5],
                'tot_nl_h6_k2_z1':tot_nl_k2_z1_ll[5],
                'tot_nl_h6_k3_z1':tot_nl_k3_z1_ll[5],
                'tot_nl_h6_k1_z2':tot_nl_k1_z2_ll[5],
                'tot_nl_h6_k2_z2':tot_nl_k2_z2_ll[5],
                'tot_nl_h6_k3_z2':tot_nl_k3_z2_ll[5],
                'tot_nl_h6_k1_z3':tot_nl_k1_z3_ll[5],
                'tot_nl_h6_k2_z3':tot_nl_k2_z3_ll[5],
                'tot_nl_h6_k3_z3':tot_nl_k3_z3_ll[5],
                'tot_nl_h6_k1_z4':tot_nl_k1_z4_ll[5],
                'tot_nl_h6_k2_z4':tot_nl_k2_z4_ll[5],
                'tot_nl_h6_k3_z4':tot_nl_k3_z4_ll[5],
                'tot_nl_h6_k1_z5':tot_nl_k1_z5_ll[5],
                'tot_nl_h6_k2_z5':tot_nl_k2_z5_ll[5],
                'tot_nl_h6_k3_z5':tot_nl_k3_z5_ll[5],
                'tot_nl_h6_k1_z6':tot_nl_k1_z6_ll[5],
                'tot_nl_h6_k2_z6':tot_nl_k2_z6_ll[5],
                'tot_nl_h6_k3_z6':tot_nl_k3_z6_ll[5]}

    
    #data_lin_pre = {'tot_tot_lin_pre':tot_tot_lin_pre,
    data_lin_pre = {'tot_lin_pre_h1_k1_z1':tot_lin_pre_k1_z1_ll[0],
                'tot_lin_pre_h1_k2_z1':tot_lin_pre_k2_z1_ll[0],
                'tot_lin_pre_h1_k3_z1':tot_lin_pre_k3_z1_ll[0],
                'tot_lin_pre_h1_k1_z2':tot_lin_pre_k1_z2_ll[0],
                'tot_lin_pre_h1_k2_z2':tot_lin_pre_k2_z2_ll[0],
                'tot_lin_pre_h1_k3_z2':tot_lin_pre_k3_z2_ll[0],
                'tot_lin_pre_h1_k1_z3':tot_lin_pre_k1_z3_ll[0],
                'tot_lin_pre_h1_k2_z3':tot_lin_pre_k2_z3_ll[0],
                'tot_lin_pre_h1_k3_z3':tot_lin_pre_k3_z3_ll[0],
                'tot_lin_pre_h1_k1_z4':tot_lin_pre_k1_z4_ll[0],
                'tot_lin_pre_h1_k2_z4':tot_lin_pre_k2_z4_ll[0],
                'tot_lin_pre_h1_k3_z4':tot_lin_pre_k3_z4_ll[0],
                'tot_lin_pre_h1_k1_z5':tot_lin_pre_k1_z5_ll[0],
                'tot_lin_pre_h1_k2_z5':tot_lin_pre_k2_z5_ll[0],
                'tot_lin_pre_h1_k3_z5':tot_lin_pre_k3_z5_ll[0],
                'tot_lin_pre_h1_k1_z6':tot_lin_pre_k1_z6_ll[0],
                'tot_lin_pre_h1_k2_z6':tot_lin_pre_k2_z6_ll[0],
                'tot_lin_pre_h1_k3_z6':tot_lin_pre_k3_z6_ll[0],
                'tot_lin_pre_h2_k1_z1':tot_lin_pre_k1_z1_ll[1],
                'tot_lin_pre_h2_k2_z1':tot_lin_pre_k2_z1_ll[1],
                'tot_lin_pre_h2_k3_z1':tot_lin_pre_k3_z1_ll[1],
                'tot_lin_pre_h2_k1_z2':tot_lin_pre_k1_z2_ll[1],
                'tot_lin_pre_h2_k2_z2':tot_lin_pre_k2_z2_ll[1],
                'tot_lin_pre_h2_k3_z2':tot_lin_pre_k3_z2_ll[1],
                'tot_lin_pre_h2_k1_z3':tot_lin_pre_k1_z3_ll[1],
                'tot_lin_pre_h2_k2_z3':tot_lin_pre_k2_z3_ll[1],
                'tot_lin_pre_h2_k3_z3':tot_lin_pre_k3_z3_ll[1],
                'tot_lin_pre_h2_k1_z4':tot_lin_pre_k1_z4_ll[1],
                'tot_lin_pre_h2_k2_z4':tot_lin_pre_k2_z4_ll[1],
                'tot_lin_pre_h2_k3_z4':tot_lin_pre_k3_z4_ll[1],
                'tot_lin_pre_h2_k1_z5':tot_lin_pre_k1_z5_ll[1],
                'tot_lin_pre_h2_k2_z5':tot_lin_pre_k2_z5_ll[1],
                'tot_lin_pre_h2_k3_z5':tot_lin_pre_k3_z5_ll[1],
                'tot_lin_pre_h2_k1_z6':tot_lin_pre_k1_z6_ll[1],
                'tot_lin_pre_h2_k2_z6':tot_lin_pre_k2_z6_ll[1],
                'tot_lin_pre_h2_k3_z6':tot_lin_pre_k3_z6_ll[1],
                'tot_lin_pre_h3_k1_z1':tot_lin_pre_k1_z1_ll[2],
                'tot_lin_pre_h3_k2_z1':tot_lin_pre_k2_z1_ll[2],
                'tot_lin_pre_h3_k3_z1':tot_lin_pre_k3_z1_ll[2],
                'tot_lin_pre_h3_k1_z2':tot_lin_pre_k1_z2_ll[2],
                'tot_lin_pre_h3_k2_z2':tot_lin_pre_k2_z2_ll[2],
                'tot_lin_pre_h3_k3_z2':tot_lin_pre_k3_z2_ll[2],
                'tot_lin_pre_h3_k1_z3':tot_lin_pre_k1_z3_ll[2],
                'tot_lin_pre_h3_k2_z3':tot_lin_pre_k2_z3_ll[2],
                'tot_lin_pre_h3_k3_z3':tot_lin_pre_k3_z3_ll[2],
                'tot_lin_pre_h3_k1_z4':tot_lin_pre_k1_z4_ll[2],
                'tot_lin_pre_h3_k2_z4':tot_lin_pre_k2_z4_ll[2],
                'tot_lin_pre_h3_k3_z4':tot_lin_pre_k3_z4_ll[2],
                'tot_lin_pre_h3_k1_z5':tot_lin_pre_k1_z5_ll[2],
                'tot_lin_pre_h3_k2_z5':tot_lin_pre_k2_z5_ll[2],
                'tot_lin_pre_h3_k3_z5':tot_lin_pre_k3_z5_ll[2],
                'tot_lin_pre_h3_k1_z6':tot_lin_pre_k1_z6_ll[2],
                'tot_lin_pre_h3_k2_z6':tot_lin_pre_k2_z6_ll[2],
                'tot_lin_pre_h3_k3_z6':tot_lin_pre_k3_z6_ll[2],
                'tot_lin_pre_h4_k1_z1':tot_lin_pre_k1_z1_ll[3],
                'tot_lin_pre_h4_k2_z1':tot_lin_pre_k2_z1_ll[3],
                'tot_lin_pre_h4_k3_z1':tot_lin_pre_k3_z1_ll[3],
                'tot_lin_pre_h4_k1_z2':tot_lin_pre_k1_z2_ll[3],
                'tot_lin_pre_h4_k2_z2':tot_lin_pre_k2_z2_ll[3],
                'tot_lin_pre_h4_k3_z2':tot_lin_pre_k3_z2_ll[3],
                'tot_lin_pre_h4_k1_z3':tot_lin_pre_k1_z3_ll[3],
                'tot_lin_pre_h4_k2_z3':tot_lin_pre_k2_z3_ll[3],
                'tot_lin_pre_h4_k3_z3':tot_lin_pre_k3_z3_ll[3],
                'tot_lin_pre_h4_k1_z4':tot_lin_pre_k1_z4_ll[3],
                'tot_lin_pre_h4_k2_z4':tot_lin_pre_k2_z4_ll[3],
                'tot_lin_pre_h4_k3_z4':tot_lin_pre_k3_z4_ll[3],
                'tot_lin_pre_h4_k1_z5':tot_lin_pre_k1_z5_ll[3],
                'tot_lin_pre_h4_k2_z5':tot_lin_pre_k2_z5_ll[3],
                'tot_lin_pre_h4_k3_z5':tot_lin_pre_k3_z5_ll[3],
                'tot_lin_pre_h4_k1_z6':tot_lin_pre_k1_z6_ll[3],
                'tot_lin_pre_h4_k2_z6':tot_lin_pre_k2_z6_ll[3],
                'tot_lin_pre_h4_k3_z6':tot_lin_pre_k3_z6_ll[3],
                'tot_lin_pre_h5_k1_z1':tot_lin_pre_k1_z1_ll[4],
                'tot_lin_pre_h5_k2_z1':tot_lin_pre_k2_z1_ll[4],
                'tot_lin_pre_h5_k3_z1':tot_lin_pre_k3_z1_ll[4],
                'tot_lin_pre_h5_k1_z2':tot_lin_pre_k1_z2_ll[4],
                'tot_lin_pre_h5_k2_z2':tot_lin_pre_k2_z2_ll[4],
                'tot_lin_pre_h5_k3_z2':tot_lin_pre_k3_z2_ll[4],
                'tot_lin_pre_h5_k1_z3':tot_lin_pre_k1_z3_ll[4],
                'tot_lin_pre_h5_k2_z3':tot_lin_pre_k2_z3_ll[4],
                'tot_lin_pre_h5_k3_z3':tot_lin_pre_k3_z3_ll[4],
                'tot_lin_pre_h5_k1_z4':tot_lin_pre_k1_z4_ll[4],
                'tot_lin_pre_h5_k2_z4':tot_lin_pre_k2_z4_ll[4],
                'tot_lin_pre_h5_k3_z4':tot_lin_pre_k3_z4_ll[4],
                'tot_lin_pre_h5_k1_z5':tot_lin_pre_k1_z5_ll[4],
                'tot_lin_pre_h5_k2_z5':tot_lin_pre_k2_z5_ll[4],
                'tot_lin_pre_h5_k3_z5':tot_lin_pre_k3_z5_ll[4],
                'tot_lin_pre_h5_k1_z6':tot_lin_pre_k1_z6_ll[4],
                'tot_lin_pre_h5_k2_z6':tot_lin_pre_k2_z6_ll[4],
                'tot_lin_pre_h5_k3_z6':tot_lin_pre_k3_z6_ll[4],
                'tot_lin_pre_h6_k1_z1':tot_lin_pre_k1_z1_ll[5],
                'tot_lin_pre_h6_k2_z1':tot_lin_pre_k2_z1_ll[5],
                'tot_lin_pre_h6_k3_z1':tot_lin_pre_k3_z1_ll[5],
                'tot_lin_pre_h6_k1_z2':tot_lin_pre_k1_z2_ll[5],
                'tot_lin_pre_h6_k2_z2':tot_lin_pre_k2_z2_ll[5],
                'tot_lin_pre_h6_k3_z2':tot_lin_pre_k3_z2_ll[5],
                'tot_lin_pre_h6_k1_z3':tot_lin_pre_k1_z3_ll[5],
                'tot_lin_pre_h6_k2_z3':tot_lin_pre_k2_z3_ll[5],
                'tot_lin_pre_h6_k3_z3':tot_lin_pre_k3_z3_ll[5],
                'tot_lin_pre_h6_k1_z4':tot_lin_pre_k1_z4_ll[5],
                'tot_lin_pre_h6_k2_z4':tot_lin_pre_k2_z4_ll[5],
                'tot_lin_pre_h6_k3_z4':tot_lin_pre_k3_z4_ll[5],
                'tot_lin_pre_h6_k1_z5':tot_lin_pre_k1_z5_ll[5],
                'tot_lin_pre_h6_k2_z5':tot_lin_pre_k2_z5_ll[5],
                'tot_lin_pre_h6_k3_z5':tot_lin_pre_k3_z5_ll[5],
                'tot_lin_pre_h6_k1_z6':tot_lin_pre_k1_z6_ll[5],
                'tot_lin_pre_h6_k2_z6':tot_lin_pre_k2_z6_ll[5],
                'tot_lin_pre_h6_k3_z6':tot_lin_pre_k3_z6_ll[5]}
              
    #data_nl_pre = {'tot_tot_nl_pre':tot_tot_nl_pre,
    data_nl_pre = {'tot_nl_pre_h1_k1_z1':tot_nl_pre_k1_z1_ll[0],
                'tot_nl_pre_h1_k2_z1':tot_nl_pre_k2_z1_ll[0],
                'tot_nl_pre_h1_k3_z1':tot_nl_pre_k3_z1_ll[0],
                'tot_nl_pre_h1_k1_z2':tot_nl_pre_k1_z2_ll[0],
                'tot_nl_pre_h1_k2_z2':tot_nl_pre_k2_z2_ll[0],
                'tot_nl_pre_h1_k3_z2':tot_nl_pre_k3_z2_ll[0],
                'tot_nl_pre_h1_k1_z3':tot_nl_pre_k1_z3_ll[0],
                'tot_nl_pre_h1_k2_z3':tot_nl_pre_k2_z3_ll[0],
                'tot_nl_pre_h1_k3_z3':tot_nl_pre_k3_z3_ll[0],
                'tot_nl_pre_h1_k1_z4':tot_nl_pre_k1_z4_ll[0],
                'tot_nl_pre_h1_k2_z4':tot_nl_pre_k2_z4_ll[0],
                'tot_nl_pre_h1_k3_z4':tot_nl_pre_k3_z4_ll[0],
                'tot_nl_pre_h1_k1_z5':tot_nl_pre_k1_z5_ll[0],
                'tot_nl_pre_h1_k2_z5':tot_nl_pre_k2_z5_ll[0],
                'tot_nl_pre_h1_k3_z5':tot_nl_pre_k3_z5_ll[0],
                'tot_nl_pre_h1_k1_z6':tot_nl_pre_k1_z6_ll[0],
                'tot_nl_pre_h1_k2_z6':tot_nl_pre_k2_z6_ll[0],
                'tot_nl_pre_h1_k3_z6':tot_nl_pre_k3_z6_ll[0],
                'tot_nl_pre_h2_k1_z1':tot_nl_pre_k1_z1_ll[1],
                'tot_nl_pre_h2_k2_z1':tot_nl_pre_k2_z1_ll[1],
                'tot_nl_pre_h2_k3_z1':tot_nl_pre_k3_z1_ll[1],
                'tot_nl_pre_h2_k1_z2':tot_nl_pre_k1_z2_ll[1],
                'tot_nl_pre_h2_k2_z2':tot_nl_pre_k2_z2_ll[1],
                'tot_nl_pre_h2_k3_z2':tot_nl_pre_k3_z2_ll[1],
                'tot_nl_pre_h2_k1_z3':tot_nl_pre_k1_z3_ll[1],
                'tot_nl_pre_h2_k2_z3':tot_nl_pre_k2_z3_ll[1],
                'tot_nl_pre_h2_k3_z3':tot_nl_pre_k3_z3_ll[1],
                'tot_nl_pre_h2_k1_z4':tot_nl_pre_k1_z4_ll[1],
                'tot_nl_pre_h2_k2_z4':tot_nl_pre_k2_z4_ll[1],
                'tot_nl_pre_h2_k3_z4':tot_nl_pre_k3_z4_ll[1],
                'tot_nl_pre_h2_k1_z5':tot_nl_pre_k1_z5_ll[1],
                'tot_nl_pre_h2_k2_z5':tot_nl_pre_k2_z5_ll[1],
                'tot_nl_pre_h2_k3_z5':tot_nl_pre_k3_z5_ll[1],
                'tot_nl_pre_h2_k1_z6':tot_nl_pre_k1_z6_ll[1],
                'tot_nl_pre_h2_k2_z6':tot_nl_pre_k2_z6_ll[1],
                'tot_nl_pre_h2_k3_z6':tot_nl_pre_k3_z6_ll[1],
                'tot_nl_pre_h3_k1_z1':tot_nl_pre_k1_z1_ll[2],
                'tot_nl_pre_h3_k2_z1':tot_nl_pre_k2_z1_ll[2],
                'tot_nl_pre_h3_k3_z1':tot_nl_pre_k3_z1_ll[2],
                'tot_nl_pre_h3_k1_z2':tot_nl_pre_k1_z2_ll[2],
                'tot_nl_pre_h3_k2_z2':tot_nl_pre_k2_z2_ll[2],
                'tot_nl_pre_h3_k3_z2':tot_nl_pre_k3_z2_ll[2],
                'tot_nl_pre_h3_k1_z3':tot_nl_pre_k1_z3_ll[2],
                'tot_nl_pre_h3_k2_z3':tot_nl_pre_k2_z3_ll[2],
                'tot_nl_pre_h3_k3_z3':tot_nl_pre_k3_z3_ll[2],
                'tot_nl_pre_h3_k1_z4':tot_nl_pre_k1_z4_ll[2],
                'tot_nl_pre_h3_k2_z4':tot_nl_pre_k2_z4_ll[2],
                'tot_nl_pre_h3_k3_z4':tot_nl_pre_k3_z4_ll[2],
                'tot_nl_pre_h3_k1_z5':tot_nl_pre_k1_z5_ll[2],
                'tot_nl_pre_h3_k2_z5':tot_nl_pre_k2_z5_ll[2],
                'tot_nl_pre_h3_k3_z5':tot_nl_pre_k3_z5_ll[2],
                'tot_nl_pre_h3_k1_z6':tot_nl_pre_k1_z6_ll[2],
                'tot_nl_pre_h3_k2_z6':tot_nl_pre_k2_z6_ll[2],
                'tot_nl_pre_h3_k3_z6':tot_nl_pre_k3_z6_ll[2],
                'tot_nl_pre_h4_k1_z1':tot_nl_pre_k1_z1_ll[3],
                'tot_nl_pre_h4_k2_z1':tot_nl_pre_k2_z1_ll[3],
                'tot_nl_pre_h4_k3_z1':tot_nl_pre_k3_z1_ll[3],
                'tot_nl_pre_h4_k1_z2':tot_nl_pre_k1_z2_ll[3],
                'tot_nl_pre_h4_k2_z2':tot_nl_pre_k2_z2_ll[3],
                'tot_nl_pre_h4_k3_z2':tot_nl_pre_k3_z2_ll[3],
                'tot_nl_pre_h4_k1_z3':tot_nl_pre_k1_z3_ll[3],
                'tot_nl_pre_h4_k2_z3':tot_nl_pre_k2_z3_ll[3],
                'tot_nl_pre_h4_k3_z3':tot_nl_pre_k3_z3_ll[3],
                'tot_nl_pre_h4_k1_z4':tot_nl_pre_k1_z4_ll[3],
                'tot_nl_pre_h4_k2_z4':tot_nl_pre_k2_z4_ll[3],
                'tot_nl_pre_h4_k3_z4':tot_nl_pre_k3_z4_ll[3],
                'tot_nl_pre_h4_k1_z5':tot_nl_pre_k1_z5_ll[3],
                'tot_nl_pre_h4_k2_z5':tot_nl_pre_k2_z5_ll[3],
                'tot_nl_pre_h4_k3_z5':tot_nl_pre_k3_z5_ll[3],
                'tot_nl_pre_h4_k1_z6':tot_nl_pre_k1_z6_ll[3],
                'tot_nl_pre_h4_k2_z6':tot_nl_pre_k2_z6_ll[3],
                'tot_nl_pre_h4_k3_z6':tot_nl_pre_k3_z6_ll[3],
                'tot_nl_pre_h5_k1_z1':tot_nl_pre_k1_z1_ll[4],
                'tot_nl_pre_h5_k2_z1':tot_nl_pre_k2_z1_ll[4],
                'tot_nl_pre_h5_k3_z1':tot_nl_pre_k3_z1_ll[4],
                'tot_nl_pre_h5_k1_z2':tot_nl_pre_k1_z2_ll[4],
                'tot_nl_pre_h5_k2_z2':tot_nl_pre_k2_z2_ll[4],
                'tot_nl_pre_h5_k3_z2':tot_nl_pre_k3_z2_ll[4],
                'tot_nl_pre_h5_k1_z3':tot_nl_pre_k1_z3_ll[4],
                'tot_nl_pre_h5_k2_z3':tot_nl_pre_k2_z3_ll[4],
                'tot_nl_pre_h5_k3_z3':tot_nl_pre_k3_z3_ll[4],
                'tot_nl_pre_h5_k1_z4':tot_nl_pre_k1_z4_ll[4],
                'tot_nl_pre_h5_k2_z4':tot_nl_pre_k2_z4_ll[4],
                'tot_nl_pre_h5_k3_z4':tot_nl_pre_k3_z4_ll[4],
                'tot_nl_pre_h5_k1_z5':tot_nl_pre_k1_z5_ll[4],
                'tot_nl_pre_h5_k2_z5':tot_nl_pre_k2_z5_ll[4],
                'tot_nl_pre_h5_k3_z5':tot_nl_pre_k3_z5_ll[4],
                'tot_nl_pre_h5_k1_z6':tot_nl_pre_k1_z6_ll[4],
                'tot_nl_pre_h5_k2_z6':tot_nl_pre_k2_z6_ll[4],
                'tot_nl_pre_h5_k3_z6':tot_nl_pre_k3_z6_ll[4],
                'tot_nl_pre_h6_k1_z1':tot_nl_pre_k1_z1_ll[5],
                'tot_nl_pre_h6_k2_z1':tot_nl_pre_k2_z1_ll[5],
                'tot_nl_pre_h6_k3_z1':tot_nl_pre_k3_z1_ll[5],
                'tot_nl_pre_h6_k1_z2':tot_nl_pre_k1_z2_ll[5],
                'tot_nl_pre_h6_k2_z2':tot_nl_pre_k2_z2_ll[5],
                'tot_nl_pre_h6_k3_z2':tot_nl_pre_k3_z2_ll[5],
                'tot_nl_pre_h6_k1_z3':tot_nl_pre_k1_z3_ll[5],
                'tot_nl_pre_h6_k2_z3':tot_nl_pre_k2_z3_ll[5],
                'tot_nl_pre_h6_k3_z3':tot_nl_pre_k3_z3_ll[5],
                'tot_nl_pre_h6_k1_z4':tot_nl_pre_k1_z4_ll[5],
                'tot_nl_pre_h6_k2_z4':tot_nl_pre_k2_z4_ll[5],
                'tot_nl_pre_h6_k3_z4':tot_nl_pre_k3_z4_ll[5],
                'tot_nl_pre_h6_k1_z5':tot_nl_pre_k1_z5_ll[5],
                'tot_nl_pre_h6_k2_z5':tot_nl_pre_k2_z5_ll[5],
                'tot_nl_pre_h6_k3_z5':tot_nl_pre_k3_z5_ll[5],
                'tot_nl_pre_h6_k1_z6':tot_nl_pre_k1_z6_ll[5],
                'tot_nl_pre_h6_k2_z6':tot_nl_pre_k2_z6_ll[5],
                'tot_nl_pre_h6_k3_z6':tot_nl_pre_k3_z6_ll[5]}
    source_lin = ColumnDataSource(data=data_lin)
    source_nl = ColumnDataSource(data=data_nl)
    source_lin_pre = ColumnDataSource(data=data_lin_pre)
    source_nl_pre = ColumnDataSource(data=data_nl_pre)

    #Uses this dictionary, since if using x,y for fig.rect
    #That will lead to x, and y values changing all the time
    #So calling the dictionary value is better and won't fuck up your plots
    source_data = ColumnDataSource(data={'tot_tot_data':tot_tot_lin[100:200], 'h_arr':h_arr, 
                               'Omega_b_arr':Omega_b_arr, 'Omega_cdm_arr':Omega_cdm_arr,
                               'A_s_arr':A_s_arr, 'n_s_arr':n_s_arr, 'trial_arr':trial_arr})
    #Bokeh, so I have to individually plot each one first

    #initialize the color values, this is Gn To Red
    #colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    #colors = ['#fff5ee', '#ffe4e1', '#ecc3bf', '#ffc1c1', '#ffa07a', '#ff7f50', '#ff5333', '#ff2400', '#cc1100']

    #This one goes from some really light yellow thing (fff5ee) to Red
    colors = ['#fff5ee', '#ffe4e1', '#ffc1c1', '#eeb4b4', '#f08080', '#ee6363', '#d44942', '#cd0000', '#ff0000']
    #Mapper corresponding to the tot_tot_data
    mapper = LinearColorMapper(palette=colors, low=0, high=1000)

    #Create hover tool, I have to declare multiple instances of this
    hover1 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])

    hover2 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover3 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover4 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover5 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover6 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover7 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover8 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover9 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])
    
    hover10 = HoverTool(tooltips=[
    ('index', '$index'),
    ('(x,y,)', '($x, $y)'),
    ('Failure', '@tot_tot_data')])

    #What tools do I want
    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'
    #Makes the plot
    s1 = figure(plot_width=300, plot_height=300,tools=[hover1, TapTool()])

    s1.grid.grid_line_color = None
    #Plots the rectangles
    s1_rect = s1.rect('h_arr', 'Omega_b_arr',width=0.025, height=0.0017, alpha=0.8, source=source_data,fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s1.yaxis.axis_label = u'\u03A9_b'
    
    s2 = figure(plot_width=300, plot_height=300, tools=[hover2, TapTool()])
    s2.grid.grid_line_color=None
    s2_rect = s2.rect('h_arr', 'Omega_cdm_arr', width=0.025, height=0.017, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s2.yaxis.axis_label = u'\u03A9_cdm' 

    s3 = figure(plot_width=300, plot_height=300, tools=[hover3, TapTool()])
    s3.grid.grid_line_color = None
    #Plots the rectangles
    s3_rect = s3.rect('Omega_b_arr', 'Omega_cdm_arr',width=0.0017, height=0.017, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    
    s4 = figure(plot_width=300, plot_height=300, tools=[hover4, TapTool()])
    s4.grid.grid_line_color = None
    #Plots the rectangles
    s4_rect = s4.rect('h_arr', 'A_s_arr',width=0.025, height=0.045e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s4.yaxis.axis_label = 'A_s' 

    s5 = figure(plot_width=300, plot_height=300, tools=[hover5, TapTool()])
    s5.grid.grid_line_color = None
    s5_rect = s5.rect('Omega_b_arr', 'A_s_arr',width=0.0017, height=0.045e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)

    s6 = figure(plot_width=300, plot_height=300, tools=[hover6, TapTool()])
    s6.grid.grid_line_color = None
    s6_rect = s6.rect('Omega_cdm_arr', 'A_s_arr',width=0.017, height=0.045e-9, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)

    s7 = figure(plot_width=300, plot_height=300, tools=[hover7, TapTool()])
    s7.grid.grid_line_color = None
    s7_rect = s7.rect('h_arr', 'n_s_arr',width=0.025, height=0.0034, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s7.yaxis.axis_label = 'n_s'
    s7.xaxis.axis_label = 'h'
   
    s8 = figure(plot_width=300, plot_height=300, tools=[hover8,TapTool()])
    s8.grid.grid_line_color = None
    s8_rect = s8.rect('Omega_b_arr', 'n_s_arr', width=0.0017, height=0.0034, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s8.xaxis.axis_label = u'\u03A9_b'

    s9 = figure(plot_width=300, plot_height=300, tools=[hover9, TapTool()])
    s9.grid.grid_line_color = None
    s9_rect = s9.rect('Omega_cdm_arr', 'n_s_arr', width=0.017, height=0.0034, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s9.xaxis.axis_label = u'\u03A9_cdm'

    s10 = figure(plot_width=300, plot_height=300,tools=[hover10, TapTool()])
    s10.grid.grid_line_color = None
    s10_rect = s10.rect('A_s_arr', 'n_s_arr', width=0.045e-9, height=0.0034, alpha=0.8, source=source_data, fill_color={'field':'tot_tot_data', 'transform':mapper}, line_color=None)
    s10.xaxis.axis_label = 'A_s'
   
    #Create glyphs for the highlighting portion, so that when it is tapped
    #the colors don't change

    selected = Rect(fill_color={'field':'tot_tot_data', 'transform':mapper}, fill_alpha=0.8, line_color=None)
    nonselected = Rect(fill_color={'field':'tot_tot_data', 'transform':mapper}, fill_alpha=0.8, line_color=None)

    s1_rect.selection_glyph = selected
    s1_rect.nonselection_glyph = nonselected

    s2_rect.selection_glyph = selected
    s2_rect.nonselection_glyph = nonselected

    s3_rect.selection_glyph = selected
    s3_rect.nonselection_glyph = nonselected

    s4_rect.selection_glyph = selected
    s4_rect.nonselection_glyph = nonselected

    s5_rect.selection_glyph = selected
    s5_rect.nonselection_glyph = nonselected
    
    s6_rect.selection_glyph = selected
    s6_rect.nonselection_glyph = nonselected

    s7_rect.selection_glyph = selected
    s7_rect.nonselection_glyph = nonselected

    s8_rect.selection_glyph = selected
    s8_rect.nonselection_glyph = nonselected

    s9_rect.selection_glyph = selected
    s9_rect.nonselection_glyph = nonselected

    s10_rect.selection_glyph = selected
    s10_rect.nonselection_glyph = nonselected
    #Creates the color bar and adds it to the right side of the big plot
    
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='12pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))

    s_color = figure()
    #Since this basically creates another plot, we want to remove it
    #That's what the next couple of lines does
    s_color.grid.grid_line_color = None
    s_color.axis.axis_line_color = None
    s_color.add_layout(color_bar, 'left')
    s_color.toolbar.logo = None
    s_color.toolbar_location = None


    #Creates the gridplot to be reminscient of a corner plot
    plot = gridplot([[s1, None, None, None], [s2, s3, None, None], [s4,s5,s6, None], [s7,s8,s9,s10]])

    #Code to be utilized by the JavaScript in the interface
    code_sliders="""

    // Get the value from our threshold slider
    var thres = thres_slider.value;
    console.log(thres);

    //Get the range of our z_Slider
    var z = z_slider.range;
    var start = z_slider.range[0];
    var end = z_slider.range[1];
    console.log(start);
    console.log(end);

    
    //Get the mode in the dropdown
    var mode_selected = dropdown.value;

    //All of our data
    var tot_data = source_data.data;
    var tot_lin = js_lin.data;
    var tot_nl = js_nl.data;
    var tot_lin_pre = js_lin_pre.data;
    var tot_nl_pre = js_nl_pre.data;
    var sum = 0;
    console.log(mode_selected);

    //Daa from the checkbox group
    var k_check = k_checkbox.active;
    console.log(k_check);
    
    if (k_check != []) {
        var k_check_start = k_checkbox.active[0];
        var k_check_end = k_checkbox.active[k_check.length - 1];


        thres_string = String(thres)
        if (mode_selected == "Linear") {
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j*2)+1);
                    for (var l = k_check_start + 1; l<= k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_lin['tot_lin_h' + thres_string + '_k' + k_string + '_z' + z_string][i];
                    } // k_range

                } // z_value

                tot_data['tot_tot_data'][i] = sum;
            } // sum
        }

        if (mode_selected == "Non-Linear") {
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j * 2)+1);
                    for (var l = k_check_start + 1; l<=k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_nl['tot_nl_h' + thres_string + '_k' + k_string + '_z' + z_string][i];
                    } // k_range
                } // z_value

                tot_data['tot_tot_data'][i] = sum;
                
            } // sum
        }

        if (mode_selected == "Linear, Precision"){
            
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j * 2)+1);
                    for (var l = k_check_start + 1; l<=k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_lin_pre['tot_lin_pre_h' + thres_string + '_k' + k_string + '_z' + z_string][i];

                    } // k_range
                
                } // z_value

                tot_data['tot_tot_data'][i] = sum;
            } // sum
        }

        if (mode_selected == "Non-Linear, Precision"){
           
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j * 2)+1);
                    for (var l = k_check_start + 1; l<=k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_nl_pre['tot_nl_pre_h' + thres_string + '_k' + k_string + '_z' + z_string][i];
                    } // k_range
                
                } // z_value
                tot_data['tot_tot_data'][i] = sum;
            } // sum
        }
    } //else statement
    console.log(tot_data['tot_tot_data']);
    source_data.trigger('change');

    """

    callback_sliders = CustomJS(args=dict(source_data=source_data, js_lin=source_lin, js_nl=source_nl, js_lin_pre=source_lin_pre, js_nl_pre=source_nl_pre), code=code_sliders)
    
    #Creates the selection menu for the select
    selection_men = ['Linear', 'Non-Linear', 'Linear, Precision', 'Non-Linear, Precision']
    dropdown = Select(title='Mode', value=selection_men[0], options=selection_men, callback=callback_sliders)

    #Create the RangeSlider for the z values
    z_slider = RangeSlider(start=0, end=2.5, range=(0,2.5), step=0.5, title='Range of z values', callback=callback_sliders)
    
    #Create the slider for the threshold
    thres_slider = Slider(start=1, end=6, value=2, step=1, title='Threshold', callback=callback_sliders)


    #Create a checkbox group for the k ranges
    k_checkbox = CheckboxGroup(labels=[u'Ultra-Large Scales, 10\u207B\u2074 <= k <= 10\u207B\u00B2', u'Linear Scales, 10\u207B\u00B2 <= k <= 10\u207B\u00B9', u'Quasi-Linear Scales, 10\u207B\u00B9 <= k <= 1'], active=[0,1,2], callback=callback_sliders)
    
    callback_sliders.args['z_slider'] = z_slider
    callback_sliders.args['dropdown'] = dropdown
    callback_sliders.args['thres_slider'] = thres_slider
    callback_sliders.args['k_checkbox'] = k_checkbox
    
    #Make it open a new URL on tap
    #Bokeh is again a bitch, so we gotta initiate multiple instances
    taptool = s1.select(type=TapTool)
    code_tap="""
        //Get the value 'Tapped'
        var index_selected=source.selected['1d'].indices[0];
        console.log(index_selected);
        //Get the mode in the dropdown
        var mode_selected = dropdown.value;
        console.log(mode_selected);
        //Initialize the starting URL
        var url = 'http://127.0.0.1:5000/'

        if (mode_selected == "Linear") {
        var url_mode = 'lin/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Non-Linear") {
        var url_mode = 'nl/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Linear, Precision"){
        var url_mode = 'lin_pre/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Non-Linear, Precision"){
        var url_mode = 'nl_pre/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }
    """


        
    taptool.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))
    
    taptool2 = s2.select(type=TapTool)
    taptool2.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool3 = s3.select(type=TapTool)
    taptool3.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool4 = s4.select(type=TapTool)
    taptool4.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool5 = s5.select(type=TapTool)
    taptool5.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool6 = s6.select(type=TapTool)
    taptool6.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool7 = s7.select(type=TapTool)
    taptool7.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool8 = s8.select(type=TapTool)
    taptool8.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool9 = s9.select(type=TapTool)
    taptool9.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool10 = s10.select(type=TapTool)
    taptool10.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    
    l = layout([[WidgetBox(thres_slider),],[WidgetBox(dropdown),],[WidgetBox(z_slider),], [WidgetBox(k_checkbox),], [plot,s_color]])
    script, div_dict = components(l)
    print div_dict
    #print div_dict
    return render_template('homepage.html', script=script, div=div_dict)
                           #feature_names=feature_names, current_feature_name=current_feature_name)


#Index page 
@app.route('/lin/')
def lin():
    index = request.args.get('index')
    if index == None:
        index = '0'
    i = int(index)
    # Create the plot
        # load the data
    i = int(index)

    z_vals = ['1', '2', '3', '4', '5', '6']
    p = figure(toolbar_location="right", title = "CCL vs CLASS mPk, Linear", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "Discrepancy mPk, Linear", x_axis_type = "log", y_axis_type = "log",
         tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")
    
    #Load the parameter valus
    data = np.loadtxt('../data/par_stan1.csv', skiprows = 1)

    index = float(data[i,0])
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])

    for j, color in zip(z_vals, Spectral6):
        z_act = (float(j) - 1) / 2
        z_path = 'z%s_pk.dat' %j
        ccl_path = '../CCL/data_files/lhs_mpk_lin_%05d' % i 
        class_path = '../class/output/lin/lhs_lin_%05d' %i
        ccl_path += z_path
        class_path += z_path

        cclData = np.loadtxt(ccl_path,  skiprows = 1)
        cclK = cclData[:, 0]
        cclPk = cclData[:, 1]

        classData = np.loadtxt(class_path, skiprows = 4);
        classKLin = classData[:, 0]
        classPLin = classData[:, 1]

        #Multiply by factors
        #multiply k by some factor of h, CLASS and CCL use different units, ugh
        
        classKLin *= h
        classPLin /= h**3

        # create a plot and style its properties
        
        p.outline_line_color = None
        p.grid.grid_line_color = None

        p2.outline_line_color = None
        p2.grid.grid_line_color = None

        # plot the data
        #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
        p.line(cclK, cclPk, line_width = 2, color=color, legend='ccl data, z=%3.1f' %z_act)
        p.circle(cclK, cclPk, size = 5, color=color, legend = "ccl data, z=%3.1f" %z_act)

        #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
        p.line(classKLin, classPLin, line_width = 2,color=color, line_dash='dashed', legend='class data, z=%3.1f' %z_act)
        p.square(classKLin, classPLin, size = 5, fill_alpha=0.8,color=color, legend = "class data, z=%3.1f" %z_act)

        # Set the x axis label
        # Set the y axis label
        p.yaxis.axis_label = 'Count (log)'
        comparisonValue = abs(cclPk - classPLin) / classPLin
        p2.line(classKLin, comparisonValue, line_width = 2,color=color, legend='z=%3.1f' %z_act)
        p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, color=color,size = 5, legend='z=%3.1f' %z_act)

    #Adds the interactive legend and the axes
    p.legend.click_policy='hide'
    p.legend.location = 'bottom_left'
    p.yaxis.axis_label = 'P(k)'
    p.xaxis.axis_label = 'k'


    p2.legend.click_policy='hide'
    p2.legend.location = 'bottom_left'
    p2.yaxis.axis_label = '(CCL - CLASS)/CLASS'
    p2.xaxis.axis_label = 'k'
    plot = gridplot([[p2, p]])

    #Also the number for failures can either include clustering regime only or not
    thres = 1.e-4 #Threshold for number of failures
    clustering_only = False #Only counts failures if inside the clustering regime

    ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
    ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
    lin_scale_min = 1e-2 #Min for the linear scales
    lin_scale_max = 1e-1 #Max for the linear scales
    quasi_scale_min = 1e-1 #Min for the quasi-lin scales
    quasi_scale_max = 1.0 #Max for the quasi-lin scales


    cluster_reg_min = 1e-2 #Min for the cluster regime
    cluster_reg_max = 0.2 # Max for the cluster regime

    #load the data


    #Create arrays that will be filled in the loop over trials
    #Total of the wights
    tot_tot_lin = []

    #Get the totals for different k_ranges
    #We have 3 k_ranges, denote by 1,2,3
    #1 = Ultra Large Scales
    #2 = Linear scales
    #3 = Nonlinear scales


    ###########################
    #                         #
    #GETTING THE SUMMARY STATS#
    #                         #
    ###########################
    #for i in range(len(trial_arr)):
    print("\n\ni is ", i)
    print("\n\nin summary statistic plot")

    trial = data[i,0]
    print ('Performing trial %05d' %trial)

    z_vals = ['1', '2', '3', '4', '5', '6']
    #Gonna generate an array of arrays, with each row corresponding to a different z value
    #Each columns will correspond to a different bins of k_values
    tot_lin = []

    #For list of lists
    tot_lin_ll = []

    for j in range(len(z_vals)):
        z_val = z_vals[j]
        z_path ='_z%s.dat' %z_val
        print ('Performing z_val = ', z_val)

        #For ease in iterating over different z values we use string manipulation
        stats_lin_path = '../stats/lhs_mpk_err_lin_%05d' %trial
#stats_lin_path = '../../stats/lhs/lin/non_pre/lhs_mpk_err_lin_%05d' %trial

        #Adds the z_path
        stats_lin_path += z_path

        #Calls the data
        stats_lin_data = np.loadtxt(stats_lin_path, skiprows=1)

        stats_lin_k = stats_lin_data[:,0]
        stats_lin_err = stats_lin_data[:,1]

        #Create arrays that will be used to fill the complete summary arrays
        tot_lin_z = []

        #For list of lists
        tot_lin_z_ll = []

        #We perform a loop that looks into the bins for k
        #Doing this for lin
        #Much easier than doing a for loop because of list comprehension ALSO FASTER
        tot_ultrasc = 0 #initialize value for ultra large scales
        tot_linsc = 0 #initialize for lin scales
        tot_quasisc = 0 #initialize for quasi lin scales

        #k has to fall in the proper bins
        aux_k_ultra = (stats_lin_k >= ultra_scale_min) & (stats_lin_k < ultra_scale_max)
        aux_k_lin = (stats_lin_k >= lin_scale_min) & (stats_lin_k < lin_scale_max)
        aux_k_quasi = (stats_lin_k >= quasi_scale_min) & (stats_lin_k <= quasi_scale_max)

        #Looks at only the regime where clustering affects it
        if clustering_only == True:
            aux_cluster_ultra = (stats_lin_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_k[aux_k_ultra] < cluster_reg_max)
            aux_cluster_lin = (stats_lin_k[aux_k_lin] > cluster_reg_min) & (stats_lin_k[aux_k_lin] < cluster_reg_max)
            aux_cluster_quasi = (stats_lin_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_k[aux_k_quasi] < cluster_reg_max)

           #Calculate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs((stats_lin_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
            w_lin = np.log10(np.abs((stats_lin_err[aux_k_lin])[aux_cluster_lin]) / thres)
            w_quasi = np.log10(np.abs((stats_lin_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            tot_ultrasc = np.sum(w_ultra)
            tot_linsc = np.sum(w_lin)
            tot_quasisc = np.sum(w_quasi)
        #calculates imprecision in any regime
        if clustering_only == False:
            #caluclate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs(stats_lin_err[aux_k_ultra]) / thres)
            w_lin = np.log10(np.abs(stats_lin_err[aux_k_lin]) / thres)
            w_quasi = np.log10(np.abs(stats_lin_err[aux_k_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            #calculate the totals
            tot_ultrasc = np.sum(w_ultra)
            tot_linsc = np.sum(w_lin)
            tot_quasisc = np.sum(w_quasi)


        #Append these values to our z summary stat
        #For list only
        tot_lin_z = np.append(tot_lin_z, tot_ultrasc)
        tot_lin_z = np.append(tot_lin_z, tot_ultrasc) # 2 bins
        tot_lin_z = np.append(tot_lin_z, tot_linsc)
        tot_lin_z = np.append(tot_lin_z, tot_quasisc)

        #For list of lists
        tot_lin_z_ll.append(tot_ultrasc)
        tot_lin_z_ll.append(tot_ultrasc) # 2 bins
        tot_lin_z_ll.append(tot_linsc)
        tot_lin_z_ll.append(tot_quasisc)

        #Append these values for the general z stat
        #For list only
        tot_lin = np.append(tot_lin, tot_lin_z)
        #For list of lists
        tot_lin_ll.append(tot_lin_z_ll)



	#Generate our z values for plotting
    z_actual = range(len(z_vals))
    z_arr = np.float_(np.asarray(z_actual))
    z_arr *= 0.5
    z = []
    z_ll = []	#Create a heat map, but makes it red, right now we just mark threshold on the heat map
    for j in range(len(z_actual)):
        z_full = np.full(len(tot_lin_ll[0]), z_arr[j])
        z = np.append(z,z_full)
        z_ll.append(z_full)

	#Generate an array of the midpoints of the bins
    ultra_scale_bin = (np.log10(ultra_scale_max) + np.log10(ultra_scale_min))/2
    ultra_scale_bin_1 = ultra_scale_bin - 0.5
    ultra_scale_bin_2 = ultra_scale_bin + 0.5
    lin_scale_bin = (np.log10(lin_scale_max) + np.log10(lin_scale_min))/2
    quasi_scale_bin = (np.log10(quasi_scale_max) + np.log10(quasi_scale_min))/2

    k_bin = [ultra_scale_bin_1, ultra_scale_bin_2, lin_scale_bin, quasi_scale_bin]
    k_list = k_bin * len(z_vals) 


	#Gonna try to plot it the pandas way
	#WORKS!!!! AND it fills the whole space. FUCKING LIT
    k_words = ['Ultra-large', 'Linear', 'Quasi Lin']
	#Use pandas to generate a data frame
    #df = pd.DataFrame(sum_lin_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])
    #print(sum_lin_z_ll)

    #print(sum_lin_z)
    #df = pd.DataFrame(tot_lin_ll, index=z_arr, columns=k_words)
    data_lin = {'tot_lin': tot_lin, 'z':z, 'k':k_list}
    source = ColumnDataSource(data=data_lin)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])

	#Trying to brute force colors for me
    colors = ['#fff5ee', '#ffe4e1', '#ffc1c1', '#eeb4b4', '#f08080', '#ee6363', '#d44942', '#cd0000', '#ff0000']
    mapper = LinearColorMapper(palette = colors, low = 0, high = 100)

    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'
    
    p_sum = figure(title = "Summary Statistic", toolbar_location = "above", tools=TOOLS)
        #tools = tools)

    p_sum.grid.grid_line_color = None
    p_sum.axis.axis_line_color = None
    p_sum.axis.major_tick_line_color = None
    p_sum.axis.major_label_text_font_size = "12pt"
    p_sum.axis.major_label_standoff = 0
    p_sum.xaxis.major_label_orientation = 0.5
    p_sum.rect('k', 'z', source = source, width = (1.0), height = (0.5), fill_color={'field': 'tot_lin', 'transform':mapper}, line_color= None)


    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='12pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))


    p_sum.add_layout(color_bar, 'right')
    p_sum.xaxis.axis_label = "log k"
    p_sum.yaxis.axis_label = "z"

    #Make a textarea, so that the html will print out a textbox of the parameter values

    id_val_string = 'Index = %s <br/>' %index
    h_string = 'h = %s <br/>' %h
    Omega_b_string = '&Omega;<sub>b</sub> = %s <br/>' %Omega_b
    Omega_cdm_string = '&Omega;<sub>cdm</sub> = %s <br/>' %Omega_cdm
    A_s_string = 'A<sub>s</sub> = %s <br/>' %A_s
    n_s_string = 'n<sub>s</sub> = %s <br/>' %n_s

    #Textbox html
    textbox = '<div class=\'boxed\'> Parameter values: <br/>' + id_val_string + h_string + Omega_b_string + Omega_cdm_string + A_s_string + n_s_string + '</div>'

    

    #Create a paragraph to tell the users what to do
    readme = Paragraph(text = """If you want to recreate these plots, look
    no further! Below is the .ini file for CLASS and the code used to run CCL
    on python. For the .ini file, save it under something like mytext.ini, then
    go to your folder with CLASS and simply run ./class myext.ini
    For the CCL one, make sure you have it installed then simply run in Python.
    When you plot these against each other make sure to multiply the CLASS values
    by proper factor of h, since CLASS units are proportional to factors of h
    """, width = 500)

    #Create preformatted text of the .ini file used and the code for CLASS and CCL
    with open('../class/ini_files/lhs_lin_%05d.ini' %i, 'r') as myfile:
        ini_text = myfile.read()
    class_pretext = PreText(text='CLASS .ini file \n' + ini_text)

    h_ccl = 'h = %s \n' %h
    Omega_b_ccl = 'Omega_b = %s \n' %Omega_b
    Omega_cdm_ccl = 'Omega_cdm = %s \n' %Omega_cdm
    A_s_ccl = 'A_s = %s \n' %A_s
    n_s_ccl = 'n_s = %s \n' %n_s

    index_ccl = 'index = %s \n' %index
    #Create a textbox that tells the parameters
    parameters = PreText(text="""Parameter values \n""" + index_ccl + h_ccl +
        Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl)

    #Create a textbox for CCL code
    ccl_pretext = PreText(text=
    """Code for CCL, just simply run in python
Make sure to have the CLASS k values, so it coincides properly
i.e. make sure the class_path_lin is correct

import numpy as np
import pyccl

""" + 
    h_ccl + Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl + 
    """
cosmo = pyccl.Cosmology(Omega_c=Omega_cdm, Omega_b=Omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
z_vals = ['1', '2', '3', '4', '5', '6']
for j in range(len(z_vals)):
    z_val = z_vals[j]
    class_path_lin = '/class/output/lin/lhs_lin_%s' %trial
    z_path = 'z%s_pk.dat' %z_val
    k_lin_data = np.loadtxt(class_path_lin, skiprows=4)
    k_lin = k_lin_data[:,0]
    k_lin *= h
    #Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
    z = j * 0.5
    a = 1. / (1. + z)
    #Matter power spectrum for lin
    pk_lin = pyccl.linear_matter_power(cosmo, k_lin, a)
    """, width=500)

    #ccl_pretext = 
    # Embed plot into HTML via Flask Render

    #Create whitespace to fill between class_pretext and ccl_pretext
    whitespace = PreText(text = """ """, width = 200)
    #l = layout([[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    l = layout([[p_sum, parameters,],[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    script, div = components(l)
    #print (script)
    #print(div)

    return render_template("lin.html", script=script, div=div)

@app.route('/nl/')
def nl():
    index = request.args.get('index')
    if index == None:
        index = '0'
    # Create the plot
        # load the data
    i = int(index)

    z_vals = ['1', '2', '3', '4', '5', '6']
    p = figure(toolbar_location="right", title = "CCL vs CLASS mPk, Non-Linear", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "Discrepancy mPk, Non-Linear", x_axis_type = "log", y_axis_type = "log",
         tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    #load the parameter values
    data = np.loadtxt('../data/par_stan1.csv', skiprows = 1)

    index = float(data[i,0])
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])

    for j,color in zip(z_vals, Spectral6):
        z_act = (float(j) - 1) / 2
        z_path = 'z%s_pk.dat' %j
        z_nl_path = 'z%s_pk_nl.dat' %j
        ccl_path = '../CCL/data_files/lhs_mpk_nl_%05d' % i 
        class_path = '../class/output/nonlin/lhs_nonlin_%05d' %i
        ccl_path += z_path
        class_path += z_nl_path

        cclData = np.loadtxt(ccl_path,  skiprows = 1)
        cclK = cclData[:, 0]
        cclPk = cclData[:, 1]
        
        classData = np.loadtxt(class_path, skiprows = 4);
        classKLin = classData[:, 0]
        classPLin = classData[:, 1]

        #Multiply by factors
        #multiply k by some factor of h, CLASS and CCL use different units, ugh
        
        classKLin *= h
        classPLin /= h**3

        # create a plot and style its properties
        
        p.outline_line_color = None
        p.grid.grid_line_color = None

        p2.outline_line_color = None
        p2.grid.grid_line_color = None

        # plot the data
        #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
        p.line(cclK, cclPk, line_width = 2, color=color, legend='ccl data, z=%3.1f' %z_act)
        p.circle(cclK, cclPk, size = 5, color=color, legend = "ccl data, z=%3.1f" %z_act)

        #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
        p.line(classKLin, classPLin, line_width = 2,color=color, line_dash='dashed', legend='class data, z=%3.1f' %z_act)
        p.square(classKLin, classPLin, size = 5, fill_alpha=0.8,color=color, legend = "class data, z=%3.1f" %z_act)

        # Set the x axis label
        # Set the y axis label
        p.yaxis.axis_label = 'Count (log)'
        comparisonValue = abs(cclPk - classPLin) / classPLin
        p2.line(classKLin, comparisonValue, line_width = 2,color=color, legend='z=%3.1f' %z_act)
        p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, color=color,size = 5, legend='z=%3.1f' %z_act)

    #Adds the interactive legend and the axes labels
    p.legend.click_policy='hide'
    p.legend.location = 'bottom_left'
    p.yaxis.axis_label = 'P(k)'
    p.xaxis.axis_label = 'k'


    p2.legend.click_policy='hide'
    p2.legend.location = 'bottom_left'
    p2.yaxis.axis_label = '(CCL - CLASS)/CLASS'
    p2.xaxis.axis_label = 'k'
    #Make a textarea, so that the html will print out a textbox of the parameter values


#Also the number for failures can either include clustering regime only or not
    thres = 1.e-4 #Threshold for number of failures
    clustering_only = False #Only counts failures if inside the clustering regime

    ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
    ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
    lin_scale_min = 1e-2 #Min for the linear scales
    lin_scale_max = 1e-1 #Max for the linear scales
    quasi_scale_min = 1e-1 #Min for the quasi-lin scales
    quasi_scale_max = 1.0 #Max for the quasi-lin scales


    cluster_reg_min = 1e-2 #Min for the cluster regime
    cluster_reg_max = 0.2 # Max for the cluster regime

    #load the data


    #Create arrays that will be filled in the loop over trials
    tot_tot_nl = []

    #Get the totals for the different thresholds
    #For now, we'll denote it as 1,2,3,4,5,6
    #1 = 5e-5
    #2 = 1e-4
    #3 = 5e-4
    #4 = 1e-3
    #5 = 5e-3
    #6 = 1e-2

    #Get the totals for different k_ranges
    #We have 3 k_ranges, denote by 1,2,3
    #1 = Ultra Large Scales
    #2 = Linear scales
    #3 = Nonlinear scales


    ###########################
    #                         #
    #GETTING THE SUMMARY STATS#
    #                         #
    ###########################
    #for i in range(len(trial_arr)):
    print("\n\ni is ", i)
    print("\n\nin summary statistic plot")

    trial = data[i,0]
    print ('Performing trial %05d' %trial)

    z_vals = ['1', '2', '3', '4', '5', '6']

    print ('Performing this for nonlin')
    #Gonna generate an array of arrays, with each row corresponding to a different z value
    #Each columns will correspond to a different bins of k_values
    tot_nl = []

    #For list of lists
    tot_nl_ll = []

    for j in range(len(z_vals)):
        z_val = z_vals[j]
        z_path ='_z%s.dat' %z_val
        print ('Performing z_val = ', z_val)

        #For ease in iterating over different z values we use string manipulation
        #stats_nl_path = '../../stats/lhs/nl/non_pre/lhs_mpk_err_nl_%05d' %trial
        stats_nl_path = '../stats/lhs_mpk_err_nl_%05d' %trial

        #Adds the z_path
        stats_nl_path += z_path

        #Calls the data
        stats_nl_data = np.loadtxt(stats_nl_path, skiprows=1)

        stats_nl_k = stats_nl_data[:,0]
        stats_nl_err = stats_nl_data[:,1]

        #Create arrays that will be used to fill the complete summary arrays
        tot_nl_z = []

        #For list of lists
        tot_nl_z_ll = []

        #We perform a loop that looks into the bins for k
        #Doing this for lin
        #Much easier than doing a for loop because of list comprehension ALSO FASTER
        tot_ultra = 0 #initialize value for ultra large scales
        tot_lin = 0 #initialize for lin scales
        tot_quasi = 0 #initialize for quasi lin scales

        #k has to fall in the proper bins
        aux_k_ultra = (stats_nl_k >= ultra_scale_min) & (stats_nl_k < ultra_scale_max)
        aux_k_lin = (stats_nl_k >= lin_scale_min) & (stats_nl_k < lin_scale_max)
        aux_k_quasi = (stats_nl_k >= quasi_scale_min) & (stats_nl_k <= quasi_scale_max)

        #Looks at only the regime where clustering affects it
        if clustering_only == True:
            aux_cluster_ultra = (stats_nl_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_k[aux_k_ultra] < cluster_reg_max)
            aux_cluster_lin = (stats_nl_k[aux_k_lin] > cluster_reg_min) & (stats_nl_k[aux_k_lin] < cluster_reg_max)
            aux_cluster_quasi = (stats_nl_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_k[aux_k_quasi] < cluster_reg_max)

            #Calculate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs((stats_nl_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
            w_lin = np.log10(np.abs((stats_nl_err[aux_k_lin])[aux_cluster_lin]) / thres)
            w_quasi = np.log10(np.abs((stats_nl_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            tot_ultra = np.sum(w_ultra)
            tot_lin = np.sum(w_lin)
            tot_quasi = np.sum(w_quasi)
        #calculates imprecision in any regime
        if clustering_only == False:
            #caluclate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs(stats_nl_err[aux_k_ultra]) / thres)
            w_lin = np.log10(np.abs(stats_nl_err[aux_k_lin]) / thres)
            w_quasi = np.log10(np.abs(stats_nl_err[aux_k_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            #calculate the totals
            tot_ultra = np.sum(w_ultra)
            tot_lin = np.sum(w_lin)
            tot_quasi = np.sum(w_quasi)


        #Append these values to our z summary stat
        #For list only
        tot_nl_z = np.append(tot_nl_z, tot_ultra)
        tot_nl_z = np.append(tot_nl_z, tot_ultra) # 2 bins
        tot_nl_z = np.append(tot_nl_z, tot_lin)
        tot_nl_z = np.append(tot_nl_z, tot_quasi)

        #For list of lists
        tot_nl_z_ll.append(tot_ultra)
        tot_nl_z_ll.append(tot_ultra) # 2 bins
        tot_nl_z_ll.append(tot_lin)
        tot_nl_z_ll.append(tot_quasi)

        #Append these values for the general z stat
        #For list only
        tot_nl = np.append(tot_nl, tot_nl_z)
        #For list of lists
        tot_nl_ll.append(tot_nl_z_ll)


    tot_tot_nl = np.append(tot_tot_nl,np.sum(tot_nl))


	#Generate our z values for plotting
    z_actual = range(len(z_vals))
    z_arr = np.float_(np.asarray(z_actual))
    z_arr *= 0.5
    z = []
    z_ll = []	#Create a heat map, but makes it red, right now we just mark threshold on the heat map
    for j in range(len(z_actual)):
        z_full = np.full(len(tot_nl_ll[0]), z_arr[j])
        z = np.append(z,z_full)
        z_ll.append(z_full)

	#Generate an array of the midpoints of the bins
    
    ultra_scale_bin = (np.log10(ultra_scale_max) + np.log10(ultra_scale_min))/2
    ultra_scale_bin_1 = ultra_scale_bin - 0.5
    ultra_scale_bin_2 = ultra_scale_bin + 0.5
    lin_scale_bin = (np.log10(lin_scale_max) + np.log10(lin_scale_min))/2
    quasi_scale_bin = (np.log10(quasi_scale_max) + np.log10(quasi_scale_min))/2

    k_bin = [ultra_scale_bin_1, ultra_scale_bin_2, lin_scale_bin, quasi_scale_bin]
    k_list = k_bin * len(z_vals) 

	#Gonna try to plot it the pandas way
	#WORKS!!!! AND it fills the whole space. FUCKING LIT
    k_words = ['Ultra-large', 'Linear', 'Quasi Lin']
	#Use pandas to generate a data frame
    #df = pd.DataFrame(sum_lin_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])
    #print(sum_lin_z_ll)

    #print(sum_lin_z)
    #df = pd.DataFrame(tot_nl_ll, index=z_arr, columns=k_words)
    data_nl = {'tot_nl': tot_nl, 'z':z, 'k':k_list}
    source = ColumnDataSource(data=data_nl)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])

	#Trying to brute force colors for me
    colors = ['#fff5ee', '#ffe4e1', '#ffc1c1', '#eeb4b4', '#f08080', '#ee6363', '#d44942', '#cd0000', '#ff0000']
    mapper = LinearColorMapper(palette = colors, low = 0, high = 100)
    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'

    p_sum = figure(title = "Summary Statistic", toolbar_location = "above", tools = TOOLS)
        #tools = TOOLS)

    p_sum.grid.grid_line_color = None
    p_sum.axis.axis_line_color = None
    p_sum.axis.major_tick_line_color = None
    p_sum.axis.major_label_text_font_size = "12pt"
    p_sum.axis.major_label_standoff = 0
    p_sum.xaxis.major_label_orientation = 0.5
    p_sum.rect('k', 'z', source = source, width = (1.0), height = (0.5), fill_color={'field': 'tot_nl', 'transform':mapper}, line_color= None)


    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='12pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))


    p_sum.add_layout(color_bar, 'right')
    p_sum.xaxis.axis_label = "log k"
    p_sum.yaxis.axis_label = "z"

    id_val_string = 'Index = %s <br/>' %index
    h_string = 'h = %s <br/>' %h
    Omega_b_string = '&Omega;<sub>b</sub> = %s <br/>' %Omega_b
    Omega_cdm_string = '&Omega;<sub>cdm</sub> = %s <br/>' %Omega_cdm
    A_s_string = 'A<sub>s</sub> = %s <br/>' %A_s
    n_s_string = 'n<sub>s</sub> = %s <br/>' %n_s

    #Textbox html code
    textbox = '<div class=\'boxed\'> Parameter values: <br/>' + id_val_string + h_string + Omega_b_string + Omega_cdm_string + A_s_string + n_s_string + '</div>'
    
    #Create a paragraph to tell the users what to do
    readme = Paragraph(text = """If you want to recreate these plots, look
    no further! Below is the .ini file for CLASS and the code used to run CCL
    on python. For the .ini file, save it under something like mytext.ini, then
    go to your folder with CLASS and simply run ./class myext.ini
    For the CCL one, make sure you have it installed then simply run in Python.
    When you plot these against each other make sure to multiply the CLASS values
    by proper factor of h, since CLASS units are proportional to factors of h
    """, width = 500)

    #Create preformatted text of the .ini file used and the code for CLASS and CCL
    with open('../class/ini_files/lhs_nonlin_%05d.ini' %i, 'r') as myfile:
        ini_text = myfile.read()
    class_pretext = PreText(text='CLASS .ini file \n' + ini_text)

    index_ccl = 'index = %s \n' %index
    h_ccl = 'h = %s \n' %h
    Omega_b_ccl = 'Omega_b = %s \n' %Omega_b
    Omega_cdm_ccl = 'Omega_cdm = %s \n' %Omega_cdm
    A_s_ccl = 'A_s = %s \n' %A_s
    n_s_ccl = 'n_s = %s \n' %n_s

    #Create a textbox that tells the parameters
    parameters = PreText(text="""Parameter values \n""" + index_ccl + h_ccl +
        Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl)

    #Create one for the CCL code used
    ccl_pretext = PreText(text=
    """Code for CCL, just simply run in python
Make sure to have the CLASS k values, so it coincides properly
i.e. make sure the class_path_nl is correct

import numpy as np
import pyccl

""" + 
    h_ccl + Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl + 
    """
cosmo = pyccl.Cosmology(Omega_c=Omega_cdm, Omega_b=Omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
z_vals = ['1', '2', '3', '4', '5', '6']
for j in range(len(z_vals)):
    z_val = z_vals[j]
    class_path_nl = '/class/output/nonlin/lhs_nonlin_%s' %trial
    z_path = 'z%s_pk_nl.dat' %z_val
    k_nl_data = np.loadtxt(class_path_nl, skiprows=4)
    k_nl = k_nl_data[:,0]
    k_nl *= h
    #Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
    z = j * 0.5
    a = 1. / (1. + z)
    #Matter power spectrum for nonlin
    pk_nl = pyccl.nonlinear_matter_power(cosmo, k_nl, a)
    """, width=500)

    #ccl_pretext = 
    # Embed plot into HTML via Flask Render

    #Create whitespace to fill between class_pretext and ccl_pretext
    whitespace = PreText(text = """ """, width = 200)
    #l = layout([[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    l = layout([[p_sum, parameters],[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    # Embed plot into HTML via Flask Render

    script, div = components(l)
    #print (script)
    #print(div)
    #print(div)

    return render_template("nl.html", script=script, div=div)


@app.route('/lin_pre/')
def lin_pre():
    index = request.args.get('index')
    if index == None:
        index = '0'
    i = int(index)
    # Create the plot
    #load the data
    z_vals = ['1', '2', '3', '4', '5', '6']
    p = figure(toolbar_location="right", title = "CCL vs CLASS mPk, Linear Precision", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "Discrepancy mPk, Linear Precision", x_axis_type = "log", y_axis_type = "log",
         tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    #load the parameter values
    data = np.loadtxt('../data/par_stan1.csv', skiprows = 1)
   
    index = float(data[i,0])
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])
    for j, color in zip(z_vals, Spectral6):
        z_act = (float(j) - 1) / 2
        z_path = 'z%s_pk.dat' %j
        ccl_path = '../CCL/data_files/lhs_mpk_lin_pk_%05d' % i 
        class_path = '../class/output/lin/lhs_lin_pk_%05d' %i
        ccl_path += z_path
        class_path += z_path

        cclData = np.loadtxt(ccl_path,  skiprows = 1)
        cclK = cclData[:, 0]
        cclPk = cclData[:, 1]

        classData = np.loadtxt(class_path, skiprows = 4);
        classKLin = classData[:, 0]
        classPLin = classData[:, 1]

        #Multiply by factors
        #multiply k by some factor of h, CLASS and CCL use different units, ugh

        classKLin *= h
        classPLin /= h**3

        # create a plot and style its properties
        
        p.outline_line_color = None
        p.grid.grid_line_color = None

        p2.outline_line_color = None
        p2.grid.grid_line_color = None

        # plot the data
        #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
        p.line(cclK, cclPk, line_width = 2, color=color, legend='ccl data, z=%3.1f' %z_act)
        p.circle(cclK, cclPk, size = 5, color=color, legend = "ccl data, z=%3.1f" %z_act)

        #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
        p.line(classKLin, classPLin, line_width = 2,color=color, line_dash='dashed', legend='class data, z=%3.1f' %z_act)
        p.square(classKLin, classPLin, size = 5, fill_alpha=0.8,color=color, legend = "class data, z=%3.1f" %z_act)

        # Set the x axis label
        # Set the y axis label
        p.yaxis.axis_label = 'Count (log)'
        comparisonValue = abs(cclPk - classPLin) / classPLin
        p2.line(classKLin, comparisonValue, line_width = 2,color=color, legend='z=%3.1f' %z_act)
        p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, color=color,size = 5, legend='z=%3.1f' %z_act)

    #Adds the interactive legend and the axes
    p.legend.click_policy='hide'
    p.legend.location = 'bottom_left'
    p.yaxis.axis_label = 'P(k)'
    p.xaxis.axis_label = 'k'


    p2.legend.click_policy='hide'
    p2.legend.location = 'bottom_left'
    p2.yaxis.axis_label = '(CCL - CLASS)/CLASS'
    p2.xaxis.axis_label = 'k'
    
    #Also the number for failures can either include clustering regime only or not
    thres = 1.e-4 #Threshold for number of failures
    clustering_only = False #Only counts failures if inside the clustering regime

    ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
    ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
    lin_scale_min = 1e-2 #Min for the linear scales
    lin_scale_max = 1e-1 #Max for the linear scales
    quasi_scale_min = 1e-1 #Min for the quasi-lin scales
    quasi_scale_max = 1.0 #Max for the quasi-lin scales


    cluster_reg_min = 1e-2 #Min for the cluster regime
    cluster_reg_max = 0.2 # Max for the cluster regime

    #load the data


    #Create arrays that will be filled in the loop over trials
    #Total of the wights
    tot_tot_lin_pre = []
    tot_tot_nl_pre = []

    #Get the totals for different k_ranges
    #We have 3 k_ranges, denote by 1,2,3
    #1 = Ultra Large Scales
    #2 = Linear scales
    #3 = Nonlinear scales


    ###########################
    #                         #
    #GETTING THE SUMMARY STATS#
    #                         #
    ###########################
    #for i in range(len(trial_arr)):
    trial = data[i,0]
    print ('Performing trial %05d' %trial)

    z_vals = ['1', '2', '3', '4', '5', '6']


    #Gonna generate an array of arrays, with each row corresponding to a different z value
    #Each columns will correspond to a different bins of k_values
    tot_lin_pre = []

    #For list of lists
    tot_lin_pre_ll = []



    for j in range(len(z_vals)):
        z_val = z_vals[j]
        z_path ='_z%s.dat' %z_val
        print ('Performing z_val = ', z_val)

        #For ease in iterating over different z values we use string manipulation
        #stats_lin_pre_path = '../../stats/lhs/lin/pre/lhs_mpk_err_lin_pk_%05d' %trial
        stats_lin_pre_path = '../stats/lhs_mpk_err_lin_pk_%05d' %trial

        #Adds the z_path
        stats_lin_pre_path += z_path

        #Calls the data
        stats_lin_pre_data = np.loadtxt(stats_lin_pre_path, skiprows=1)

        stats_lin_pre_k = stats_lin_pre_data[:,0]
        stats_lin_pre_err = stats_lin_pre_data[:,1]

        #Create arrays that will be used to fill the complete summary arrays
        tot_lin_pre_z = []

        #For list of lists
        tot_lin_pre_z_ll = []

        #We perform a loop that looks into the bins for k
        #Doing this for lin
        #Much easier than doing a for loop because of list comprehension ALSO FASTER
        tot_ultra = 0 #initialize value for ultra large scales
        tot_lin = 0 #initialize for lin scales
        tot_quasi = 0 #initialize for quasi lin scales

        #k has to fall in the proper bins
        aux_k_ultra = (stats_lin_pre_k >= ultra_scale_min) & (stats_lin_pre_k < ultra_scale_max)
        aux_k_lin = (stats_lin_pre_k >= lin_scale_min) & (stats_lin_pre_k < lin_scale_max)
        aux_k_quasi = (stats_lin_pre_k >= quasi_scale_min) & (stats_lin_pre_k <= quasi_scale_max)

        #Looks at only the regime where clustering affects it
        if clustering_only == True:
            aux_cluster_ultra = (stats_lin_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_pre_k[aux_k_ultra] < cluster_reg_max)
            aux_cluster_lin = (stats_lin_pre_k[aux_k_lin] > cluster_reg_min) & (stats_lin_pre_k[aux_k_lin] < cluster_reg_max)
            aux_cluster_quasi = (stats_lin_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_pre_k[aux_k_quasi] < cluster_reg_max)

            #Calculate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs((stats_lin_pre_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
            w_lin = np.log10(np.abs((stats_lin_pre_err[aux_k_lin])[aux_cluster_lin]) / thres)
            w_quasi = np.log10(np.abs((stats_lin_pre_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            tot_ultra = np.sum(w_ultra)
            tot_lin = np.sum(w_lin)
            tot_quasi = np.sum(w_quasi)
        #calculates imprecision in any regime
        if clustering_only == False:
            #caluclate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs(stats_lin_pre_err[aux_k_ultra]) / thres)
            w_lin = np.log10(np.abs(stats_lin_pre_err[aux_k_lin]) / thres)
            w_quasi = np.log10(np.abs(stats_lin_pre_err[aux_k_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            #calculate the totals
            tot_ultra = np.sum(w_ultra)
            tot_lin = np.sum(w_lin)
            tot_quasi = np.sum(w_quasi)


        #Append these values to our z summary stat
        #For list only
        tot_lin_pre_z = np.append(tot_lin_pre_z, tot_ultra)
        tot_lin_pre_z = np.append(tot_lin_pre_z, tot_ultra) # This is because we have 2 ultra_large bins
        tot_lin_pre_z = np.append(tot_lin_pre_z, tot_lin)
        tot_lin_pre_z = np.append(tot_lin_pre_z, tot_quasi)

        #For list of lists
        tot_lin_pre_z_ll.append(tot_ultra)
        tot_lin_pre_z_ll.append(tot_ultra) #This is because we have 2 ultra_large bins
        tot_lin_pre_z_ll.append(tot_lin)
        tot_lin_pre_z_ll.append(tot_quasi)

        #Append these values for the general z stat
        #For list only
        tot_lin_pre = np.append(tot_lin_pre, tot_lin_pre_z)
        #For list of lists
        tot_lin_pre_ll.append(tot_lin_pre_z_ll)

    tot_tot_lin_pre = np.append(tot_tot_lin_pre, np.sum(tot_lin_pre))



	#Generate our z values for plotting
    z_actual = range(len(z_vals))
    z_arr = np.float_(np.asarray(z_actual))
    z_arr *= 0.5
    z = []
    z_ll = []	#Create a heat map, but makes it red, right now we just mark threshold on the heat map
    for j in range(len(z_actual)):
        z_full = np.full(len(tot_lin_pre_ll[0]) , z_arr[j]) #The +1 is to make it 4 bins
        print z_full
        z = np.append(z,z_full)
        z_ll.append(z_full)

    
	#Generate an array of the midpoints of the bins
    #We have 2 ultra scale bins to make it evenly spaced out
    ultra_scale_bin = (np.log10(ultra_scale_max) + np.log10(ultra_scale_min))/2
    ultra_scale_bin_1 = ultra_scale_bin - 0.5
    ultra_scale_bin_2 = ultra_scale_bin + 0.5
    lin_scale_bin = (np.log10(lin_scale_max) + np.log10(lin_scale_min))/2
    quasi_scale_bin = (np.log10(quasi_scale_max) + np.log10(quasi_scale_min))/2

    k_bin = [ultra_scale_bin_1, ultra_scale_bin_2, lin_scale_bin, quasi_scale_bin]
    k_list = k_bin * len(z_vals) 
    #log_k_list = np.log10(k_list)

	#Gonna try to plot it the pandas way
	#WORKS!!!! AND it fills the whole space. FUCKING LIT
    k_words = ['Ultra-large', 'Linear', 'Quasi Lin']
	#Use pandas to generate a data frame
    #df = pd.DataFrame(sum_lin_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])
    #print(sum_lin_z_ll)

    #print(sum_lin_z)
    print len(tot_lin_pre), len(z), len(k_list)
    data_lin_pre = {'tot_lin_pre': tot_lin_pre, 'z':z, 'k':k_list}
    source = ColumnDataSource(data=data_lin_pre)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])

	#Trying to brute force colors for me
    colors = ['#fff5ee', '#ffe4e1', '#ffc1c1', '#eeb4b4', '#f08080', '#ee6363', '#d44942', '#cd0000', '#ff0000']
    mapper = LinearColorMapper(palette = colors, low = 0, high = 100)

    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'
    p_sum = figure(title = "Summary Statistic", toolbar_location = "above", tools=TOOLS)
        #tools = tools)

    p_sum.grid.grid_line_color = None
    p_sum.axis.axis_line_color = None
    p_sum.axis.major_tick_line_color = None
    p_sum.axis.major_label_text_font_size = "12pt"
    p_sum.axis.major_label_standoff = 0
    p_sum.xaxis.major_label_orientation = 0.5
    p_sum.rect('k', 'z', source = source, width = (1.0), height = (0.5), fill_color={'field': 'tot_lin_pre', 'transform':mapper}, line_color= None)


    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='12pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))


    p_sum.add_layout(color_bar, 'right')
    p_sum.xaxis.axis_label = "log k"
    p_sum.yaxis.axis_label = "z"
    
    
    #Make a textarea, so that the html will print out a textbox of the parameter values

    id_val_string = 'Index = %s <br/>' %index
    h_string = 'h = %s <br/>' %h
    Omega_b_string = '&Omega;<sub>b</sub> = %s <br/>' %Omega_b
    Omega_cdm_string = '&Omega;<sub>cdm</sub> = %s <br/>' %Omega_cdm
    A_s_string = 'A<sub>s</sub> = %s <br/>' %A_s
    n_s_string = 'n<sub>s</sub> = %s <br/>' %n_s

    #Textbox html
    textbox = '<div class=\'boxed\'> Parameter values: <br/>' + id_val_string + h_string + Omega_b_string + Omega_cdm_string + A_s_string + n_s_string + '</div>'
    
    #Create a paragraph to tell the users what to do
    readme = Paragraph(text = """If you want to recreate these plots, look
    no further! Below is the .ini file for CLASS and the code used to run CCL
    on python. For the .ini file, save it under something like mytext.ini, then
    go to your folder with CLASS and simply run ./class myext.ini pk_ref.pre
    REMEMBER TO ADD THAT LAST ARGUMENT SINCE THAT ALLOWS FOR A HIGHER PRECISION
    For the CCL one, make sure you have it installed then simply run in Python.
    When you plot these against each other make sure to multiply the CLASS values
    by proper factor of h, since CLASS units are proportional to factors of h
    """, width = 500)

    #Create preformatted text of the .ini file used and the code for CLASS and CCL
    with open('../class/ini_files/lhs_lin_pk_%05d.ini' %i, 'r') as myfile:
        ini_text = myfile.read()
    class_pretext = PreText(text='CLASS .ini file \n' + ini_text)

    h_ccl = 'h = %s \n' %h
    Omega_b_ccl = 'Omega_b = %s \n' %Omega_b
    Omega_cdm_ccl = 'Omega_cdm = %s \n' %Omega_cdm
    A_s_ccl = 'A_s = %s \n' %A_s
    n_s_ccl = 'n_s = %s \n' %n_s

    index_ccl = 'index = %s \n' %index
    #Create a textbox that tells the parameters
    parameters = PreText(text="""Parameter values \n""" + index_ccl + h_ccl +
        Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl)

    #Create one for the CCL code used
    ccl_pretext = PreText(text=
    """Code for CCL, just simply run in python
Make sure to have the CLASS k values, so it coincides properly
i.e. make sure the class_path_lin is correct

import numpy as np
import pyccl

""" + 
    h_ccl + Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl + 
    """
cosmo = pyccl.Cosmology(Omega_c=Omega_cdm, Omega_b=Omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
z_vals = ['1', '2', '3', '4', '5', '6']
for j in range(len(z_vals)):
    z_val = z_vals[j]
    class_path_lin = '/class/output/lin/lhs_lin_pk_%s' %trial
    z_path = 'z%s_pk.dat' %z_val
    k_lin_data = np.loadtxt(class_path_lin, skiprows=4)
    k_lin = k_lin_data[:,0]
    k_lin *= h
    #Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
    z = j * 0.5
    a = 1. / (1. + z)
    #Matter power spectrum for lin
    pk_lin = pyccl.linear_matter_power(cosmo, k_lin, a)
    """, width=500)

    #ccl_pretext = 
    # Embed plot into HTML via Flask Render

    #Create whitespace to fill between class_pretext and ccl_pretext
    whitespace = PreText(text = """ """, width = 200)
    #l = layout([[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    l = layout([[p_sum, parameters],[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    # Embed plot into HTML via Flask Render
    script, div = components(l)
    #print (script)
    #print(div)

    return render_template("lin_pre.html", script=script, div=div)

@app.route('/nl_pre/')
def nl_pre():
    index = request.args.get('index')
    if index == None:
        index = '0'
    #Create the plot and get the parameter values

    # load the data
    i = int(index)

    z_vals = ['1', '2', '3', '4', '5', '6']
    p = figure(toolbar_location="right", title = "CCL vs CLASS mPk, Non-Linear Precision", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "Discrepancy mPk, Non-Linear Precision", x_axis_type = "log", y_axis_type = "log",
         tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")
   
    #load the data and parameter values
    data = np.loadtxt('../data/par_stan1.csv', skiprows = 1)
    index = float(data[i,0])
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])
    for j, color in zip(z_vals, Spectral6):
        z_act = (float(j) - 1) / 2
        z_path = 'z%s_pk.dat' %j
        z_nl_path = 'z%s_pk_nl.dat' %j
        ccl_path = '../CCL/data_files/lhs_mpk_nl_pk_%05d' % i 
        class_path = '../class/output/nonlin/lhs_nonlin_pk_%05d' %i
        ccl_path += z_path
        class_path += z_nl_path

        cclData = np.loadtxt(ccl_path,  skiprows = 1)
        cclK = cclData[:, 0]
        cclPk = cclData[:, 1]

        classData = np.loadtxt(class_path, skiprows = 4);
        classKLin = classData[:, 0]
        classPLin = classData[:, 1]

        #Multiply by factors
        #multiply k by some factor of h, CLASS and CCL use different units, ugh

        classKLin *= h
        classPLin /= h**3

        # create a plot and style its properties
        
        p.outline_line_color = None
        p.grid.grid_line_color = None

        p2.outline_line_color = None
        p2.grid.grid_line_color = None

        # plot the data
        #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
        p.line(cclK, cclPk, line_width = 2, color=color, legend='ccl data, z=%3.1f' %z_act)
        p.circle(cclK, cclPk, size = 5, color=color, legend = "ccl data, z=%3.1f" %z_act)

        #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
        p.line(classKLin, classPLin, line_width = 2,color=color, line_dash='dashed', legend='class data, z=%3.1f' %z_act)
        p.square(classKLin, classPLin, size = 5, fill_alpha=0.8,color=color, legend = "class data, z=%3.1f" %z_act)

        # Set the x axis label
        # Set the y axis label
        p.yaxis.axis_label = 'Count (log)'
        comparisonValue = abs(cclPk - classPLin) / classPLin
        p2.line(classKLin, comparisonValue, line_width = 2,color=color, legend='z=%3.1f' %z_act)
        p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, color=color,size = 5, legend='z=%3.1f' %z_act)

    #Adds the interactive legend and the axes labels
    p.legend.click_policy='hide'
    p.legend.location = 'bottom_left'
    p.yaxis.axis_label = 'P(k)'
    p.xaxis.axis_label = 'k'


    p2.legend.click_policy='hide'
    p2.legend.location = 'bottom_left'
    p2.yaxis.axis_label = '(CCL - CLASS)/CLASS'
    p2.xaxis.axis_label = 'k'

    #Also the number for failures can either include clustering regime only or not
    thres = 1.e-4 #Threshold for number of failures
    clustering_only = False #Only counts failures if inside the clustering regime

    ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
    ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
    lin_scale_min = 1e-2 #Min for the linear scales
    lin_scale_max = 1e-1 #Max for the linear scales
    quasi_scale_min = 1e-1 #Min for the quasi-lin scales
    quasi_scale_max = 1.0 #Max for the quasi-lin scales


    cluster_reg_min = 1e-2 #Min for the cluster regime
    cluster_reg_max = 0.2 # Max for the cluster regime

    #load the data


    #Create arrays that will be filled in the loop over trials
    #Total of the wights
    tot_tot_nl_pre = []

    #Get the totals for different k_ranges
    #We have 3 k_ranges, denote by 1,2,3
    #1 = Ultra Large Scales
    #2 = Linear scales
    #3 = Nonlinear scales


    ###########################
    #                         #
    #GETTING THE SUMMARY STATS#
    #                         #
    ###########################
    #for i in range(len(trial_arr)):
    trial = data[i,0]
    print ('Performing trial %05d' %trial)

    z_vals = ['1', '2', '3', '4', '5', '6']

    #Gonna generate an array of arrays, with each row corresponding to a different z value
    #Each columns will correspond to a different bins of k_values
    tot_nl_pre = []

    #For list of lists
    tot_nl_pre_ll = []

    for j in range(len(z_vals)):
        z_val = z_vals[j]
        z_path ='_z%s.dat' %z_val
        print ('Performing z_val = ', z_val)

        #For ease in iterating over different z values we use string manipulation
        #stats_nl_pre_path = '../../stats/lhs/nl/pre/lhs_mpk_err_nl_pk_%05d' %trial
        stats_nl_pre_path = '../stats/lhs_mpk_err_nl_pk_%05d' %trial

        #Adds the z_path
        stats_nl_pre_path += z_path

        #Calls the data
        stats_nl_pre_data = np.loadtxt(stats_nl_pre_path, skiprows=1)

        stats_nl_pre_k = stats_nl_pre_data[:,0]
        stats_nl_pre_err = stats_nl_pre_data[:,1]

        #Create arrays that will be used to fill the complete summary arrays
        tot_nl_pre_z = []

        #For list of lists
        tot_nl_pre_z_ll = []

        #We perform a loop that looks into the bins for k
        #Doing this for lin
        #Much easier than doing a for loop because of list comprehension ALSO FASTER
        tot_ultra = 0 #initialize value for ultra large scales
        tot_lin = 0 #initialize for lin scales
        tot_quasi = 0 #initialize for quasi lin scales

        #k has to fall in the proper bins
        aux_k_ultra = (stats_nl_pre_k >= ultra_scale_min) & (stats_nl_pre_k < ultra_scale_max)
        aux_k_lin = (stats_nl_pre_k >= lin_scale_min) & (stats_nl_pre_k < lin_scale_max)
        aux_k_quasi = (stats_nl_pre_k >= quasi_scale_min) & (stats_nl_pre_k <= quasi_scale_max)

        #Looks at only the regime where clustering affects it
        if clustering_only == True:
            aux_cluster_ultra = (stats_nl_pre_k[aux_k_ultra] > cluster_reg_min) & (stats_nl_pre_k[aux_k_ultra] < cluster_reg_max)
            aux_cluster_lin = (stats_nl_pre_k[aux_k_lin] > cluster_reg_min) & (stats_nl_pre_k[aux_k_lin] < cluster_reg_max)
            aux_cluster_quasi = (stats_nl_pre_k[aux_k_quasi] > cluster_reg_min) & (stats_nl_pre_k[aux_k_quasi] < cluster_reg_max)

            #Calculate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs((stats_nl_pre_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
            w_lin = np.log10(np.abs((stats_nl_pre_err[aux_k_lin])[aux_cluster_lin]) / thres)
            w_quasi = np.log10(np.abs((stats_nl_pre_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            tot_ultra = np.sum(w_ultra)
            tot_lin = np.sum(w_lin)
            tot_quasi = np.sum(w_quasi)
        #calculates imprecision in any regime
        if clustering_only == False:
            #caluclate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs(stats_nl_pre_err[aux_k_ultra]) / thres)
            w_lin = np.log10(np.abs(stats_nl_pre_err[aux_k_lin]) / thres)
            w_quasi = np.log10(np.abs(stats_nl_pre_err[aux_k_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            #calculate the totals
            tot_ultra = np.sum(w_ultra)
            tot_lin = np.sum(w_lin)
            tot_quasi = np.sum(w_quasi)


        #Append these values to our z summary stat
        #For list only
        tot_nl_pre_z = np.append(tot_nl_pre_z, tot_ultra)
        tot_nl_pre_z = np.append(tot_nl_pre_z, tot_ultra) # 2 bins
        tot_nl_pre_z = np.append(tot_nl_pre_z, tot_lin)
        tot_nl_pre_z = np.append(tot_nl_pre_z, tot_quasi)

        #For list of lists
        tot_nl_pre_z_ll.append(tot_ultra)
        tot_nl_pre_z_ll.append(tot_ultra) # 2 bins
        tot_nl_pre_z_ll.append(tot_lin)
        tot_nl_pre_z_ll.append(tot_quasi)

        #Append these values for the general z stat
        #For list only
        tot_nl_pre = np.append(tot_nl_pre, tot_nl_pre_z)
        #For list of lists
        tot_nl_pre_ll.append(tot_nl_pre_z_ll)




	#Generate our z values for plotting
    z_actual = range(len(z_vals))
    z_arr = np.float_(np.asarray(z_actual))
    z_arr *= 0.5
    z = []
    z_ll = []	#Create a heat map, but makes it red, right now we just mark threshold on the heat map
    for j in range(len(z_actual)):
        z_full = np.full(len(tot_nl_pre_ll[0]), z_arr[j])
        z = np.append(z,z_full)
        z_ll.append(z_full)

	#Generate an array of the midpoints of the bins

    ultra_scale_bin = (np.log10(ultra_scale_max) + np.log10(ultra_scale_min))/2
    ultra_scale_bin_1 = ultra_scale_bin - 0.5
    ultra_scale_bin_2 = ultra_scale_bin + 0.5
    lin_scale_bin = (np.log10(lin_scale_max) + np.log10(lin_scale_min))/2
    quasi_scale_bin = (np.log10(quasi_scale_max) + np.log10(quasi_scale_min))/2

    k_bin = [ultra_scale_bin_1, ultra_scale_bin_2, lin_scale_bin, quasi_scale_bin]
    k_list = k_bin * len(z_vals) 


	#Gonna try to plot it the pandas way
	#WORKS!!!! AND it fills the whole space. FUCKING LIT
    k_words = ['Ultra-large', 'Linear', 'Quasi Lin']
	#Use pandas to generate a data frame
    #df = pd.DataFrame(sum_lin_ll, index=z_arr, columns=k_words)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])
    #print(sum_lin_z_ll)

    #print(sum_lin_z)
    #df = pd.DataFrame(tot_nl_pre_ll, index=z_arr, columns=k_words)
    data_nl_pre = {'tot_nl_pre': tot_nl_pre, 'z':z, 'k':k_list}
    source = ColumnDataSource(data=data_nl_pre)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange

	#Failed here
	#cmap, norm = mcolors.from_levels_and_colors([thres,100], ['red'])

	#Trying to brute force colors for me
    colors = ['#fff5ee', '#ffe4e1', '#ffc1c1', '#eeb4b4', '#f08080', '#ee6363', '#d44942', '#cd0000', '#ff0000']
    mapper = LinearColorMapper(palette = colors, low = 0, high = 100)

    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'
    p_sum = figure(title = "Summary Statistic", toolbar_location = "above", tools=TOOLS)
        #tools = tools, toolbar_location = "above")

    p_sum.grid.grid_line_color = None
    p_sum.axis.axis_line_color = None
    p_sum.axis.major_tick_line_color = None
    p_sum.axis.major_label_text_font_size = "12pt"
    p_sum.axis.major_label_standoff = 0
    p_sum.xaxis.major_label_orientation = 0.5
    p_sum.rect('k', 'z', source = source, width = (1.0), height = (0.5), fill_color={'field': 'tot_nl_pre', 'transform':mapper}, line_color= None)


    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='12pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))


    p_sum.add_layout(color_bar, 'right')
    p_sum.xaxis.axis_label = "log k"
    p_sum.yaxis.axis_label = "z"

    #Make a textarea, so that the html will print out a textbox of the parameter values

    id_val_string = 'Index = %s <br/>' %index
    h_string = 'h = %s <br/>' %h
    Omega_b_string = '&Omega;<sub>b</sub> = %s <br/>' %Omega_b
    Omega_cdm_string = '&Omega;<sub>cdm</sub> = %s <br/>' %Omega_cdm
    A_s_string = 'A<sub>s</sub> = %s <br/>' %A_s
    n_s_string = 'n<sub>s</sub> = %s <br/>' %n_s

    
    #textbox
    textbox = '<div class=\'boxed\'> Parameter values: <br/>' + id_val_string + h_string + Omega_b_string + Omega_cdm_string + A_s_string + n_s_string + '</div>'
    
    #parameter values
    #parameter = 
    #Create a paragraph to tell the users what to do
    readme = Paragraph(text = """If you want to recreate these plots, look
    no further! Below is the .ini file for CLASS and the code used to run CCL
    on python. For the .ini file, save it under something like mytext.ini, then
    go to your folder with CLASS and simply run ./class myext.ini pk_ref.pre
    REMEMBER TO ADD THAT LAST ARGUMENT SINCE THAT ALLOWS FOR A HIGHER PRECISION
    For the CCL one, make sure you have it installed then simply run in Python.
    When you plot these against each other make sure to multiply the CLASS values
    by proper factor of h, since CLASS units are proportional to factors of h
    """, width = 500)

    #Create preformatted text of the .ini file used and the code for CLASS and CCL
    with open('../class/ini_files/lhs_nonlin_%05d.ini' %i, 'r') as myfile:
        ini_text = myfile.read()
    class_pretext = PreText(text='CLASS .ini file \n' + ini_text)

    h_ccl = 'h = %s \n' %h
    Omega_b_ccl = 'Omega_b = %s \n' %Omega_b
    Omega_cdm_ccl = 'Omega_cdm = %s \n' %Omega_cdm
    A_s_ccl = 'A_s = %s \n' %A_s
    n_s_ccl = 'n_s = %s \n' %n_s

    index_ccl = 'index = %s \n' %index
    #Create a textbox that tells the parameters
    parameters = PreText(text="""Parameter values \n""" + index_ccl + h_ccl +
        Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl)

    #Create one for the CCL code used
    ccl_pretext = PreText(text=
    """Code for CCL, just simply run in python
Make sure to have the CLASS k values, so it coincides properly
i.e. make sure the class_path_nl is correct

import numpy as np
import pyccl

""" + 
    h_ccl + Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl + 
    """
cosmo = pyccl.Cosmology(Omega_c=Omega_cdm, Omega_b=Omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
z_vals = ['1', '2', '3', '4', '5', '6']
for j in range(len(z_vals)):
    z_val = z_vals[j]
    class_path_nl = '/class/output/nonlin/lhs_nonlin_pk_%s' %trial
    z_path = 'z%s_pk_nl.dat' %z_val
    k_nl_data = np.loadtxt(class_path_nl, skiprows=4)
    k_nl = k_nl_data[:,0]
    k_nl *= h
    #Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
    z = j * 0.5
    a = 1. / (1. + z)
    #Matter power spectrum for nonlin
    pk_nl = pyccl.nonlinear_matter_power(cosmo, k_nl, a)
    """, width=500)

    #ccl_pretext = 

    #Create whitespace to fill between class_pretext and ccl_pretext
    whitespace = PreText(text = """ """, width = 200)
    #l = layout([[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    l = layout([[p_sum, parameters],[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    #
    # Embed plot into HTML via Flask Render
    script, div = components(l)   
    #print (script)
    #print(div)

    return render_template("nl_pre.html", script=script, div=div)

#With debug=True, Flask Render will auto-reload when there are code changes
if __name__ == '__main__':
    #set debug to False in a production environment
    app.run(port=5000, debug=True)







