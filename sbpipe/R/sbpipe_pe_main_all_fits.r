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
# $Date: 2016-07-01 14:14:32 $


# retrieve SBpipe folder containing R scripts
args <- commandArgs(trailingOnly = FALSE)
SBPIPE_R <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))
source(file.path(SBPIPE_R, 'sbpipe_pe.r'))




# R Script to run model parameter estimation analysis and plot results. This script analyses
# all fits.
#
# :args[1]: the model name without extension.
# :args[2]: the dataset containing all the parameter fits
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
  allfits_filenamein <- args[2]
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
  


  dim_all_fits = dim(read.table(allfits_filenamein, header=TRUE, sep="\t"))[1]

  if(dim_all_fits-1 <= 0) {
      warning('All fits analysis requires at least one parameter set. Cannot continue.')
      stop()
  }

  df_all_fits = read.table(allfits_filenamein, header=TRUE, dec=".", sep="\t")

  # non-positive entries test
  # If so, logspace will be set to FALSE, otherwise SBpipe will fail due to NaN values.
  # This is set once for all
  nonpos_entries <- sum(df_all_fits <= 0)
  if(nonpos_entries > 0) {
      warning('Non-positive values found for one or more parameters. `logspace` option set to FALSE')
      logspace = FALSE
  }

  all_fits_analysis(model, df_all_fits, plots_dir, data_point_num, fileout_param_estim_details,
                    fileout_param_estim_summary, plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
                    logspace, scientific_notation)

}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )

