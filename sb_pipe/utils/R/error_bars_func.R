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
# $Date: 2011-07-7 11:14:32 $



# plotCI
library(gplots)
# skewness, kurtosis
#library(GLDEX)
# create a multidimensional matrix from matrices
library(abind)

# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source( paste(SB_PIPE, "/sb_pipe/utils/R/plot_functions.R", sep="") )
source( paste(SB_PIPE, "/sb_pipe/utils/R/matrices.R", sep="") )





compute_descriptive_statistics <- function(timepoint.values, timepoint, species, nfiles) {
    # compute mean, standard deviation, error, error.left, error.right
    timepoint$mean <- mean(timepoint.values, na.rm = TRUE)
    timepoint$sd <- sd(timepoint.values, na.rm = TRUE)
    timepoint$var <- var(timepoint.values, na.rm = TRUE)
    #y <- timepoint.values - timepoint.mean
    timepoint$skew <- mean(timepoint.values^3, na.rm = TRUE)/mean(timepoint.values^2, na.rm = TRUE)^1.5
    timepoint$kurt <- mean(timepoint.values^4, na.rm = TRUE)/mean(timepoint.values^2, na.rm = TRUE)^2 -3
    # use of GLDEX
    #timepoint$skew <- skewness(timepoint.values, na.rm = TRUE, method = "fisher")
    #timepoint$kurt <- kurtosis(timepoint.values, na.rm = TRUE, method = "fisher")
    timepoint$sderr <- timepoint$sd/sqrt(nfiles) 
    # 0.95 confidence level 
    timepoint$ci95 <- qt(0.975, df=nfiles-1)*timepoint$sd/sqrt(nfiles)  # quantile t-distribution (few sample, stddev unknown exactly)
    #timepoint$ci95 <- qnorm(0.975)*timepoint$sd/sqrt(nfiles) # quantile normal distribution (lot of samples)
    timepoint$coeffvar <- timepoint$sd / timepoint$mean
    timepoint$min <- min(timepoint.values, na.rm = TRUE)
    timepoint$stquantile <- quantile(timepoint.values, na.rm = TRUE)[2]  # Q1
    timepoint$median <- median(timepoint.values, na.rm = TRUE)  # Q2 or quantile(timepoint.values)[3]
    timepoint$rdquantile <- quantile(timepoint.values, na.rm = TRUE)[4]  # Q3
    timepoint$max <- max(timepoint.values, na.rm = TRUE)

    # put data in lists
    species$mean <- c ( species$mean, timepoint$mean )
    species$sd <- c ( species$sd, timepoint$sd )
    species$var <- c ( species$var, timepoint$var )
    species$skew <- c ( species$skew, timepoint$skew )
    species$kurt <- c ( species$kurt, timepoint$kurt )
    species$ci95 <- c ( species$ci95, timepoint$ci95 )
    species$sderr <- c ( species$sderr, timepoint$sderr )
    species$coeffvar <- c ( species$coeffvar, timepoint$coeffvar )
    species$min <- c ( species$min, timepoint$min )
    species$stquantile <- c ( species$stquantile, timepoint$stquantile )
    species$median <- c ( species$median, timepoint$median )
    species$rdquantile <- c ( species$rdquantile, timepoint$rdquantile )
    species$max <- c ( species$max, timepoint$max )
 
    #print(nfiles)
    #for debug
    #print(column[j])
    #print(timepoints[k])
    #print(species.mean)
    #prints(species.sd)
    return (species)
}


get_column_names_statistics <- function(column.names, name) {    
    column.names <- c (column.names,
                       paste(name, "_Mean", sep=""),
                       paste(name, "_StdDev", sep=""),
                       paste(name, "_Variance", sep=""),
                       paste(name, "_Skewness", sep=""),
                       paste(name, "_Kurtosis", sep=""),                       
                       paste(name, "_t-dist_CI95%", sep=""),
                       paste(name, "_StdErr", sep=""),
                       paste(name, "_CoeffVar", sep=""),
                       paste(name, "_Minimum", sep=""),
                       paste(name, "_1stQuantile", sep=""),
                       paste(name, "_Median", sep=""),
                       paste(name, "_3rdQuantile", sep=""),
                       paste(name, "_Maximum", sep=""))
    #print(name)
    return (column.names)
}

get_statistics_table <- function(statistics, species, s=2) {    
    #print(species$mean) 
    statistics[,s]   <- species$mean
    statistics[,s+1] <- species$sd
    statistics[,s+2] <- species$var
    statistics[,s+3] <- species$skew
    statistics[,s+4] <- species$kurt
    statistics[,s+5] <- species$ci95
    statistics[,s+6] <- species$sderr
    statistics[,s+7] <- species$coeffvar
    statistics[,s+8] <- species$min
    statistics[,s+9] <- species$stquantile
    statistics[,s+10] <- species$median
    statistics[,s+11] <- species$rdquantile
    statistics[,s+12] <- species$max
    return (statistics)
}


plot_error_bars <- function(outputdir, files, version, name, species, time_length, timepoints, simulate__start, simulate__end, simulate__xaxis_label, linewidth, bar_type="sem") {
    filename = ""
    uiw_bars = c()
    ylimit = c()
    legend_title = ""
    if(bar_type == "none") {
      # standard error configuration
      filename = paste(outputdir, version, "_none_", name, ".png", sep="" )
      ylimit = c(0,max(species$mean)+max((species$mean)/4))
      legend_title = paste("Mean \u{00B1} SEM (", length(files), " Samples)", sep="" )
    } else if(bar_type == "sem") {
      # standard error configuration
      filename = paste(outputdir, version, "_sem_", name, ".png", sep="" )
      uiw_bars = species$sderr
      ylimit = c(0,max(species$mean + species$sderr)+max((species$mean + species$sderr)/4))
      legend_title = paste("Mean \u{00B1} SEM (", length(files), " Samples)", sep="" )
    } else if(bar_type == "sd") {
      # standard deviation configuration
      filename = paste(outputdir, version, "_sd_", name, ".png", sep="" )
      uiw_bars = species$sd
      ylimit = c(0,max(species$mean + species$sd)+max((species$mean + species$sd)/3))
      legend_title = paste("Mean \u{00B1} SD (", length(files), " Samples)", sep="" )
    } else if(bar_type == "sd_n_ci95") {
      # standard deviation configuration
      filename = paste(outputdir, version, "_sd_n_ci95_", name, ".png", sep="" )
      uiw_bars = species$sd
      ylimit = c(0,max(species$mean + species$sd)+max((species$mean + species$sd)/3))
      legend_title = paste("Mean \u{00B1} SD (", length(files), " Samples)", sep="" )
    } else if(bar_type == "ci95") { 
      # confidence intervals 95% configuration
      filename = paste(outputdir, version, "_ci95_", name, ".png", sep="" )
      uiw_bars = species$ci95
      ylimit = c(0,max(species$mean + species$ci95)+max((species$mean + species$ci95)/4))
      legend_title = paste("Mean \u{00B1} t-distrib CI 95% (", length(files), " Samples)", sep="")
    }
    
    
    png (filename, height=1000, width=1400, bg="transparent")
    # increase the margin on the right of the plot
    par(mar=c(20,20,12,0))
    plotCI(x=species$mean,
           uiw=uiw_bars,
           col="black", barcol=colours()[288],
           type="l", #line
	    pch=NA, # no circle for the mean point
           xlim=c(1,time_length), 
           ylim=ylimit,
           labels=FALSE,
	   #xlab="Time (min)", ylab="Relative Phosphorylation Activity", 
	   xlab="", ylab="", 
	   main="",
	   las=1,
	   lwd.ticks=12,
	   cex.main=5.6, cex.lab=5.6, cex.axis=5.6, font.axis=2,bty="n",
	   cex=5.6,lwd=linewidth,
           xaxt='n', gap=0.0)

    if(bar_type == "sd_n_ci95") { # add ci95
    	plotCI(x=species$mean,
           uiw=species$ci95,
           col="black", barcol=colours()[278],
           type="l", #line
	    pch=NA, # no circle for the mean point
           xlim=c(1,time_length),
           ylim=ylimit,
           labels=FALSE,
	   #xlab="Time (min)", ylab="Relative Phosphorylation Activity", 
	   xlab="", ylab="", 
	   main="",
	   las=1,
	   lwd.ticks=12,
	   cex.main=5.6, cex.lab=5.6, cex.axis=5.6, font.axis=2,bty="n",
	   cex=5.6,lwd=linewidth,
           xaxt='n', gap=0.0, add=TRUE)
    }
 
    # SPAN: 0.25 (line is the mean), 0.90 (line approximates the mean)
    #species.mean.loess <- loess(species$mean ~ timepoints, span=0.90, data.frame(x=timepoints, y=species$mean))
    #species.mean.predict <- predict(species.mean.loess, data.frame(x=timepoints))
    #lines(spline(species.mean.predict, method="natural", n = 10*length(species$mean)), lwd=linewidth)
    #lines(spline(species$mean, method="natural", n = 10*length(species$mean)),lwd=linewidth)
    #lines(spline(species$mean+species$sderr, method="natural", n = 10*length(species$mean)))
    #lines(spline(species$mean-species$sderr, method="natural", n = 10*length(species$mean)))

    lines(species$mean,lwd=linewidth)

    
    ## set x axis
    # Set up x axis with tick marks alone
    tp <- seq(from=simulate__start, to=timepoints[length(timepoints)], by=(simulate__end-simulate__start)/10)
    
    ## Plot the axes
    # if timepoints has "by=0.1", then set 50*0...otherwise set 10*0.....
    axis(side=1, labels=FALSE, at=(length(timepoints)/10)*0:length(timepoints), cex.axis=5.6, font.axis=2,lwd.ticks=12)
    # Plot x axis labels at default tick marks
    #text(side=1, 10*0:length(timepoints), par("usr")[3]-0.0, srt=45, adj=c(1.2,1.2), labels=timepoints, cex=4.0, font=2, xpd=TRUE)
    #text(side=1, 10*0:length(tp), par("usr")[3]-0.0, srt=45, adj=c(1.2,1.2), labels=tp, cex=4.0, font=2, xpd=TRUE)
    text(side=1, (length(timepoints)/10)*0:length(tp), par("usr")[3]-0.0, srt=0, adj=c(0.5,1.4), labels=tp, cex=5.6, font=2, xpd=TRUE)
    # Plot x axis label at line 6 (of 7)
    mtext(side=1, text=simulate__xaxis_label, line=8, cex=5.6, font=2, adj=0.5, padj=0.5) 
    mtext(side=2, text=paste(name, " level [a.u.]", sep=""), line=12, cex=5.6, font=2)
    #legend("topright", legend_title,cex=4.5, lty=1,lwd=linewidth, bty="n")   # col=c("blue","red","green")
    box(bty="l", lwd=14, lty=1)
    dev.off()  
}



plot_error_bars_plus_statistics <- function(inputdir, outputdir, version, files, outputfile, simulate__start, simulate__end, simulate__interval_size, simulate__xaxis_label, exp=TRUE) {

    timepoints <- seq(from=simulate__start, to=simulate__end, by=simulate__interval_size)
    
    # Read species
    timecourses <- read.table ( paste ( inputdir, '/', files[1], sep="" ), header=TRUE, na.strings="NA", dec=".", sep="\t" )
    column <- names (timecourses)
    time_length <- length(timepoints)
    column.names <- c ("Time")
    if(exp == TRUE && timecourses$Time[length(timecourses$Time)] != timepoints[time_length]) {
	print(paste("ERROR: Simulated length (", timecourses$Time[length(timecourses$Time)], 
		    ") is NOT equal to experiment length (", timepoints[time_length], ")", sep=""))
	quit()
    }
    # statistical table (to export)
    statistics <- matrix( nrow=time_length, ncol=(((length(column)-1)*13)+1) )
    statistics[,1] <- timepoints
    s <- 2
    linewidth=14

    #dataset <- load_files_in_matrix(inputdir, files)
    #print(dataset)

    for(j in 1:length(column)) {
      if(column[j] != "Time") {
	print(column[j])

	# Don't retrieve the variable Time.
	cols <- c(rep("NULL",j-1), NA, rep("NULL",length(column)-j))
	# Extract column[j] for each file.
	dataset <- load_files_columns_in_matrix(inputdir, files, cols)
	#print(dataset)
	# structures
	timepoint <- list("mean"=0,"sd"=0,"var"=0,"skew"=0,"kurt"=0,"ci95"=0,"sderr"=0,
			  "coeffvar"=0,"min"=0,"stquantile"=0,"median"=0,"rdquantile"=0,"max"=0)
	species <-list("mean"=c(),"sd"=c(),"var"=c(),"skew"=c(),"kurt"=c(),"ci95"=c(),"sderr"=c(),
		      "coeffvar"=c(),"min"=c(),"stquantile"=c(),"median"=c(),"rdquantile"=c(),"max"=c())
	k <- 1
	# for each computed timepoint
 	for( l in 1:length ( timecourses$Time ) ) {

	  # it contains values for a specific timepoint (same size of the array timepoints)
	  timepoint.values <- c ( )
	  # consider only a subset of timepoints (vector: timepoints)

#	  print(timepoints[k])
	  #print(timecourses$Time[l])
	  #print(timepoint.values)

  	  if ( k <= length( timepoints ) && as.character(timepoints[k]) == as.character(timecourses$Time[l]) ) {
	      #print(timepoints[k])
	      #if(timecourses$Time[l] == 0.3) print ("0.3")
 	      # for each Sample
 	      for ( m in 1:length ( files) ) {
  		#timepoint.values <- c(timepoint.values, dataset[l,j,m]) 
  		timepoint.values <- c(timepoint.values, dataset[l,1,m]) 
 	      }
  	      species <- compute_descriptive_statistics(timepoint.values, timepoint, species, length(files))   
 	      #print(species)
  	      k <- k + 1
  	  }
 	}
  	column.names <- get_column_names_statistics(column.names, column[j])
  	statistics <- get_statistics_table(statistics, species, s)
 	s <- s+13
  	plot_error_bars(outputdir, files, version, column[j], species, time_length, timepoints, simulate__start, simulate__end, simulate__xaxis_label, linewidth, "none")   	
  	plot_error_bars(outputdir, files, version, column[j], species, time_length, timepoints, simulate__start, simulate__end, simulate__xaxis_label, linewidth, "sem")   
  	plot_error_bars(outputdir, files, version, column[j], species, time_length, timepoints, simulate__start, simulate__end, simulate__xaxis_label, linewidth, "sd") 
 	plot_error_bars(outputdir, files, version, column[j], species, time_length, timepoints, simulate__start, simulate__end, simulate__xaxis_label, linewidth, "ci95") 
 	plot_error_bars(outputdir, files, version, column[j], species, time_length, timepoints, simulate__start, simulate__end, simulate__xaxis_label, linewidth, "sd_n_ci95") 
	
      }
    }
    #print (statistics)
    write.table(statistics, outputfile, sep="\t", col.names = column.names, row.names = FALSE) 
}


