#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $



# Collection of functions for generating Latex code. These functions are used for reporting purposes.

import os



# Initialize a Latex header with a title and an abstract
def get_latex_header(pdftitle = "", title = "", abstract=""):
  return "\\documentclass[10pt,a4paper]{article}\n" \
	   "\\usepackage[utf8]{inputenc}\n" \
	   "\\usepackage[english]{babel}\n" \
	   "\\usepackage[T1]{fontenc}\n" \
	   "\\usepackage[a4paper,top=2.54cm,bottom=2.54cm,left=3.17cm,right=3.17cm]{geometry}\n" \
	   "\\usepackage{graphicx}\n" \
	   "\\usepackage[plainpages=false,pdfauthor={Generated with sb_pipe},pdftitle={" + pdftitle + "},pdftex]{hyperref}\n" \
	   "\\hypersetup{colorlinks=false,linkcolor=blue}\n" \
	   "\\usepackage{url}\n" \
	   "\\usepackage{makeidx}\n" \
	   "\\author{A clever scientist} \n" \
	   "\\title{" + title + "}\n" \
	   "\\date{\\today}\n" \
	   "\\makeindex\n" \
	   "\\begin{document}\n" \
	   "\\maketitle\n" \
	   "\\begin{abstract}\n" + abstract + "\\end{abstract}\n" \
	   "\\tableofcontents\n"


# Create a report for a parameter scanning task (1 model)
def latex_report_par_scan(results_dir, plots_dir, filename_prefix, model_noext, species, legend_noext):
  with open(results_dir + "/" + filename_prefix + model_noext + ".tex", "w") as file_out:
    model_ver = model_noext[:].replace("_", " ")
    species_name = species[0:].replace("_", " ")
    print("Model: " + model_ver)
    print("Perturbation of the species: " + species)
    # writing on file
    # Get latex header
    header = get_latex_header("Report: " + model_ver, "Report: " + model_ver, "Parameter Scan Task for " + species_name)
    file_out.write(header)
    print("List of files in " + results_dir + '/' + plots_dir  + '/' + ":\n")
    file_out.write("\\section*{Plots - Perturbation of " + species_name + "}\n")
    folder = os.listdir(results_dir + '/' + plots_dir + '/')
    folder.sort()
    for infile in folder:
      if infile.find(model_noext) != -1:
	pos = infile.find(species)
	marker = infile.find("__eval_")
	if pos != -1 and pos < marker:
	  print(infile)
	  file_out.write("\\includegraphics[scale=0.20]{" + plots_dir + "/" + infile + "}\n")
	  file_out.write("\\hfill\n")
    file_out.write("\\includegraphics[scale=0.20]{" + plots_dir + "/" + legend_noext + ".png}\n")
    file_out.write("\\hfill\n")
    file_out.write("\\end{document}\n")


# Create a report of a time course task (1 model)
def latex_report_simulate(results_dir, plots_dir, model_noext, filename_prefix):
  with open(results_dir + "/" + filename_prefix + model_noext + ".tex", "w") as file_out:
    model_ver = model_noext[:].replace("_", " ")
    print(model_ver)
    # writing on file
    # Get latex header
    header = get_latex_header("Report: " + model_ver, "Report: " + model_ver)
    file_out.write(header)  
    print("List of files in " + results_dir + '/' + plots_dir + '/' + ":\n")
    file_out.write("\\section*{Plots}\n")
    folder = os.listdir(results_dir + '/' + plots_dir + '/')
    folder.sort()  
    for infile in folder:
      if infile.find(model_noext) != -1:
	if (infile.find('_sd_n_ci95_') != -1):
	  print(infile)
	  file_out.write("\\includegraphics[scale=0.20]{" + plots_dir + "/" + infile + "}\n")
	  file_out.write("\\hfill\n")
    file_out.write("\\end{document}\n")



# Create a generic report
def latex_report(results_dir, plots_dir, model_noext, filename_prefix):
  with open(results_dir + "/" + filename_prefix + model_noext + ".tex", "w") as file_out:
    model_ver = model_noext[:].replace("_", " ")
    print(model_ver)
    # writing on file
    # Get latex header
    header = get_latex_header("Report: " + model_ver, "Report: " + model_ver)
    file_out.write(header)  
    print("List of files in " + results_dir + '/' + plots_dir + '/' + ":\n")
    file_out.write("\\section*{Plots}\n")
    folder = os.listdir(results_dir + '/' + plots_dir + '/')
    folder.sort()  
    for infile in folder:
      print(infile)
      file_out.write("\\includegraphics[scale=0.20]{" + plots_dir + "/" + infile + "}\n")
      file_out.write("\\hfill\n")
    file_out.write("\\end{document}\n")

