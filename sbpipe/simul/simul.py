#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-11-01 15:43:32 $

import logging

logger = logging.getLogger('sbpipe')


class Simul:
    """
    Generic simulator.
    """

    def __init__(self):
        """
        Default constructor.
        """
        pass

    def sim(self, model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        """
        Time course simulator.
        
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory containing the output files
        :param cluster_type: pp for local Parallel Python, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param pp_cpus: the number of CPU used by Parallel Python.
        :param runs: the number of model simulation
        """
        pass

    def ps1(self, model, scanned_par, simulate_intervals,
            single_param_scan_intervals, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        """
        Single parameter scan.
        
        :param model: the model to process
        :param scanned_par: the scanned parameter
        :param simulate_intervals: the time step of each simulation
        :param single_param_scan_intervals: the number of scans to perform
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        :param cluster_type: pp for local Parallel Python, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param pp_cpus: the number of CPU used by Parallel Python.
        :param runs: the number of model simulation
        """
        pass

    def ps2(self, model, sim_length, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        """
        Double paramter scan.
        
        :param model: the model to process
        :param sim_length: the length of the simulation
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        :param cluster_type: pp for local Parallel Python, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param pp_cpus: the number of CPU used by Parallel Python.
        :param runs: the number of model simulation
        """
        pass

    def pe(self, model, inputdir, cluster_type, pp_cpus, nfits, outputdir, sim_data_dir,
           updated_models_dir):
        """
        parameter estimation.
        
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param cluster_type: pp for parallel python, lsf for load sharing facility, sge for sun grid engine
        :param pp_cpus: the number of cpu for parallel python
        :param nfits: the number of fits to perform
        :param outputdir: the directory to store the results
        :param sim_data_dir: the directory containing the simulation data sets
        :param updated_models_dir: the directory containing the models with updated parameters for
               each estimation
        """
        pass

    def collect_pe_results(self, inputdir, outputdir, fileout_all_fits, file_out_best_fits):
        """
        Collect the parameter estimation results in two files.

        :param inputdir: input folder containing the independent parameter estimation files
        :param outputdir: the output folder to store the new files to create
        :param fileout_all_fits: a global file containing all fits from the independent parameter estimations.
        :param file_out_best_fits: a global file containing the best fits from the independent parameter estimations.
        """
        pass