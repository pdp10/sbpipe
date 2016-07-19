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
# Object: Plotting of the confidence intervals
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-01 14:14:32 $


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(file.path(SB_PIPE, 'sb_pipe','pipelines','sb_param_estim__copasi','param_estim_utils.r'))


main <- function(args) {
  
  filename <- args[1]
  plots_dir <- args[2]
  data_point_num <- args[3]
  fileout_approx_ple_stats <- args[4]
  fileout_conf_levels <- args[5]
  plot_2d_66_95cl_corr <- args[6]
  
  if(plot_2d_66_95cl_corr == 'True' || plot_2d_66_95cl_corr == 'TRUE' || plot_2d_66_95cl_corr == 'true') plot_2d_66_95cl_corr = TRUE
  else plot_2d_66_95cl_corr = FALSE

  all_fits_analysis(filename, plots_dir, data_point_num, fileout_approx_ple_stats, fileout_conf_levels, plot_2d_66_95cl_corr)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )

