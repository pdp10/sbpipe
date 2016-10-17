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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $



# Utilities to generate Latex code. These functions are used for reporting purposes.

import logging
import os
import re
import subprocess
import sys

logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from re_utils import natural_sort_key
from sb_config import which


def get_latex_header(pdftitle="SB pipe report", title="SB pipe report", abstract="Generic report."):
    """
    Initialize a Latex header with a title and an abstract.
    
    :param pdftitle: the pdftitle for the LaTeX header
    :param title: the title for the LaTeX header
    :param abstract: the abstract for the LaTeX header
    :return: the LaTeX header
    """
    return (
        "\\documentclass[10pt,a4paper]{article}\n"
        "\\usepackage[english]{babel}\n"
        "\\usepackage[top=2.54cm,bottom=2.54cm,left=3.17cm,right=3.17cm]{geometry}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage[plainpages=false,pdfauthor={Generated with SB pipe},pdftitle={" + pdftitle + "},pdftex]{hyperref}\n"
        "\\author{Generated with SB pipe} \n"
        "\\title{" + title + "}\n"
        "\\date{\\today}\n"
        "\\begin{document}\n"
        "\\maketitle\n"
        "\\begin{abstract}\n" + abstract + " \n\\end{abstract}\n"
    )


def latex_report_single_param_scan(outputdir, sim_plots_folder, filename_prefix, model_noext, scanned_par):
    """
    Generate a report for a single parameter scan task.
    
    :param outputdir: the output directory
    :param sim_plots_folder: the folder containing the simulated plots
    :param filename_prefix: the prefix for the LaTeX file
    :param model_noext: the model name
    :param scanned_par: the scanned parameter
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        scanned_par_name = scanned_par[0:].replace("_", " ")
        logger.info("Model: " + model_name)
        logger.info("Parameter scan for: " + scanned_par)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Report for {\\it " + model_name + "} model, scanning {\\it " + scanned_par_name + "}.")
        file_out.write(header)
        logger.info("List of files in " + os.path.join(outputdir, sim_plots_folder) + ":")
        file_out.write("\\section*{Plots - Parameter scan for " + scanned_par_name + "}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, sim_plots_folder)) if f.endswith('.png')]
        folder.sort()
        for infile in folder:
            if infile.find(model_noext) != -1:
                scanned_par_pos = infile.find(scanned_par)
                eval_marker = infile.find("__eval_")
                if scanned_par_pos != -1 and scanned_par_pos < eval_marker:
                    logger.info(infile)
                    file_out.write("\\includegraphics[scale=0.24]{" + sim_plots_folder + "/" + infile + "}\n")
                    file_out.write("\\hfill\n")
        file_out.write("\\end{document}\n")


def latex_report_double_param_scan(outputdir, sim_plots_folder, filename_prefix, model_noext,
                                   scanned_par1, scanned_par2):
    """
    Generate a report for a double parameter scan task.
    
    :param outputdir: the output directory
    :param sim_plots_folder: the folder containing the simulated plots
    :param filename_prefix: the prefix for the LaTeX file
    :param model_noext: the model name
    :param scanned_par1: the 1st scanned parameter
    :param scanned_par1: the 2nd scanned parameter
    """    
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        scanned_par1_name = scanned_par1[0:].replace("_", " ")
        scanned_par2_name = scanned_par2[0:].replace("_", " ")
        logger.info("Model: " + model_name)
        logger.info("Parameter scan for: " + scanned_par1_name + " and " + scanned_par2_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Report for {\\it " + model_name + "} model, scanning {\\it " +
                                  scanned_par1_name + "} and {\\it " + scanned_par2_name + "}.")
        file_out.write(header)
        logger.info("List of files in " + os.path.join(outputdir, sim_plots_folder) + ":")
        file_out.write("\\section*{Plots - Parameter scan for " + scanned_par1_name + " and " +
                       scanned_par2_name + "}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, sim_plots_folder)) if f.endswith('.png')]
        folder.sort(key=natural_sort_key)
        curr_readout = ''
        prev_readout = ''
        for infile in folder:
            if infile.find(model_noext) != -1:
                try:
                    curr_readout = re.search('__eval_(.+?)__tp_', infile).group(1)
                except AttributeError:
                    curr_readout = 'Unknown readout'
                if curr_readout != prev_readout:
                    logger.debug("Adding plots for: " + curr_readout)
                    file_out.write("\\subsection*{Readout: " + curr_readout.replace("_", " ") + "}\n")
                    prev_readout = curr_readout

                scanned_par1_pos = infile.find(scanned_par1)
                eval_marker = infile.find("__eval_")
                if scanned_par1_pos != -1 and scanned_par1_pos < eval_marker:
                    logger.info(infile)
                    file_out.write("\\includegraphics[scale=0.24]{" + sim_plots_folder + "/" + infile + "}\n")
                    file_out.write("\\hfill\n")
        file_out.write("\\end{document}\n")


def latex_report_simulate(outputdir, sim_plots_folder, model_noext, filename_prefix):
    """
    Generate a report for a time course task.
    
    :param outputdir: the output directory
    :param sim_plots_folder: the folder containing the simulated plots
    :param model_noext: the model name
    :param filename_prefix: the prefix for the LaTeX file
    """     
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        logger.info(model_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Report for {\\it " + model_name + "} model.")
        file_out.write(header)
        logger.info("List of files in " + os.path.join(outputdir, sim_plots_folder) + ":")
        file_out.write("\\section*{Plots}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, sim_plots_folder)) if f.endswith('.png')]
        folder.sort()
        for infile in folder:
            if infile.find(model_noext) != -1:
                if (infile.find('_sd_n_ci95_') != -1):
                    logger.info(infile)
                    file_out.write("\\includegraphics[scale=0.24]{" + sim_plots_folder + "/" + infile + "}\n")
        file_out.write("\\end{document}\n")


def latex_report_param_estim(outputdir, sim_plots_folder, model_noext, filename_prefix):
    """
    Generate a report for a parameter estimation task.
    
    :param outputdir: the output directory
    :param sim_plots_folder: the folder containing the simulated plots
    :param model_noext: the model name
    :param filename_prefix: the prefix for the LaTeX file
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        logger.info(model_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Generic report for {\\it " + model_name + "} model.")
        file_out.write(header)
        logger.info("List of files in " + os.path.join(outputdir, sim_plots_folder) + ":")
        file_out.write("\\section*{Plots}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, sim_plots_folder)) if f.endswith('.png')]
        folder.sort()
        begin_figure = False
        figure_num = 0
        figures_per_page = 12
        for infile in folder:
            logger.info(infile)
            figure_num += 1
            if not begin_figure:
                file_out.write("\\begin{figure}[!ht]\n")
                begin_figure = True
            file_out.write("\\begin{minipage}{0.31\\textwidth}\n")
            file_out.write("\\includegraphics[width=\\textwidth]{" + sim_plots_folder + "/" + infile + "}\n")
            file_out.write("\\end{minipage}\n")
            file_out.write("\\hfill\n")
            if figure_num % figures_per_page == 0 and begin_figure:
                file_out.write("\\end{figure}\n")
                file_out.write("\\newpage\n")
                begin_figure = False
                figures_per_page = 18
                figure_num = 0
        if begin_figure:
            file_out.write("\\end{figure}\n")
        file_out.write("\\end{document}\n")
    

def latex_report(outputdir, sim_plots_folder, model_noext, filename_prefix, caption=False):
    """
    Generate a generic report.
    
    :param outputdir: the output directory
    :param sim_plots_folder: the folder containing the simulated plots
    :param model_noext: the model name
    :param filename_prefix: the prefix for the LaTeX file
    :param caption: True if figure captions (=figure file name) should be added
    """
    with open(os.path.join(outputdir, filename_prefix + model_noext + ".tex"), "w") as file_out:
        model_name = model_noext[:].replace("_", " ")
        logger.info(model_name)
        # writing on file
        # Get latex header
        header = get_latex_header("Report: " + model_name,
                                  "Report: " + model_name,
                                  "Generic report for {\\it " + model_name + "} model.")
        file_out.write(header)
        logger.info("List of files in " + os.path.join(outputdir, sim_plots_folder) + ":")
        file_out.write("\\section*{Plots}\n")
        folder = [f for f in os.listdir(os.path.join(outputdir, sim_plots_folder)) if f.endswith('.png')]
        folder.sort()
        begin_figure = False
        figure_num = 0
        figures_per_page = 9
        for infile in folder:
            logger.info(infile)
            figure_num += 1
            if not begin_figure:
                file_out.write("\\begin{figure}[!ht]\n")
                begin_figure = True
            file_out.write("\\begin{minipage}{0.31\\textwidth}\n")
            file_out.write("\\includegraphics[width=\\textwidth]{" + sim_plots_folder + "/" + infile + "}\n")
            if caption:
                file_out.write("\\caption{" + infile.replace(model_noext, "").replace("_", " ")[:-4] + "}\n")
            file_out.write("\\end{minipage}\n")
            file_out.write("\\hfill\n")
            if figure_num % figures_per_page == 0 and begin_figure:
                file_out.write("\\end{figure}\n")
                file_out.write("\\newpage\n")
                begin_figure = False
                figures_per_page = 15
                figure_num = 0
        if begin_figure:
            file_out.write("\\end{figure}\n")
        file_out.write("\\end{document}\n")


def pdf_report(outputdir, filename):
    """
    Generate a PDF report from LaTeX report using pdflatex.
    
    :param outputdir: the output directory
    :param filename: the LaTeX file name
    """
    pdflatex = which("pdflatex")
    if pdflatex is None:
        logger.error("pdflatex not found! pdflatex must be installed for pdf reports.")
        return
    currdir = os.getcwd()
    os.chdir(outputdir)
    logger.info(pdflatex + " -halt-on-error " + filename + " ... ")
    p = subprocess.Popen([pdflatex, "-halt-on-error", filename],
                         stdout=subprocess.PIPE)
    p.communicate()[0]
    p = subprocess.Popen([pdflatex, "-halt-on-error", filename],
                         stdout=subprocess.PIPE)
    p.communicate()[0]
    os.chdir(currdir)
