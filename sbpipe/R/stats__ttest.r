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
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-7 16:14:32 $



# symmetry test
library(lawstat) 


# Perform two samples statistical tests. 
#
# :args[1] filename: the filename containing the data
main <- function(args) {
    # The name of the file to import controls and treatment. 
    # Structure: CTRL_A|TRMT_A|CTRL_B|TRMT_B|...|CTRL_M|TRMT_M
    filename <- args[1]
  
    
    #fileout_name<-"fileout.txt";


    # import the input file
    my_table<-read.table(filename,header=TRUE,sep='\t',na.strings="NA")
    # Open the file output

    #unlink(fileout_name)
    #fileout<-file(fileout_name)
    # Write the data inside the output file
    #writeLines(my_table,fileout)
    #write.table(my_table,fileout,append=TRUE,sep='\t',col.names=TRUE,row.names=FALSE)
    print(my_table)


    # interate on the control columns only
    for(i in seq(1,ncol(my_table),2)) {


	  control_header<-colnames(my_table)[i]
	  treatment_header<-colnames(my_table)[i+1]
	  control<-my_table[[i]]
	  treatment<-my_table[[i+1]]


	  cat("\n\n\n\n\n\n\n\n\n\n")
	  print("########################################")
	  print(paste("control:", control_header, sep=" "));
	  print(paste("treatment:", treatment_header, sep=" "));
	  print("########################################")
	  cat("\n")


	  print("###################################")
	  print("SYMMETRY TEST ABOUT UNKNOWN MEDIAN:")
	  print("###################################")
	  my_symtest<-symmetry.test(control-treatment)
	  print(my_symtest)
	  
	  
	  print("###############")
	  print("NORMALITY TEST:")
	  print("###############")
	  # Normality test (p-value < 0.05 could suggest there is eveidence of non-normality, but p>0.05 just shows a lack of evidence).
	  # Shapiro's normality test (small size sample)
	  #my_st_ctrl<-shapiro.test(control)
	  #print(my_st_ctrl)
	  my_st_trmt<-shapiro.test(treatment)
	  print(my_st_trmt)
	  # Kolmogorow-Smirnov's normality test (big size sample)
	  my_kst<-ks.test(control,treatment)
	  print(my_kst)


	  print("####################")
	  print("PARARAMETRIC T-TEST:")
	  print("####################")
	  # IF ctrl AND treatment ARE normally distributed => parametric t-test is sufficient
	  # We can test for significant differences in the variances
	  my_vt<-var.test(control,treatment)
	  print(my_vt)
	  # and if the previous test is negative, we can also assume equality of the variances.
	  my_tt_vareq<-t.test(control,treatment,var.equal=TRUE)
	  print('The following parametric t-test assumes `equality of the variances` test as computed above')
	  print(my_tt_vareq)
	  # By default, R DOES NOT assume equality of variances in t.test(). So, this is more general:
	  my_tt_varineq<-t.test(control,treatment)
	  print(my_tt_varineq)


	  print("######################")
	  print("NON-PARAMETRIC T-TEST:")
	  print("######################")
	  # IF ctrl AND treatment ARE NOT normally distributed => non parametric t-test (Wilcoxon-Mann-Whitney test)
	  print('PAIRED=FALSE') # consider this generally
	  my_wt<-wilcox.test(control,treatment,correct=FALSE,exact=FALSE,alternative="less")
	  print(my_wt)
	  my_wt<-wilcox.test(control,treatment,correct=FALSE,exact=FALSE,alternative="greater")
	  print(my_wt)

	  my_wt<-wilcox.test(control,treatment,correct=FALSE,exact=FALSE,alternative="two.sided")
	  print(my_wt)	  
	  
	  print('PAIRED=TRUE')
	  my_wt<-wilcox.test(control,treatment,paired=TRUE,correct=FALSE,exact=FALSE,alternative="less")
	  print(my_wt)
	  my_wt<-wilcox.test(control,treatment,paired=TRUE,correct=FALSE,exact=FALSE,alternative="greater")
	  print(my_wt)	  



	  # Write test results on file
	  #writeLines("",fileout)
	  #writeLines("",fileout)
	  #writeLines("",fileout)
	  #writeLines(c("########################################",paste("control=", control_header, sep=" "),paste("treatment:", treatment_header, sep=" "),"########################################"),fileout)
	  #writeLines(c("########################################","NORMALITY TEST:","########################################"),fileout)
	  #writeLines(my_st_ctrl,fileout)
	  #writeLines(my_st_trmt,fileout)
	  #writeLines(my_kst,fileout)
	  #writeLines(c("########################################","PARARAMETRIC AND NON-PARAMETRIC T-TEST:","########################################"),fileout)
	  #writeLines(my_tt_varineq,fileout)
	  #writeLines(my_vt,fileout)
	  #writeLines(my_tt_vareq,fileout)
	  #out<-capture.output(my_wt)
	  #write(out,fileout)
	  

    }


    #close(fileout)
}
    
    
    

main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())



