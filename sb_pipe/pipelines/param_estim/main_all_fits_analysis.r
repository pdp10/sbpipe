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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-01 14:14:32 $


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(file.path(SB_PIPE, 'sb_pipe','pipelines','param_estim','param_estim_utils.r'))



# R Script to run model parameter estimation analysis and plot results. This script analyses
# all fits.
#
# :args[1]: the model name without extension.
# :args[2]: the dataset containing the parameter estimation data.
# :args[3]: the directory to save the generated plots.
# :args[4]: the number of data points used for parameterise the model.
# :args[5]: the name of the file containing the detailed statistics for the estimated parameters.
# :args[6]: the name of the file containing the summary for the parameter estimation.
# :args[7]: true if the 2D parameter correlation plots for 66% confidence intervals should be plotted.
# :args[8]: true if the 2D parameter correlation plots for 95% confidence intervals should be plotted.
# :args[9]: true if the 2D parameter correlation plots for 99% confidence intervals should be plotted.
# :args[10]: true if parameters should be plotted in logspace.
# :args[11]: true if axis labels should be plotted in scientific notation.
main <- function(args) {
  
  model <- args[1]
  dataset <- args[2]
  plots_dir <- args[3]
  data_point_num <- args[4]
  fileout_param_estim_details <- args[5]
  fileout_param_estim_summary <- args[6]
  plot_2d_66cl_corr <- args[7]
  plot_2d_95cl_corr <- args[8]
  plot_2d_99cl_corr <- args[9]  
  logspace <- args[10]
  scientific_notation <- args[11]
  
  if(plot_2d_66cl_corr == 'True' || plot_2d_66cl_corr == 'TRUE' || plot_2d_66cl_corr == 'true') {
    plot_2d_66cl_corr = TRUE
  } else {
    plot_2d_66cl_corr = FALSE
  }

  if(plot_2d_95cl_corr == 'True' || plot_2d_95cl_corr == 'TRUE' || plot_2d_95cl_corr == 'true') {
    plot_2d_95cl_corr = TRUE
  } else {
    plot_2d_95cl_corr = FALSE
  }

  if(plot_2d_99cl_corr == 'True' || plot_2d_99cl_corr == 'TRUE' || plot_2d_99cl_corr == 'true') {
    plot_2d_99cl_corr = TRUE
  } else {
    plot_2d_99cl_corr = FALSE
  }  
  
  if(logspace == 'True' || logspace == 'TRUE' || logspace == 'true') {
    logspace = TRUE
  } else {
    logspace = FALSE
  }
  
  if(scientific_notation == 'True' || scientific_notation == 'TRUE' || scientific_notation == 'true') {
    scientific_notation = TRUE
  } else {
    scientific_notation = FALSE
  }  
  
  all_fits_analysis(model, dataset, plots_dir, data_point_num, fileout_param_estim_details, 
                    fileout_param_estim_summary, plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr, 
                    logspace, scientific_notation)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )

