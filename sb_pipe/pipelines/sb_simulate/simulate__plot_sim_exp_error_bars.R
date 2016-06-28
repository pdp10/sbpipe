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
# Object: Plotting of the confidence intervals
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2009-01-15 16:14:32 $


# IMPORTANT:
# files containing timecourses MUST contain the timepoints declared in the variable timepoints 


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(paste(SB_PIPE, "/sb_pipe/utils/R/plot_sim_exp_func.R", sep=""))



main <- function(args) {
    # The model model_noext
    model_noext <- args[1]
    inputdir_sim <- args[2]
    inputdir_exp <- args[3]
    outputdir <- args[4]
    file_sim <- args[5]
    file_exp <- args[6]

    
    
    # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }

    # Read species
    sim_stat <- read.table ( paste ( inputdir_sim, file_sim, sep="" ), header=TRUE, na.strings="NA", dec=".", sep="\t" )
    sim_column <- names(sim_stat)
    exp_stat <- read.table ( paste ( inputdir_exp, file_exp, sep="" ), header=TRUE, na.strings="NA", dec=".", sep="\t" )
    exp_column <- names(exp_stat)
    # A lookup table for computational-experimental comparison
    lookup_table = matrix( 
	c("IR_beta_pY1146","IR_beta_Y1146",
	  "Akt_pT308", "Akt_p308",
	  "Akt_pT308_pS473", "Akt_p473",
	  "mTORC2_pS2481", "mTOR_p2481",
	  "mTORC1_pS2448", "mTOR_p2448",  
	  "PRAS40_pT246", "PRAS40_T246",
	  "PRAS40_pS183", "PRAS40_S183",
	  "p70S6K_pT389", "S6K_p389",
	  "IRS1_pS636_PI3K", "IRS_S636"),
	ncol=2,
	byrow=TRUE)

    #results contains the total_chi_square, and the total_timepoints
    results <- sim_exp_error_bars_main(sim_stat, sim_column, exp_stat, exp_column, outputdir, model_noext, lookup_table)
    print(results)
    write.csv(results, file=paste(results_dir, "/fitting_statistics_", model_noext,".csv",sep=""), sep="\t") 
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())
