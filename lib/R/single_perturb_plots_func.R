# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Plotting of time courses columns wrt time. 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-11-16 12:14:32 $
# $Id: param_scan__sim_parameter_scan.R,v 3.0 2010-11-16 19:45:32 Piero Dalle Pezze Exp $



# to use string replace
library(stringr)     


# Retrieve the environment variable SB_PIPE_LIB
SB_PIPE_LIB <- Sys.getenv(c("SB_PIPE_LIB"))
# Add a collection of R functions
source(paste(SB_PIPE_LIB, "/R/matrices.R", sep=""))




plot_single_perturbation_data <- function(model_noext, species, inhibition_only, results_dir, dataset_parameter_scan_dir, tc_parameter_scan_dir, simulate__start, simulate__end, simulate__interval_size, simulate__xaxis_label, param_scan__single_perturb_simulations_number, perturbation_in_percent_levels) {
    
    
    writeLines(paste("Model: ", model_noext, ".cps", sep=""))
    writeLines(paste("Perturbed species: ", species, sep=""))
    #writeLines(results_dir)
    # variables
    inputdir <- c ( paste(results_dir, "/", dataset_parameter_scan_dir, "/", sep="" ) )
    outputdir <- c ( paste(results_dir, "/", tc_parameter_scan_dir, "/", sep="" ) )
    #writeLines(inputdir)
    #writeLines(outputdir)
    

    
    for(k_sim in 1:param_scan__single_perturb_simulations_number) {    
    
	  
	  files <- list.files( path=inputdir, pattern=paste(model_noext, '__sim_', k_sim, sep=""))
	  levels <- c()
	  levels.index <- c()

	  # create the directory of output
	  if (!file.exists(outputdir)){ dir.create(outputdir) }
	  
	  
	  # the array files MUST be sorted. Required to convert the string into numeric.
	  # this is important because the legend must present species's knockdown in order.
	  # It is also important that the order is decreasing because of the size of the plot,
	  # otherwise some curve could be outside the box of the graph.
	  for(i in 1:length(files)) {
	      num_of_underscores <- length(gregexpr("_", files[i])[[1]])
	      levels <- c(levels, as.numeric(str_replace( strsplit( files[i], "_")[[1]][num_of_underscores + 1], ".csv", "")))
	  }
	  levels.temp <- c(levels)
	  newmax <- max(levels)+1
	  for(i in 1:length(levels)) {
	    min <- which.min(levels.temp)
	    #writeLines(min(levels.temp))
	    levels.index <- c(levels.index, min)
	    levels.temp[min] <- newmax
	  }
	  #writeLines(levels)
	  # sort by decreasing order
	  #writeLines(files)
	  #writeLines(levels)
	  #writeLines(levels.index)
	  levels <- sort(levels)

						  # Read species
	  timecourses <- read.table ( paste ( inputdir, files[1], sep="" ), header=TRUE, na.strings="NA", dec=".", sep="\t" )
	  column <- names ( timecourses )

	  #writeLines(levels)
	  #writeLines(levels.index)

	  # Load files in memory
	  dataset <- load_files_in_matrix_wlevels(inputdir, files, levels.index)

	  levels <- paste(species, levels, sep=" ")
	  writeLines(levels)

          

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
	    } else {
	      # THIS PALETTE OF COLOURS can be used for gradual overexpression (magenta [100,250])	  
	      # First number is control (black), last number 96 is overexpression (magenta) (100%,115%,130%,..250%)
	      # In linetype: 1 is a full line
	      colors <- colors()[c(24,99,115,95,98,97,96,464,463,510)]
	      linetype <- c(1,2,3,4,1,2,3,4,6,1)
	    }
	  }
	  
	  
	  # points to retrieve
	  # configuration of the x axis
	  time_axis <- seq(from=simulate__start, to=simulate__end, by=(simulate__end-simulate__start)/10)
          xoffset <- c(0,max(time_axis))
	  
	  linewidth <- 12
	  plotchar <- seq(1,length(files),1)
	  plottype <- "l" # "b"

	  if(plottype == "l") {
	      plotchar <- c()
	  }

	  for ( j in 2:length ( column ) ) {
	    # continuous time 

	    name <- column[j]

	    png ( paste ( outputdir, model_noext, "__eval_", name, "__sim_", k_sim, ".png", sep="" ), height=1000, width=1400, bg="transparent")
	    
	    # increase the margin on the right of the plot
	    par(mar=c(20,20,12,0))

	    # Plot the maximum curve as first
	    if(max(dataset[,j,1]) >= max(dataset[,j,length(files)])) {
		plot(x=c(dataset[,1,1]), y=c(dataset[,j,1]),
		      type=plottype,
		      xlab="", ylab="", 
		      ylim=c(0,max(dataset[,j,1])+max(dataset[,j,1])/4 ),
		      xlim=xoffset, 
		      main="",
		      las=1,
		      lwd.ticks=12,
		      bty="n", xaxt='n', 
		      lwd=linewidth,
		      lty=linetype[1], 
		      col=colors[1], pch=plotchar[1],
		      cex.main=5.6, cex.lab=5.6, cex.axis=5.6,cex=5.6, font.axis=2 )
	    } else {
		plot(x=c(dataset[,1,1]), y=c(dataset[,j,length(files)]),
		      type=plottype,
		      xlab="", ylab="", 
		      ylim=c(0,max(dataset[,j,length(files)])+max(dataset[,j,length(files)])/4 ),
		      xlim=xoffset, 
		      main="",
		      las=1,
		      lwd.ticks=12,
		      lwd=linewidth,
		      bty="n",xaxt='n', 
		      lty=linetype[length(files)], 
		      col=colors[length(files)], pch=plotchar[length(files)],
		      cex.main=5.6, cex.lab=5.6, cex.axis=5.6,cex=5.6, font.axis=2)
	    }

	    for ( m in (length(files)):1 ) {
		lines( x=dataset[,1,1], y=dataset[,j,m], type=plottype, lty=linetype[m], col=colors[m], pch=plotchar[m], lwd=linewidth ) 
	    }    

	    ## set x axis
	    # Set up x axis with tick marks alone
	    tp <- seq(from=simulate__start, to=simulate__end, by=(simulate__end-simulate__start)/10)
	    time_axis <- seq(from=simulate__start, to=simulate__end-1, by=(simulate__end-simulate__start)/10)
	    
	    
	    ## Plot the axes
	    # Set up axis with tick marks alone
	    axis(side=1, labels=FALSE, at=(length(time_axis)/10)*0:length(time_axis), cex.axis=5.6, font.axis=2, lwd.ticks=12)    	    
	    # Plot x axis labels at default tick marks
	    text(side=1, (length(time_axis)/10)*0:length(time_axis), par("usr")[3]-0.0, srt=0, adj=c(0.5,1.5), labels=tp, cex=5.6, font=2, xpd=TRUE)  	    
	    # Plot x axis label at line 6 (of 7)
	    mtext(side=1, text=simulate__xaxis_label, line=12, cex=5.6, font=2) 
	    mtext(side=2, text=paste(name, " level [a.u.]", sep=""), line=12, cex=5.6, font=2) 

	    # legend removed and added manually 
	    #legend(x="topright", legend=rev(levels), cex=3.6, lty=rev(linetype), col=rev(colors), pch=rev(plotchar), lwd=linewidth)   # pch=11:10+length(files), col=c("blue","red","green","orange")
	    box(bty="l", lwd=14, lty=1)      
	    dev.off ( )       # empty the device

	  }
  
  }
  
}
