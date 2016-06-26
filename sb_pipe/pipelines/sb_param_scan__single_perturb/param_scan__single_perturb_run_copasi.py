#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Run CopasiSE performing a parameter scan.
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-24 13:14:32 $


import os, sys
import subprocess
import shutil

# For reading the first N lines of a file.
from itertools import islice


SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + "/sb_pipe/utils/python/")
import CopasiUtils


# INITIALIZATION
# model: read the model
# species: the species to knock-down (name of the species as in copasi)
# param_scan__single_perturb_simulations_number: Number of times the model should be simulated. For deterministic simulations, ${param_scan__single_perturb_simulations_number}==1 . For stochastic simulations, ${param_scan__single_perturb_simulations_number}==h. 
# models_dir: Read the models dir
# results_dir: Read the results dir
# tmp_dir: Read the tmp dir
def main(model, species, param_scan__single_perturb_simulations_number, simulate__intervals, 
	 param_scan__single_perturb_intervals, models_dir, results_dir, tmp_dir):


  print("Simulating Model: "+ model)

  model_noext=model[:-4]

  names=[]
  species_index=-1
  species_level=-1
  # Set the number of intervals
  intervals=int(param_scan__single_perturb_intervals)+1
  # Set the number of timepoints
  timepoints=int(simulate__intervals)+1


  for i in xrange(0, int(param_scan__single_perturb_simulations_number)):
    
      print("Simulation No.: "+str(i))
      # run CopasiSE. Copasi must generate a (TIME COURSE) report called ${model_noext}.csv in ${tmp_dir}
      process = subprocess.Popen(['CopasiSE', '--nologo', models_dir+"/"+model])
      process.wait()
      

      if not os.path.isfile(tmp_dir+"/"+model_noext+".csv"): 
	  print("ERROR: " + tmp_dir+"/"+model_noext+".csv does not exist!") 
	  continue
      
      # Replace some string in the report file   
      CopasiUtils.replace_str_copasi_sim_report(tmp_dir, model)
      



      # Find the index of species in the header file, so it is possible to read the amount at 
      # the second line.
      if i == 0:
	print("Retrieving column index for species "+species+" from file "+tmp_dir+"/"+model_noext+".csv")
	# Read the first line of a file.
	with open(tmp_dir+"/"+model_noext+".csv") as myfile:
	  # 1 is the number of lines to read, 0 is the i-th element to extract from the list.
	  header = list(islice(myfile, 1))[0].replace("\n", "").split('\t')
	#print header
	for j, name in enumerate(header): 
	  print(str(j) + " " + name + " " + species)
	  if name == species: 
	    species_index=j 
	    break;
	if species_index == -1: 
	  print("Column index for species "+species+": "+str(species_index)+". ERROR: Species not found!!! You must add the species "+species+
	  " to the report form in the copasi file (check the report time-course or parameter scan). STOP")
	  return
	else:
	  print("Column index for species "+species+": "+str(species_index))


      # Prepare the Header for the output files
      # Add a \t at the end of each element of the header
      header = [h + "\t" for h in header]
      # Remove the \t for the last element.
      header[-1] = header[-1].strip()      


      # Prepare the table content for the output files
      for j in xrange(0, intervals):
	# Read the species level
	# Read the second line of a file.
	with open(tmp_dir+"/"+model_noext+".csv") as myfile:
	  # 2 is the number of lines to read, 1 is the i-th element to extract from the list.	  
	  initial_configuration = list(islice(myfile, 2))[1].replace("\n", "").split('\t')
	#print initial_configuration
	species_level = initial_configuration[species_index]
	if species_level == -1: 
	  print("ERROR: species_level not configured!!! STOP")
	  return 
	else:
	  print(species + " level: "+str(species_level)+" (list index: "+str(species_index)+")")
	

	# copy the -th run to a new file: add 1 to timepoints because of the header.
	round_species_level = species_level
	# Read the first timepoints+1 lines of a file.
	with open(tmp_dir+"/"+model_noext+".csv") as file:
	  table = list(islice(file, timepoints+1))  

	# Write the extracted table to a separate file
	with open(results_dir+"/"+model_noext+"__sim_"+str(i+1)+"__level_"+str(round_species_level)+".csv", 'w') as file:
	  for line in table:
	    file.write(line)

	with open(tmp_dir+"/"+model_noext+".csv") as file:
	  # read all lines
	  lines = file.readlines()
	  

	with open(tmp_dir+"/"+model_noext+".csv~", 'w') as file:
	  file.writelines(header)
	  file.writelines(lines[timepoints+1:])

	

	shutil.move(tmp_dir+"/"+model_noext+".csv~", tmp_dir+"/"+model_noext+".csv")
	
	
      # remove the file
      os.remove(tmp_dir+"/"+model_noext+".csv")
