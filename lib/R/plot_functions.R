# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should hade received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
# Object: A collection of functions
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
# $Date: 2010-06-15 16:14:32 $

require(graphics)

# plot a single time course (continue time, discrete time, boxplot)
plot_single_timecourse <- function(timecourses, outputdir, version, name, timepoints, linewidth) {
    # compute a vector of selected timepoints (used for discrete time plots)
    seltp <- c()
    l <- 1
    for (k in 1:length(timecourses[,c(name)])) {
      if(l <= length(timepoints) &&
	k == timepoints[l]) {
	seltp <- c(seltp, timecourses[,c(name)][k])
	l <- l + 1
      }	      
    }
    # discrete time
    png ( paste ( outputdir, version, "_disc_tc_", name, ".png", sep="" ), height=760, width=800, bg="white" ) #bg="transparent")
				      # increase the margin on the right of the plot
    par(mar=c(5,6,4,2)+0.1)
    matplot( x=c(1:length(timepoints)), y=c(seltp),
	    #type="l",
	    lty=1, pch=21, 
	    xlab="Time (min)", ylab="Relative Phosphorylation Level",
	    xlim=c(1,length(timepoints)),
	    ylim=c(0,max(timecourses[,c(name)])+ max(timecourses[,c(name)])/10 ),
	    main=paste(name, " Time Course", sep="" ),
	    cex.main=3,
	    #las=1,
	    cex.main=3.5, cex.lab=3.0, cex.axis=2.2, cex=2.2,xaxt="n", lwd=linewidth)
    axis(side=1, labels=timepoints, at=c(1:length(timepoints)), cex.axis=1.5)
    legend("topright", name, cex=2.2, lty=1, lwd=linewidth)   # col=c("blue","red","green")
    box()
    dev.off ( )       # empty the device      

    # continuous time
    png ( paste ( outputdir, version, "_cont_tc_", name, ".png", sep="" ), height=760, width=800, bg="white" ) #bg="transparent")
					    # increase the margin on the right of the plot
    par(mar=c(5,6,4,2)+0.1)
    matplot( x=timecourses$Time, y=timecourses[, c(name)],
	    type="l", lty=1,
	    xlab="Time (min)", ylab="Relative Phosphorylation Level",
	    ylim=c(0,max(timecourses[,c(name)])+max(timecourses[,c(name)])/10 ),
	    main=paste(name, " Time Course", sep="" ),
	    #las=1,
	    cex.main=3.5, cex.lab=3.0, cex.axis=2.2, cex=2.2, pch=".", lwd=linewidth )
    legend("topright", name, cex=2.2, lty=1, lwd=linewidth)   # col=c("blue","red","green")
    box()      
    dev.off ( )       # empty the device

    # column[j] boxplot
    png ( paste ( outputdir, version, "_bp_", name, ".png", sep="" ), height=760, width=800, bg="white" ) #bg="transparent")
					    # increase the margin on the right of the plot
    par(mar=c(5,6,4,2)+0.1)
    boxplot( timecourses[, c(name)],
	    main=paste ( name, " Boxplot", sep="" ),
	    #las=1,
	    cex.main=3.5, cex.lab=3.0, cex.axis=2.2, cex=2.2,
	    ylim=c(0,max(timecourses[,c(name)])),
	    ylab="Relative Phosphorylation Level", pch=".", lwd=linewidth )
    axis(side=1, labels=name, at=c(1:1), cex.axis=2.2)
    box()
    dev.off ( )
}



# It plots experimental time courses singlularly
plot_experimental_timecourse <- function(outputdir, file_exp, exp, name, timepoints, linewidth) {
    # plot of the discrete time courses of the three experiments
    png(paste(outputdir,substr(file_exp[1], 1, 3),"_multi_disc_tc_",name,".png",sep=""), height=580, width=600, bg="white" )
    xaxis <- c(1:length(timepoints))
    ylab <- "Relative Phosphorylation Activity (%)"
    exp1 <- exp[[1]][[name]] 
    exp2 <- exp[[2]][[name]] 
    exp3 <- exp[[3]][[name]]
    maximum <- max(exp1, exp2, exp3)
    ylim <- c(0.0, maximum + maximum/4)
    # Always plot lines choosing the biggest as first   (add lwd=2 to increase the line thickness)
    matplot(x=xaxis, y=exp1, xlab="Time (min)",  #las=1,
	    ylab=ylab, type="o", pch=21, lty=1,
	    main=paste(name, " Time Courses (experimental)", sep=""),
	    ylim=ylim, xaxt="n", cex.main=2, cex.lab=1.5, cex.axis=1.2, lwd=linewidth) # col="blue"
    lines( x=xaxis, y=exp2, type="o", pch=22, lty=2, lwd=linewidth ) # col="red"
    lines( x=xaxis, y=exp3, type="o", pch=23, lty=3, lwd=linewidth ) # col="green"
    #lines( x=xaxis, y=exp4, type="o", pch=24, lty=4 ) # col="orange"
    axis(side=1, labels=timepoints, at=xaxis, cex.axis=2.2)
    legend("topright", c("1st repeat","2nd repeat","3rd repeat"), pch=21:23, cex=2.2, lty=1:3, lwd=linewidth)   # col=c("blue","red","green","orange")
    box()
    dev.off ( )

    # plot of the continuous time courses of the three experiments
    xaxis <- exp[[1]]$Time
    png (paste(outputdir,substr(file_exp[1], 1, 3),"_multi_cont_tc_",name,".png",sep=""), height=580, width=600, bg="white" )
    # Always plot lines choosing the biggest as first   (add lwd=2 to increase the line thickness)
    matplot( x=xaxis, y=exp1, xlab="Time (min)", ylab=ylab,
	    type="o", pch=21, lty=1, main=paste(name, " Time Courses (experimental)", sep=""),
	    ylim=ylim, cex.main=3.5, cex.lab=3.0, cex.axis=2.2, cex=2.2, lwd=linewidth ) # col="blue"
    lines( x=xaxis, y=exp2, type="o", pch=22, lty=2, lwd=linewidth ) # col="red"
    lines( x=xaxis, y=exp3, type="o", pch=23, lty=3, lwd=linewidth ) # col="green"
    #lines( x=xaxis, y=exp4, type="o", pch=24, lty=4 ) # col="orange"
    legend("topright", c("1st repeat","2nd repeat","3rd repeat"), pch=21:23, cex=2.2, lty=1:3, lwd=linewidth)   # col=c("blue","red","green","orange")
    box()
    dev.off ( )

    # Boxplot of three experiments
    png (paste(outputdir, substr( file_exp[1], 1, 3 ), "_multi_bp_", name, ".png", sep="" ), height=580, width=600, bg="white" )
    boxplot(exp1, exp2, exp3, #las=1,
	    main=paste(name, " Boxplot (experimental)", sep="" ),pch=".",
	    ylim=ylim, ylab=ylab, cex.main=3.5, cex.lab=3.0, cex.axis=2.2, cex=2.2,lwd=1, lwd=linewidth)
    axis(side=1, labels=c("1st repeat","2nd repeat","3rd repeat"), at=c(1:3), cex.axis=2.2)
    box()
    dev.off ( )
}


# Plot the correlation of two time courses
plot.correlation <- function(filename, first, second, first.name, second.name, linewidth) {
  maximum <- max(first, second)
  ylim <- c(0.0, maximum + maximum/4)
  png (filename, height=580, width=600, bg="white" )
  plot(first, second,
       main=paste("Corr. ", first.name, " vs ", second.name, sep=""),
       cex.main=3.5, cex.lab=3.0, cex.axis=2.2,cex=2.2,lwd=1, ylim=ylim, pch=21, xlab=first.name, ylab=second.name, lwd=linewidth)
  legend("topleft", paste("spearman's corr: ", round(cor(first, second, method="spearman"), 6),sep=""), cex=2.2, lwd=2)
  abline(lm(second~first),lwd=2)
  box()
  dev.off ( )
}



plot_calibration_mean_ci <- function(folder, filein, fileout, best_pos, best_score, nsamples, colour, identifier) {
  library(gplots)
  dataset <- read.table(paste(folder, filein, sep=""), header=TRUE, na.strings="NA", dec=".", sep="\t")
  iteration <- dataset$Iterations
  # plot mean line with 95% CI
  png ( paste(folder, fileout, sep=""), height=760, width=800, bg="white" ) #bg="transparent")
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
  png ( paste(folder, fileout, sep=""), height=760, width=800, bg="white" ) #bg="transparent")
  # increase the margin on the right of the plot
  par(mar=c(5,6,4,2)+0.1)
  lege <- c()
  dataset <- c()
  iteration <- c()
  for(i in 1:length(filein)) {
	# required one plot before the added others! (see opt: add=TRUE)
      if (i == 1) { 
	  dataset <- read.table(paste(folder, filein[i], sep=""), header=TRUE, na.strings="NA", dec=".", sep="\t")
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
       		xlab="Iteration", ylab="Sum of Square Errors (using Simulated Annealing)",
       		main="Model Calibration by Experimental Data",
       		#las=1,  # always parallel axes
       		cex.main=3.5, cex.lab=3.0, cex.axis=2.2,cex=2.2,lwd=1,
       		gap=0.0)
	  lege = c(lege, paste(identifier[i], " - Mean \u{00B1} t-distrib CI 95% (", nsamples[i], " samples)", sep=""))
      } else {
  	dataset <- read.table(paste(folder, filein[i], sep=""), header=TRUE, na.strings="NA", dec=".", sep="\t")
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
       		xlab="Iteration", ylab="Sum of Square Errors (using Simulated Annealing)",
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
  if(length(grep("pi3k_indep", filename, value=TRUE)) > 0) {
    model <- "PI3K-indep hypothesis"
  } else if(length(grep("pi3k_dep", filename, value=TRUE)) > 0) {
    model <- "PI3K-dep hypothesis"
  } else if(length(grep("pi3k_iso_dep", filename, value=TRUE)) > 0) {
    model <- "PI3K-iso-dep hypothesis"
  } else if(length(grep("tsc_dep", filename, value=TRUE)) > 0) {
    model <- "TSC-dep hypothesis"
  }
  
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
  if(length(grep("pi3k_indep", filename, value=TRUE)) > 0) {
    model <- "PI3K-indep hypothesis (phase 6)"
  } else if(length(grep("pi3k_dep", filename, value=TRUE)) > 0) {
    model <- "PI3K-dep hypothesis (phase 5)"
  } else if(length(grep("pi3k_iso_dep", filename, value=TRUE)) > 0) {
    model <- "PI3K-iso-dep hypothesis (phase 7)"
  } else if(length(grep("tsc_dep", filename, value=TRUE)) > 0) {
    model <- "TSC-dep hypothesis (phase 4)"
  } else if(length(grep("ir_beta", filename, value=TRUE)) > 0) {
    model <- "IR-Beta (phase 1)"
  } else if(length(grep("without_pdk2", filename, value=TRUE)) > 0) {
    model <- "General model (phase 2)"
  } else if(length(grep("with_pdk2", filename, value=TRUE)) > 0) {
    model <- "General model with PDK2 (phase 3)"
  }
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





# Create a legend for name with range between min, max of n values.
make_legend <- function(path, name, min, max, values, inhibition_only, perturbation_in_percent_levels) {
    if(as.numeric(max) > as.numeric(min)) {
      scale <- seq(as.numeric(min), as.numeric(max), as.numeric(max)/(as.numeric(values)))
      
      
      scale <- seq(as.numeric(min), as.numeric(max), (as.numeric(max)-as.numeric(min))/(as.numeric(values)-1))      
      
      # Instead of a knock out, apply a minimal knock down 
      # (for graphical visualisation too.
      #scale[1] <- 1
      # plot design configuration
      colors <- c()
      linetype <- c()
      
      
      if(perturbation_in_percent_levels == "true") {
	# The model is perturbed using a virtual species (A_percent_level) defining the percent level of its corresponding real species (A). 
	# The perturbation is therefore done by percent levels and at the beginning.
	# NOTE: A_percent_level=0  ==> A is knocked out (so 0%)
	if(inhibition_only == "true") {
	  # THIS PALETTE OF COLOURS can be used for gradual inhibition only (blue [10,100])
	  # Including knockout (first number is knock out (bright blue), last number 24 is control (black))  (0%,10%,20%,..,100%)
	  # In linetype: 1 is a full line	    
	  #colors <- colors()[c(128,129,130,131,132,26,27,28,29,30,24)] 
	  #linetype <- c(1,6,4,3,2,1,6,4,3,2,1)
	  # Excluding knockout (10%,20%,..,100%)
	  colors <- colors()[c(129,130,131,132,26,27,28,29,30,24)]
	  linetype <- c(1,4,3,2,1,6,4,3,2,1)
	} else {
	  # THIS PALETTE OF COLOURS can be used for gradual inhibition and overexpression (blue [10,250])	  
	  # Including knockout (first number is knock out (bright blue), last number 96 is control (overexpression))  (0%,25%,50%,..,100%,125%,150%,..250%)
	  # In linetype: 1 is a full line	    
	  #colors <- colors()[c(27,28,29,30,24,99,115,95,98,97,96)]
	  #linetype <- c(5,4,3,2,1,6,5,4,3,2,6)
	  # Excluding knockout (25%,50%,..,100%,125%,150%,..,250%)	    
	  colors <- colors()[c(28,29,30,24,99,115,95,98,97,96)]
	  linetype <- c(4,3,2,1,6,5,4,3,2,6)
	}
      } else {
	# The model is perturbed using a virtual species (A_inhibitor) inhibiting its corresponding real species (A). 
	# In this case, the perturbation is on the inhibitor or expressor, and NOT on the species. In this case, the perturbation is done all over the time course.
	# NOTE 1: A_inhibitor=0  ==> A is not perturbed (so 100%)	    
	# NOTE 2: This case requires a preliminary approximation of the percentage of inhibited/expressed protein, and assume that this percentage is linear to the inhibitor/expressor.
	# NOTE 3: In this case, inhibition and overexpression are two separate perturbation. Although semantically incorrect, the second branch of the if-then-else clausole represents overexpression only.
	if(inhibition_only == "true") {
	  # THIS PALETTE OF COLOURS can be used for gradual inhibition only (blue [10,100])
	  # First number is 24 is control (black), last number (bright blue))  (100%,90%,80%,..,10%)
	  # In linetype: 1 is a full line	    
	  colors <- colors()[c(24,30,29,28,27,26,132,131,130,129)]
	  linetype <- c(1,2,3,4,6,1,2,3,4,1)
	  scale <- scale - as.numeric(min)
	} else {
	  # THIS PALETTE OF COLOURS can be used for gradual overexpression (magenta [100,250])	  
	  # First number is control (black), last number 96 is overexpression (magenta) (100%,115%,130%,..250%)
	  # In linetype: 1 is a full line
	  colors <- colors()[c(24,99,115,95,98,97,96,464,463,510)]
	  linetype <- c(1,2,3,4,1,2,3,4,6,1)
	}
      }
      
      scale <- round(scale, digits = 0)
      
      linewidth <- 8
      plotchar <- c()
      plottype <- "l" # "b"
      # increase the margin on the right of the plot
      par(mar=c(5,6,4,2)+0.1)
      png ( paste(path, "/", name,".png",sep=""), height=760, width=800, bg="transparent")
      par(font=2)
      plot(x=c(0), 
	  y=c(0),
	  type=plottype,
	  xlab="", ylab="",
	  main=paste("Legend - ", name, sep=""),
	  xlim=c(0,10),
	  ylim=c(0,10),
	  #las=1,
	  lwd=linewidth,bty="n",
	  cex.main=3.5, cex.lab=2.5, cex.axis=2.2, font=2,cex=2.2)
      par(font=2)
      legend(x="center", legend=paste(rev(scale), " %", sep=""), cex=3.6, lty=rev(linetype), col=rev(colors), pch=rev(plotchar), lwd=linewidth, bty='n')   # pch=11:10+length(values), col=c("blue","red","green","orange") 
      dev.off ( )   
    } else {
	print ("Error: Introduced wrong parameters. max <= min !")
    }
}


# Create a legend for name with range between min, max of n values.
make_legend_sim_exp <- function(path, name) {
      linetype <- c()
      linewidth <- 8
      plotchar <- c()
      plottype <- "l" # "b"
      # increase the margin on the right of the plot
      par(mar=c(5,6,4,2)+0.1)
      png ( paste(path, "/", name,"_sim_exp.png",sep=""), height=760, width=800, bg="transparent")
      par(font=2)
      plot(x=c(0), 
	  y=c(0),
	  type=plottype,
	  xlab="", ylab="",
	  main=paste("Legend - ", name, sep=""),
	  xlim=c(0,10),
	  ylim=c(0,10),
	  #las=1,
	  lwd=linewidth,bty="n",
	  cex.main=3.5, cex.lab=2.5, cex.axis=2.2, font=2,cex=2.2)
      par(font=1)
      legend(x="center", c("Simulation ","Experiments\n(mean\u{00B1}SEM, 4 repeats)"), pch=c('.','o'), cex=3.6, lty=c(1,6), lwd=linewidth, col=c("black","black"), bty="n")
      dev.off ( )   
}

