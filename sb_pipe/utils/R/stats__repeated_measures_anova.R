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
# Object: perform repeated measures anova
# Run: Rscript rep_meas_anova.R > fileout.txt
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-7 16:14:32 $



# Retrieve the environment variable SB_PIPE
#SB_PIPE <- Sys.getenv(c("SB_PIPE"))
# Add a collection of R functions
#source(file.path(SB_PIPE, 'utils','R','plot_functions.R'))





main <- function(args) {
    # The name of the file to import controls and treatment. 
    # Structure: TREATMENT (0,1) | time point | sample No. | result
    filename <- args[1]
  

    cat("\n")  
    print("########################")
    print("REPEATED MEASURES ANOVA:")
    print("########################")
    cat("\n\n")    
    # import the input file    
    rep_meas_anova = read.table(filename,header=TRUE,sep='\t',na.strings="NA")
    print(rep_meas_anova)
    cat("\n\n")
	  
    attach(rep_meas_anova)
    rep_meas_anova = within(rep_meas_anova, {
      timepoint = factor(timepoint)
      sample = factor(sample)
      treatment = factor(treatment)
    })
    rep_meas_anova.aov = aov(rep_meas_anova$result~timepoint+sample+treatment)
    summary (rep_meas_anova.aov)


    rep_meas_anova.aov = aov(rep_meas_anova$result~timepoint+sample+treatment+treatment*timepoint)
    summary (rep_meas_anova.aov)



}
    
    
    

main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())












