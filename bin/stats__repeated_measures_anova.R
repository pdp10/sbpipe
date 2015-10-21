# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either model_noext 2 of the License, or (at
# your option) any later model_noext.
#    
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
# Object: perform repeated measures anova
# Run: Rscript rep_meas_anova.R > fileout.txt
#
# Institute for Ageing and Health
# Newcastle University
# Newcastle upon Tyne
# NE4 5PL
# UK
# Tel: +44 (0)191 248 1106
# Fax: +44 (0)191 248 1101
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $



# Retrieve the environment variable PROJ_LIB
#PROJ_LIB <- Sys.getenv(c("PROJ_LIB"))
# Add a collection of R functions
#source(paste(PROJ_LIB, "/R/plot_functions.R", sep=""))





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












