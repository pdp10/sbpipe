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
# Object: A collection of functions
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-15 16:14:32 $

require(graphics)




plot_calibration_mean_ci <- function(folder, filein, fileout, best_pos, best_score, nsamples, colour, identifier) {
  library(gplots)
  dataset <- read.table(file.path(folder, filein), header=TRUE, na.strings="NA", dec=".", sep="\t")
  iteration <- dataset$Iterations
  # plot mean line with 95% CI
  png ( file.path(folder, fileout), height=760, width=800, bg="white" ) #bg="transparent")
  # increase the margin on the right of the plot
  par(mar=c(5,6,4,2)+0.1)
  plotCI(x=iteration,
       y=dataset$Mean,
       ui=dataset$CI_95_sup,
       li=dataset$CI_95_inf,
       err="y",
       col=colour, barcol=colour,
       type="l", # line
       xlim=c(0,max(iteration)),
       ylim=c(0,max(dataset$Mean) + max(dataset$Mean)/3),
       labels=FALSE,
       xlab="Iteration", ylab="Sum of Square Errors (using Simulated Annealing)",
       main="Model Calibration by Experimental Data",
       #las=1,  # always parallel axes
       cex.main=3.5, cex.lab=3.0, cex.axis=2.2,cex=2.2,lwd=1,
       gap=0.0)
  lines(x=iteration,y=dataset$Best_Calib, lwd=4, type="l", col="red")
  legend("topright", c(paste(identifier, " - Mean \u{00B1} t-distribution CI 95% (", nsamples, " samples)", sep=""), paste("Calibration fitting best the data (Sum of Sq. Err.: ", best_score, ")", sep="")), cex=2.2, lty=1, lwd=4, bty="n", col=c("black", "red"))
  box()
  dev.off() 
}


# As plot_calibration_mean_ci, but plots multi means+/- CI
# colour, identifier, nsamples and filein are lists
plot_calibration_mean_ci_multi <- function(folder, filein, fileout, best_pos, best_score, nsamples, colour, identifier) {
  library(gplots)
  # plot mean line with 95% CI
  png ( file.path(folder, fileout), height=760, width=800, bg="white" ) #bg="transparent")
  # increase the margin on the right of the plot
  par(mar=c(5,6,4,2)+0.1)
  lege <- c()
  dataset <- c()
  iteration <- c()
  for(i in 1:length(filein)) {
	# required one plot before the added others! (see opt: add=TRUE)
      if (i == 1) { 
	  dataset <- read.table(file.path(folder, filein[i]), header=TRUE, na.strings="NA", dec=".", sep="\t")
	  iteration <- dataset$Iterations
	  plotCI(x=iteration,
       		y=dataset$Mean,
       		ui=dataset$CI_95_sup,
       		li=dataset$CI_95_inf,
       		col=colour[i], barcol=colour[i],
       		#type="l", # line
       		xlim=c(0,max(iteration)),
       		ylim=c(0,max(dataset$Mean) + max(dataset$Mean)/3),
       		labels=FALSE,
       		xlab="Iteration", ylab="Sum of Square Errors",
       		main="Model Calibration by Experimental Data",
       		#las=1,  # always parallel axes
       		cex.main=3.5, cex.lab=3.0, cex.axis=2.2,cex=2.2,lwd=1,
       		gap=0.0)
	  lege = c(lege, paste(identifier[i], " - Mean \u{00B1} t-distrib CI 95% (", nsamples[i], " samples)", sep=""))
      } else {
  	dataset <- read.table(file.path(folder, filein[i]), header=TRUE, na.strings="NA", dec=".", sep="\t")
  	iteration <- dataset$Iterations
  	plotCI(x=iteration,
       		y=dataset$Mean,
       		ui=dataset$CI_95_sup,
       		li=dataset$CI_95_inf,
       		col=colour[i], barcol=colour[i],
       		#type="l", # line
       		xlim=c(0,max(iteration)),
       		ylim=c(0,max(dataset$Mean) + max(dataset$Mean)/3),
       		labels=FALSE,
       		xlab="Iteration", ylab="Sum of Square Errors",
       		main="Model Calibration by Experimental Data",
       		#las=1,  # always parallel axes
       		cex.main=3.5, cex.lab=3.0, cex.axis=2.2,cex=2.2,lwd=1,
       		add=TRUE, gap=0.0)
	lege = c(lege, paste(identifier[i], " - Mean \u{00B1} t-distrib CI 95% (", nsamples[i], " samples)", sep=""))
      }
  }
  lege = c(lege, paste("Calibration fitting best the data (Sum of Sq. Err.: ", best_score, ")", sep=""))
  lines(x=iteration,y=dataset$Best_Calib, lwd=4, type="l", col="red")
  legend("topright", lege, cex=2.2, lty=1, lwd=4, bty="n", col=c(colour[1:length(filein)], "red"))
  box()
  dev.off() 
}



# plot sensitivity sens_matrix by row in a multi plot
plot.sensitivities <- function(filename, kinetics) {
  sens_matrix <- read.table(filename, header=TRUE, row.names=1, na.strings="NA", dec=".", sep="\t")
  #print(sens_matrix)
  model <- ""
  
  names.row <- row.names(sens_matrix)
  names.col <- names(sens_matrix)
  if(kinetics==FALSE) {
    names.row <- substr(names.row,2, nchar(names.row)-1)
    names.col <- substr(names.col,3, nchar(names.col)-3)
    #names.col <- gsub("unknown", "x", names.col)
    #names.row <- gsub("unknown", "x", names.row)
    #print(names.row)
    #print(names.col)
    png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), height=1000, width=1000, bg="transparent") 
    heatmap.2(as.matrix(sens_matrix), 
	   key=TRUE, keysize=0.6, symkey=TRUE, 
	   density.info="none", 
           trace="none", 
	   col=diverge_hcl(256), #c=130, l=c(30,95)),
	   #col=diverge_hsv(256),
           dendrogram="none",
 	   Rowv=NA, Colv=NA, na.rm,
           colsep=c(1:(length(names.col)-1)),
           rowsep=c(1:(length(names.row)-1)),
           sepcolor="white",
           sepwidth=c(0.01,0.01),
 	   scale="none",
 	   labRow=names.row, labCol=names.col, 
 	   margins=c(19,19), cex.main=5, cexRow=2, cexCol=2,
 	   main = paste("Initial concentrations sensitivities  -  ", model, sep=""))
  } else{
    names.row <- substr(names.row,2, nchar(names.row)-1)
    names.col <- substr(names.col,3, nchar(names.col)-4)
    names.col <- gsub("phosphorylation", "phosp", names.col)
    #names.col <- gsub("unknown", "x", names.col)
    #names.row <- gsub("unknown", "x", names.row)
    #print(names.row)
    #print(names.col)
    png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), height=1200, width=1200, bg="transparent") 
    heatmap.2(as.matrix(sens_matrix), 
	   key=TRUE, keysize=0.6, symkey=TRUE, 
	   density.info="none", 
           trace="none", 
	   col=diverge_hcl(256), #, c=130, l=c(30,95)),
	   #col=diverge_hsv(256),
           dendrogram="none",
 	   Rowv=NA, Colv=NA, na.rm,
           colsep=c(1:(length(names.col)-1)),
           rowsep=c(1:(length(names.row)-1)),
           sepcolor="white",
           sepwidth=c(0.01,0.01),
 	   scale="none",
 	   labRow=names.row, labCol=names.col, 
 	   margins=c(36,19), cex.main=5, cexRow=2, cexCol=2,
 	   main = paste("Kinetic rates sensitivities  -  ", model, sep=""))
  }

  dev.off()
}



# plot the parameter correlation matrix corr_matrix by row in a multi plot
plot.param_correlations <- function(filename, valmargin, valcex) {
  corr_matrix <- read.table(filename, header=TRUE, row.names=1, na.strings="NA", dec=".", sep="\t")
  #print(corr_matrix)
  model <- ""
  names.row <- row.names(corr_matrix)
  names.col <- names(corr_matrix)
  names.row <- gsub("phosphorylation", "phosp", names.row)
  names.col <- gsub("phosphorylation", "phosp", names.col)
  #names.row <- substr(names.row,2, nchar(names.row)-5)
  #names.col <- substr(names.col,3, nchar(names.col)-5)
  #names.col <- gsub("unknown", "x", names.col)
  #names.row <- gsub("unknown", "x", names.row)
  #print(names.row)
  #print(names.col)
  abs_matrix <- abs(as.matrix(corr_matrix))
  if(model=="General model (phase 2)") {
    png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), height=1800, width=1800, bg="white") 
    heatmap.2(abs_matrix, 
	   key=TRUE, keysize=0.6, symkey=FALSE, 
	   density.info="none", 
           trace="none",
	   denscol="blue",
	   col=rev(c(gray.colors(256) )), # add black "1"
	   symm=TRUE,
           dendrogram="none",
 	   Rowv=NA, Colv=NA, na.rm=TRUE,
 	   scale="none",

           colsep=c(1:(length(names.col)-1)),
           rowsep=c(1:(length(names.row)-1)),
           sepcolor="white",
           sepwidth=c(0.01,0.01),

 	   labRow=names.row, labCol=names.col, 
 	   margins=c(60,60), cex=3, cexRow=3.5, cexCol=3.5,
 	   main = paste("Parameters Correlation Matrix  -  ", model, sep=""))
  } else {

   
   png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), width=11, height=11, units="in", res=300, bg="white")
 
   #tiff(file="test.tiff",width=11, height=11, units="in", res=300)   
    
    heatmap.2(abs_matrix, 
# # 	   key=false, 
# #	   keysize=0.4, 
	   symkey=FALSE, densadj=0.20,
	   density.info="none", 
           trace="none",
	   tracecol="blue",
	   #col=rev(c(gray.colors(256))), # add black "1"
	   col=rev(c("1",  gray.colors(256))), # add black "1"
	   symm=TRUE,
           dendrogram="none",
 	   Rowv=NA, Colv=NA, na.rm=TRUE,
 	   scale="none",

           colsep=c(1:(length(names.col)-1)),
           rowsep=c(1:(length(names.row)-1)),
           sepcolor="white",
           sepwidth=c(0.01,0.01),

  	   labRow=names.row, labCol=names.col, 
# # # 	   margins=c(73,73), cex=3.5, cexRow=3.5, cexCol=3.5,

####### Default
#  	   margins=c(21,21), 
# 	   cex=0.9, cexRow=0.9, cexCol=0.9,

####### Change the values below to adjust it
	   margins=c(valmargin,valmargin), 
	   cex=valcex, cexRow=valcex, cexCol=valcex,

 	   main = paste("Parameters Correlation Matrix  -  ", model, sep=""))
  }
  dev.off()
}


