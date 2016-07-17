#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $


# Library of functions for plotting the calibration results after running the parameter estimation task


import sys
import os, glob
# sort by string considering the locale
import locale
# this reads the environment and inits the right locale
locale.setlocale(locale.LC_ALL, "")
# alternatively, (but it's bad to hardcode)
# locale.setlocale(locale.LC_ALL, "sv_SE.UTF-8")

from numpy import *
import scipy.stats




# Created Extended-files (complete time course)
def extend(folder, files):
  print("Extend files - function")
  for file in files:
    print("\t" + file)
    fileIN = open(os.path.join(folder, file), "r")
    fileOUT = open(os.path.join(folder, file[0:-4] + "_ext.csv"), "w")
    line = fileIN.readline().split()
    fileOUT.write("Iterations\t" + line[1] + "\n")
    line = fileIN.readline()
    content = line.split()
    line_next = line
    content_next = content
    iteration = 0
    lastone = False
    while len(content) > 0 and not lastone:
      if len(content_next) > 0:
	if int(content_next[0]) <= iteration:
	  line = line_next
	  content = content_next
	  line_next = fileIN.readline()
	  content_next = line_next.split()
	  #print(content)
      elif int(content[0]) <= iteration:
	lastone = True
      fileOUT.write(str(iteration) + "\t" + content[1] + "\n")
      iteration = iteration + 1
    fileIN.close()
    fileOUT.close()



# Merge the files generated from file_extension function
# Return the best file No. and its score
def merge(folder, files, fileout):
  print("Merge files - function")
  cache = []
  iteration = 0
  completed = []
  finished = 0
  fileIN = []
  # contain the best configuration [file, value]
  best = [0, float(sys.maxint)]
  fileOUT = open(os.path.join(folder, fileout), "w")
  for file in files:
    fileIN.append(open(os.path.join(folder, file), "r"))
    completed.append(False)
  # Initialisation
  fileOUT.write("Iterations")
  for i in range(0, len(files)):
    line = fileIN[i].readline()
    cache.append(line.split()[1])
    fileOUT.write("\tCalibration_" + str(i+1))
    #fileOUT.write("\t" + cache[i])
  fileOUT.write("\n")
  # Merge and complete datasets
  while finished != len(files):
    for i in range(0, len(files)):
      if not completed[i]:
	line = fileIN[i].readline()
	if len(line) > 0:
	  cache[i] = line.split()[1]
	else:
	  completed[i] = True
	  finished = finished + 1
	  fileIN[i].close()
	  print("\t" + files[i] + " completed")
    if finished != len(files):
      fileOUT.write(str(iteration))
      for i in range(0, len(files)):
	fileOUT.write("\t" + cache[i])
	if float(cache[i]) < best[1]:
	  best[0] = i
	  best[1] = float(cache[i])
      fileOUT.write("\n")
      iteration = iteration + 1
  #endwhile  
  fileOUT.close()
  return best[0], best[1]


# Compute mean confidence intervals
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*array(data)
    n = len(a)
    m, sd = mean(a), std(a)
    # calls the inverse CDF of the Student's t distribution
    h = (sd/sqrt(n)) * scipy.stats.t._ppf((1+confidence)/2., n-1)
    return m-h, m+h


# Merge the files generated from file_extension function
def compute_statistics(folder, filename, fileout):
  print("Compute statistics - function")
  # read a text file as a list of lines
  # find the last line, change to a file you have
  with open (os.path.join(folder, filename), "r") as file:
    line = file.readlines()
  # print "The last line is:" + line[len(line)-1]
  # skip the iteration number column
  line = line[len(line)-1].split()
  lastrow = []
  for i in range(1, len(line)):
    lastrow.append(float(line[i]))
  #print "The last line is:" + line
  # store the index of the minimum element
  index_best_calib = lastrow.index(min(lastrow)) 
  print "The best calibration is Calibration_" + str(index_best_calib)
  
  fileIN = open(os.path.join(folder, filename), "r")
  fileOUT = open(os.path.join(folder, fileout), "w")
  fileOUT.write("Iterations\tMean\tCI_95_inf\tCI_95_sup\tSD\tBest_Calib\n")
  # skip the header line
  line = fileIN.readline()
  line = fileIN.readline()
  iteration = 0
  while line:
    # skip the iteration column
    row = line.split()[1:]
    for i in range(0, len(row)):
      row[i] = float(row[i])
      if iteration%50000 == 0:
        print(row)
    # skip rows for improving the quality of the plot (otherwise too dense!)
    if iteration%1000 == 0:
      m = mean(row)
      ci_95_inf, ci_95_sup = mean_confidence_interval(row, 0.95)
      sd = std(row)
      fileOUT.write(str(iteration) + "\t" + str(m) + "\t" + str(ci_95_inf) + "\t" + str(ci_95_sup)  + "\t" + str(sd) + "\t" + str(row[index_best_calib]) + "\n")
    iteration = iteration + 1
    line = fileIN.readline()
  #endwhile
  fileIN.close()
  fileOUT.close()



# plot the mean with confidence intervals 
def plot_mean_and_ci(folder, filein, fileout, best_pos, best_score, nsamples, colour, identifier):
  #from rpy2 import *
  import rpy2.robjects as robjects
  r = robjects.r
  r.source("plot_functions.r")
  # translate the function
  plot_calib_r_fun = robjects.r['plot_calibration_mean_ci']
  plot_calib_r_fun(folder, filein, fileout, best_pos, best_score, nsamples, colour, identifier)
  # This approach doesn't work because it passes a vector (1 parameter), instead of n parameters
  # translate the function parameters
  # plot_calib_r_params = robjects.StrVector([folder, filein, fileout, best_pos, best_score, nsamples, colour]) 
  # print(plot_calib_r_fun.r_repr())
  # print(plot_calib_r_params.r_repr())  
  # call the plot function
  # plot_calib_r_fun(plot_calib_r_params.r_repr())

  
def extend_merge_plot(folder, names, identifier=""):
  files = names
  files_ext = []
  for f in names:
    files_ext.append(f[0:-4] + "_ext.csv")
  extend(folder, files)
  best_pos, best_score = merge(folder, files_ext, "summary_" + identifier + "_ext.csv")
  compute_statistics(folder, "summary_" + identifier + "_ext.csv", "summary_" + identifier + "_statistics.csv")
  plot_mean_and_ci(folder, "summary_" + identifier + "_statistics.csv", "plot_summary_" + identifier + "_calib_mean_ci95.png", 
		    str(best_pos+1), str(best_score), str(len(names)), "black", identifier)
  return best_pos, best_score


# plot the mean with confidence intervals 
def plot_mean_and_ci_multi(rscript_folder, folder, filein, fileout, best_pos, best_score, nsamples, colour, identifier):
  #from rpy2 import *
  import rpy2.robjects as robjects
  r = robjects.r
  r.source(os.path.join(rscript_folder,'plot_functions.r'))
  # translate the function
  plot_calib_r_fun = robjects.r['plot_calibration_mean_ci_multi']
  plot_calib_r_fun(folder, robjects.StrVector(filein), fileout, best_pos, best_score, robjects.StrVector(nsamples), robjects.StrVector(colour), robjects.StrVector(identifier))



def plot_calibration(rscript_folder, folder, pools, colours):
  # Cleaning previous results
  for i in range(0, len(pools)):
    if(os.path.exists(os.path.join(folder,"summary_" + pools[i] + "_statistics.csv"))):
      print("Cleaning: " + os.path.join(folder,"summary_" + pools[i] + "_statistics.csv") + "\n")
      os.remove(os.path.join(folder,"summary_" + pools[i] + "_statistics.csv"))
  # Initialisation
  files = []
  idf = []
  filestat = []
  nsa = []
  best_best = [0, float(sys.maxint)]
  for i in range(0,len(pools)):
    files.append(glob.glob(os.path.join(folder, "*" + pools[i] + "*.csv")))
    files[i].sort(cmp=locale.strcoll)
    print(files[i])
    for j in range(0,len(files[i])):
      files[i][j] = os.path.basename(files[i][j])
    if(len(files[i]) > 0):
      best_pos, best_score = extend_merge_plot(folder, files[i], pools[i])
      if(best_score < best_best[1]):
	best_best = [best_pos, best_score]
      nsa.append(str(len(files[i])))
      filestat.append("summary_" + pools[i] + "_statistics.csv")
    else:
      print "Pool " + pools[i] + " is empty\n"
  # Plot the mean and the confidence intervals
  print("Printing multi-plots")
  plot_mean_and_ci_multi(rscript_folder, folder, filestat, "plot_calib_complete.png", best_best[0], best_best[1], nsa, colours, pools)
  # Removing *_ext.csv files to free hd space (these files can be huge!)
  for i in range(0, len(pools)):
    files_to_delete = glob.glob(os.path.join(folder, "*" + pools[i] + "*_ext.csv"))
    print("Cleaning *" + pools[i] + " *_ext.csv files from " + folder + "\n")
    for j in range(0, len(files_to_delete)):
      os.remove(folder + os.path.basename(files_to_delete[j]))
      print("\tFile " + files_to_delete[j] + " ... removed\n")







