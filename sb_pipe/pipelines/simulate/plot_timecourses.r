# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Plotting of the confidence intervals
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-7 11:14:32 $


library(ggplot2)


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(file.path(SB_PIPE,'sb_pipe','utils','R','sb_pipe_ggplot2_themes.r'))




compute_descriptive_statistics <- function(timepoint.values, timepoint, variable, nfiles) {
    # compute mean, standard deviation, error, error.left, error.right
    timepoint$mean <- mean(timepoint.values, na.rm = TRUE)
    timepoint$sd <- sd(timepoint.values, na.rm = TRUE)
    timepoint$var <- var(timepoint.values, na.rm = TRUE)
    #y <- timepoint.values - timepoint.mean
    timepoint$skew <- mean(timepoint.values^3, na.rm = TRUE)/mean(timepoint.values^2, na.rm = TRUE)^1.5
    timepoint$kurt <- mean(timepoint.values^4, na.rm = TRUE)/mean(timepoint.values^2, na.rm = TRUE)^2 -3
    # 0.95 confidence level 
    #timepoint$ci95 <- qt(0.975, df=nfiles-1)*timepoint$sd/sqrt(nfiles)  # quantile t-distribution (few sample, stddev unknown exactly)
    timepoint$ci95 <- qnorm(0.975)*timepoint$sd/sqrt(nfiles) # quantile normal distribution (lot of samples)
    timepoint$coeffvar <- timepoint$sd / timepoint$mean
    timepoint$min <- min(timepoint.values, na.rm = TRUE)
    timepoint$stquantile <- quantile(timepoint.values, na.rm = TRUE)[2]  # Q1
    timepoint$median <- median(timepoint.values, na.rm = TRUE)  # Q2 or quantile(timepoint.values)[3]
    timepoint$rdquantile <- quantile(timepoint.values, na.rm = TRUE)[4]  # Q3
    timepoint$max <- max(timepoint.values, na.rm = TRUE)

    # put data in lists
    variable$mean <- c ( variable$mean, timepoint$mean )
    variable$sd <- c ( variable$sd, timepoint$sd )
    variable$var <- c ( variable$var, timepoint$var )
    variable$skew <- c ( variable$skew, timepoint$skew )
    variable$kurt <- c ( variable$kurt, timepoint$kurt )
    variable$ci95 <- c ( variable$ci95, timepoint$ci95 )
    variable$coeffvar <- c ( variable$coeffvar, timepoint$coeffvar )
    variable$min <- c ( variable$min, timepoint$min )
    variable$stquantile <- c ( variable$stquantile, timepoint$stquantile )
    variable$median <- c ( variable$median, timepoint$median )
    variable$rdquantile <- c ( variable$rdquantile, timepoint$rdquantile )
    variable$max <- c ( variable$max, timepoint$max )
 
    #print(nfiles)
    #for debug
    #print(column[j])
    #print(timepoints[k])
    #print(variable.mean)
    #prints(variable.sd)
    return (variable)
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

get_statistics_table <- function(statistics, variable, s=2) {    
    #print(variable$mean) 
    statistics[,s]   <- variable$mean
    statistics[,s+1] <- variable$sd
    statistics[,s+2] <- variable$var
    statistics[,s+3] <- variable$skew
    statistics[,s+4] <- variable$kurt
    statistics[,s+5] <- variable$ci95
    statistics[,s+6] <- variable$coeffvar
    statistics[,s+7] <- variable$min
    statistics[,s+8] <- variable$stquantile
    statistics[,s+9] <- variable$median
    statistics[,s+10] <- variable$rdquantile
    statistics[,s+11] <- variable$max
    return (statistics)
}


plot_error_bars <- function(outputdir, version, name, variable, timepoints, simulate__xaxis_label, bar_type="sd") {
    filename = ""

    if(bar_type == "none") {
      # standard error configuration
      filename = file.path(outputdir, paste(version, "_none_", name, ".png", sep=""))
      # Let's plot this special case now as it does not require error bars
      df <- data.frame(a=timepoints, b=variable$mean)      
      g <- ggplot() + geom_line(data=df, aes(x=a, y=b), color="black", size=1.0)
      g <- g + xlab(simulate__xaxis_label) + ylab(paste(name, " level [a.u.]", sep=""))
      ggsave(filename, dpi=300,  width=8, height=6) #, bg = "transparent")      

    } else { 

      df <- data.frame(a=timepoints, b=variable$mean, c=variable$sd, d=variable$ci95)
      #print(df)
      g <- ggplot(df, aes(x=a, y=b))

      # plot the error bars
      g <- g + geom_errorbar(aes(ymin=b-c, ymax=b+c), colour="blue",  size=1.0, width=0.1)    
        
      if(bar_type == "sd") {
	# standard deviation configuration
	filename = file.path(outputdir, paste(version, "_sd_", name, ".png", sep=""))
      } else {
	# standard deviation + confidence interval configuration
	filename = file.path(outputdir, paste(version, "_sd_n_ci95_", name, ".png", sep=""))
        # plot the C.I.	
	g <- g + geom_errorbar(aes(ymin=b-d, ymax=b+d), colour="lightblue", size=1.0, width=0.1)	
      }

      # plot the line
      g <- g + geom_line(aes(x=a, y=b), color="black", size=1.0)    

      # decorate
      g <- g + xlab(simulate__xaxis_label) + ylab(paste(name, " level [a.u.]", sep="")) + theme(legend.position = "none")
      ggsave(filename, dpi=300,  width=8, height=6)#, bg = "transparent")
   }
}



plot_error_bars_plus_statistics <- function(inputdir, outputdir, version, files, outputfile, simulate__xaxis_label) {
    
    theme_set(tc_theme(28))  

    # Read variable
    timecourses <- read.table( file.path(inputdir, files[1]), header=TRUE, na.strings="NA", dec=".", sep="\t" )
    column <- names (timecourses)

    column.names <- c ("Time")
    
    simulate__start <- timecourses$Time[1]
    simulate__end <- timecourses$Time[length(timecourses$Time)] 
    timepoints <- seq(from=simulate__start, to=simulate__end, by=(simulate__end-simulate__start)/(length(timecourses$Time)-1))
      
    time_length <- length(timepoints)
  

    # statistical table (to export)
    statistics <- matrix( nrow=time_length, ncol=(((length(column)-1)*13)+1) )
    statistics[,1] <- timepoints
    s <- 2
    linewidth=14
    
    # an empty colum that we need for creating a data.frame of length(timecourses$Time) rows
    na <- c(rep(NA, length(timecourses$Time)))

    for(j in 1:length(column)) {
      if(column[j] != "Time") {
	print(column[j])

	# Extract column[j] for each file.
	dataset <- data.frame(na)
	for(i in 1:length(files)) {
	    dataset <- data.frame(dataset, read.table(file.path(inputdir,files[i]),header=TRUE,na.strings="NA",dec=".",sep="\t")[,j])
	}
	# remove the first column (na)
	dataset <- subset(dataset, select=-c(na))
	
	#print(dataset)
	# structures
	timepoint <- list("mean"=0,"sd"=0,"var"=0,"skew"=0,"kurt"=0,"ci95"=0,
			  "coeffvar"=0,"min"=0,"stquantile"=0,"median"=0,"rdquantile"=0,"max"=0)
	variable <-list("mean"=c(),"sd"=c(),"var"=c(),"skew"=c(),"kurt"=c(),"ci95"=c(),
		      "coeffvar"=c(),"min"=c(),"stquantile"=c(),"median"=c(),"rdquantile"=c(),"max"=c())
	k <- 1
	# for each computed timepoint
 	for( l in 1:length ( timecourses$Time ) ) {

	  timepoint.values <- c ( )

  	  if ( k <= length( timepoints ) && as.character(timepoints[k]) == as.character(timecourses$Time[l]) ) {
	      #print(timepoints[k])
 	      # for each Sample
 	      for(m in 1:length(files)) {
		  timepoint.values <- c(timepoint.values, dataset[l,m])  
 	      }
  	      variable <- compute_descriptive_statistics(timepoint.values, timepoint, variable, length(files))   
 	      #print(variable)
  	      k <- k + 1
  	  }
 	}
  	column.names <- get_column_names_statistics(column.names, column[j])
  	statistics <- get_statistics_table(statistics, variable, s)
 	s <- s+13
  	plot_error_bars(outputdir, version, column[j], variable, timepoints, simulate__xaxis_label, "none")
  	plot_error_bars(outputdir, version, column[j], variable, timepoints, simulate__xaxis_label, "sd")  
  	plot_error_bars(outputdir, version, column[j], variable, timepoints, simulate__xaxis_label, "sd_n_ci95")  	
      }
    }
    #print (statistics)
    write.table(statistics, outputfile, sep="\t", col.names = column.names, row.names = FALSE) 
}


