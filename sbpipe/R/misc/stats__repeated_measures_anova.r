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
# $Date: 2015-07-7 16:14:32 $



# Perform repeated measures anova on a file containing data. 
# This file contains control and treatment. 
# Structure: TREATMENT (0,1) | time point | sample No. | result
# where (0,1) in TREATMENT means (no-treatment,treatment).
#
# :param args[1]: the file to process
main <- function(args) {
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












