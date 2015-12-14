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
# Object: Plotting of time courses columns wrt time. 
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
# $Date: 2010-11-16 12:14:32 $
# $Id: plot_sim_parameter_scan.R,v 3.0 2010-11-16 19:45:32 Piero Dalle Pezze Exp $


# to use string replace
library(stringr)     


# Retrieve the environment variable SB_PIPE_LIB
SB_PIPE_LIB <- Sys.getenv(c("SB_PIPE_LIB"))
# Add a collection of R functions
source(paste(SB_PIPE_LIB, "/R/matrices.R", sep=""))




main <- function(args) {
    model_noext <- args[1]
    species <- args[2]
    inhibition_only <- args[3]
    results_dir <- args[4]
    dataset_parameter_scan_dir <- args[5]
    tc_parameter_scan_dir <- args[6]
    # Team: kathrin or glyn
    team <- args[7] 
    param_scan__single_perturb_simulations_number <- args[8]
    perturbation_in_percent_levels <- args[9]
    

    
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

	  timepoints <- c()
	  time_axis <- c()

	  time_length <- length(timepoints)

	  #writeLines(levels)
	  #writeLines(levels.index)

	  # Load files in memory
	  dataset <- load_files_in_matrix_wlevels(inputdir, files, levels.index)

	  levels <- paste(species, levels, sep=" ")
	  writeLines(levels)

	  # legend removed and added manually 
	  #xoffset <- c(0,max(dataset[,1,1]) + max(dataset[,1,1])/3)
	  xoffset <- c(0,max(dataset[,1,1]))

	  # points to retrieve
	  # configuration of the x axis
	  if(team == 'kathrin') { 
	      timepoints <- c (0, 1, 3, 5, 10, 15, 20, 30, 45, 60, 120)    # to add 1440
	      time_axis <- c(0, 20, 40, 60, 80, 100, 120)
	      xoffset <- c(0,max(dataset[,1,1]) + 3)
	  } else if(team == 'glyn') {
	      timepoints <- c (0, 1, 2, 3, 5, 7, 9, 10, 11, 14, 17, 19, 21)
	      time_axis <- c(0, 3, 6, 9, 12, 15, 18, 21)
	      xoffset <- c(0,max(dataset[,1,1]) + 1)	      
	  } else if(team == 'pdp') {
	      timepoints <- c (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
	      time_axis <- c(0, 20, 40, 60, 80, 100)
	      xoffset <- c(0,max(dataset[,1,1]) + 1)
	  }


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
	  
	  
	  
	  
	  linewidth <- 8
	  plotchar <- seq(1,length(files),1)
	  plottype <- "l" # "b"

	  if(plottype == "l") {
	      plotchar <- c()
	  }

	  for ( j in 2:length ( column ) ) {
	    # continuous time 

	    name <- column[j]

	    png ( paste ( outputdir, model_noext, "__eval_", name, "__sim_", k_sim, ".png", sep="" ), height=600, width=800, bg="transparent")
	    #print (paste ( outputdir, model_noext, "__eval_", name, "__sim_", k_sim, ".png", sep=" ))
	    
	    
	    # increase the margin on the right of the plot
	    par(mar=c(7,9.5,4,0)+0.1)

	    # Plot the maximum curve as first
	    if(max(dataset[,j,1]) >= max(dataset[,j,length(files)])) {
		plot(x=c(dataset[,1,1]), y=c(dataset[,j,1]),
		      type=plottype,
		      #xlab="Time (days)", ylab="Relative Phosphorylation Activity", 
		      xlab="", ylab="", 
		      ylim=c(0,max(dataset[,j,1])+max(dataset[,j,1])/4 ),
		      xlim=xoffset, 
		      main="",
		      las=1,
		      bty="n", xaxt='n', 
		      lwd=linewidth, #lwd.ticks=6,
		      lty=linetype[1], 
		      col=colors[1], pch=plotchar[1],
		      cex.main=3.5, cex.lab=3.4, cex.axis=3.4,cex=2.2, font.axis=2 )
	    } else {
		plot(x=c(dataset[,1,1]), y=c(dataset[,j,length(files)]),
		      type=plottype,
		      #xlab="Time (days)", ylab="Relative Phosphorylation Activity", 
		      xlab="", ylab="", 
		      ylim=c(0,max(dataset[,j,length(files)])+max(dataset[,j,length(files)])/4 ),
		      xlim=xoffset, 
		      main="",
		      las=1,
		      lwd=linewidth, #lwd.ticks=6,
		      bty="n",xaxt='n', 
		      lty=linetype[length(files)], 
		      col=colors[length(files)], pch=plotchar[length(files)],
		      cex.main=3.5, cex.lab=3.4, cex.axis=3.4,cex=2.2, font.axis=2)
	    }

	    ## set x axis
	    # Set up x axis with tick marks alone
	    axis(side=1, labels=FALSE, at=time_axis, cex.axis=3.4, font.axis=2,lwd.ticks=6)
	    axis(side=2, labels=FALSE, cex.axis=3.4, font.axis=2,lwd.ticks=6)
	    # Plot x axis labels at default tick marks
	    text(#side=1, 
      #           time_axis, par("usr")[3]-0.0, srt=30, adj=c(1.1,1.2), labels=time_axis, cex=3.4, font=2, xpd=TRUE)
		time_axis, par("usr")[3]-0.0, srt=0, adj=c(0.5,1.5), labels=time_axis, cex=3.4, font=2, xpd=TRUE)
	    # Plot x axis label at line 6 (of 7)
	    if(team == 'kathrin') {
	      mtext(side=1, text="Time [min]", line=5.5, cex=3.4, font=2) 
	    } else if(team == 'glyn') {
	      mtext(side=1, text="Time [days]", line=5.5, cex=3.4, font=2) 
	    } else if(team == 'pdp') {
	      mtext(side=1, text="Time [a.u.]", line=5.5, cex=3.4, font=2) 
	    }
	    mtext(side=2, text=paste(name, " level [a.u.]", sep=""), line=7, cex=3.4, font=2) 
	    for ( m in (length(files)):1 ) {
		lines( x=dataset[,1,1], y=dataset[,j,m], type=plottype, lty=linetype[m], col=colors[m], pch=plotchar[m], lwd=linewidth ) # col="red" pch=10+m, 
	    }
	    # legend removed and added manually 
	    #legend(x="topright", legend=rev(levels), cex=3.6, lty=rev(linetype), col=rev(colors), pch=rev(plotchar), lwd=linewidth)   # pch=11:10+length(files), col=c("blue","red","green","orange")
	    box(bty="l", lwd=8, lty=1)      
	    dev.off ( )       # empty the device

	  }
  }
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())

