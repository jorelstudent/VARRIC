from __future__ import print_function
import os
from subprocess import call
import subprocess
import pdb
import numpy as np
import glob

#This .py file runs ./class on the all .ini files
#Iterates over every file with that extension in this folder

#This is for default settings

#for filename in glob.iglob('/Users/penafiel/JPL/class/ini_files/tuple/*nl_0*.ini'):
#	#Executes the ./class for each ini file
#	
#	print('Performing', filename)
#	#Calls the class executable for the files
#	subprocess.call(['./class', '%s' %filename])#, stdout = subprocess.PIPE)
#	#Get and save the output
#	stdout = subprocess.check_output(['./class', '%s' %filename])
#	basefile = os.path.splitext('%s' %filename)[0]
#	file = open('%s.txt' %basefile, 'w')
#	file.write(stdout)
#	file.close()


for filename in glob.iglob('/Users/penafiel/JPL/class/ini_files/wcdm/*_lin_0*.ini'):
	#Executes the ./class for each ini file
	
	print('Performing', filename)
	#Calls the class executable for the files
	subprocess.call(['./class', '%s' %filename])#, stdout = subprocess.PIPE)
	#Get and save the output
	stdout = subprocess.check_output(['./class', '%s' %filename])
	basefile = os.path.splitext('%s' %filename)[0]
	file = open('%s.txt' %basefile, 'w')
	file.write(stdout)
	file.close()
"""
#This is for precision settings
for filename in glob.iglob('/Users/penafiel/JPL/class/ini_files/wcdm/*pk_0*.ini'):
	#Executes the ./class for each ini file
	
	print('Performing precision ', filename)
	#Do this for precision measurements
	subprocess.call(['./class', '%s' %filename, 'pk_ref.pre'])#, stdout = subprocess.PIPE)
	#Get and save the output
	stdout = subprocess.check_output(['./class', '%s' %filename, 'pk_ref.pre'])
	basefile = os.path.splitext('%s' %filename)[0]
	file = open('%s.txt' %basefile, 'w')
	file.write(stdout)
	file.close()

"""
