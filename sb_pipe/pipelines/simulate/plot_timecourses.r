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
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-7 11:14:32 $


library(ggplot2)


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(file.path(SB_PIPE,'sb_pipe','utils','R','sb_pipe_ggplot2_themes.r'))



# For each time point compute the most relevant descriptive statistics: mean, sd, var, skew, kurt, ci95, coeffvar, 
# min, 1st quantile, median, 3rd quantile, and max.
#
# :param timepoint.values: array of values for a certain time point
# :param nfiles: the number of files (samples) 
# :return: the statistics for the array of values for a specific time point
compute_descriptive_statistics <- function(timepoint.values, nfiles) {
	timepoint <- list("mean"=0,"sd"=0,"var"=0,"skew"=0,"kurt"=0,"ci95"=0,
			  "coeffvar"=0,"min"=0,"stquantile"=0,"median"=0,"rdquantile"=0,"max"=0)
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

    return (timepoint)
}



# Return the column names of the statitics to calculate
#
# :param column.names: an array of column names
# :param readout: the name of the readout
# :return: the column names including the readout name
get_column_names_statistics <- function(column.names, readout) {    
    column.names <- c (column.names,
                       paste(readout, "_Mean", sep=""),
                       paste(readout, "_StdDev", sep=""),
                       paste(readout, "_Variance", sep=""),
                       paste(readout, "_Skewness", sep=""),
                       paste(readout, "_Kurtosis", sep=""),                       
                       paste(readout, "_t-dist_CI95%", sep=""),
                       paste(readout, "_StdErr", sep=""),
                       paste(readout, "_CoeffVar", sep=""),
                       paste(readout, "_Minimum", sep=""),
                       paste(readout, "_1stQuantile", sep=""),
                       paste(readout, "_Median", sep=""),
                       paste(readout, "_3rdQuantile", sep=""),
                       paste(readout, "_Maximum", sep=""))
    #print(readout)
    return (column.names)
}



# Add the statistics for a readout to the table of statistics. The first column is Time.
#
# :param statistics: the table of statistics to fill up
# :param readout: the statistics for this readout.
# :param colidx: the position in the table to put the readout statistics
# :return: The table of statistics including this readout.
get_statistics_table <- function(statistics, readout, colidx=2) {    
    #print(readout$mean) 
    statistics[,colidx]   <- readout$mean
    statistics[,colidx+1] <- readout$sd
    statistics[,colidx+2] <- readout$var
    statistics[,colidx+3] <- readout$skew
    statistics[,colidx+4] <- readout$kurt
    statistics[,colidx+5] <- readout$ci95
    statistics[,colidx+6] <- readout$coeffvar
    statistics[,colidx+7] <- readout$min
    statistics[,colidx+8] <- readout$stquantile
    statistics[,colidx+9] <- readout$median
    statistics[,colidx+10] <- readout$rdquantile
    statistics[,colidx+11] <- readout$max
    return (statistics)
}



# Plot a model readout time course. If specified error bars are also plotted for each time point.
#
# :param outputdir: The output directory
# :param model: the model name
# :param readout: the name of the readout
# :param data: the data to plot (time point means at least)
# :param timepoints: the Time vector
# :param df_exp_dataset: an experimental data set data frame.
# :param plot_exp_dataset: TRUE if the experimental data set should be added
# :param xaxis_label: the xaxis label 
# :param yaxis_label: the yaxis label 
# :param bar_type: the type of bar ("none", "sd", "sd_n_ci95")
plot_error_bars <- function(outputdir, model, readout, data, timepoints, df_exp_dataset, plot_exp_dataset=FALSE, xaxis_label="", yaxis_label="", bar_type="sd") {
    filename = ""
    
    g <- ggplot()
    if(bar_type == "none") {
      # standard error configuration
      filename = file.path(outputdir, paste(model, "_none_", readout, ".png", sep=""))
      # Let's plot this special case now as it does not require error bars
      df <- data.frame(a=timepoints, b=data$mean)      
      g <- g + geom_line(data=df, aes(x=a, y=b), color="black", size=1.0) + 
           xlab(xaxis_label) + ylab(yaxis_label) + ggtitle(readout)
    } else { 

      df <- data.frame(a=timepoints, b=data$mean, c=data$sd, d=data$ci95)
      #print(df)

      # plot the error bars
      g <- g + geom_errorbar(data=df, aes(x=a, ymin=b-c, ymax=b+c), colour="blue", size=1.0, width=0.1)    
        
      if(bar_type == "sd") {
        # standard deviation configuration
        filename = file.path(outputdir, paste(model, "_sd_", readout, ".png", sep=""))
      } else {
        # standard deviation + confidence interval configuration
        filename = file.path(outputdir, paste(model, "_sd_n_ci95_", readout, ".png", sep=""))
        # plot the C.I.
        g <- g + geom_errorbar(data=df, aes(x=a, ymin=b-d, ymax=b+d), colour="lightblue", size=1.0, width=0.1)	
      }   

      # plot the line
      g <- g + geom_line(data=df, aes(x=a, y=b), color="black", size=1.0) 
      
      # decorate
      g <- g + xlab(xaxis_label) + ylab(yaxis_label) + ggtitle(readout) + theme(legend.position = "none")
   }
   ggsave(filename, dpi=300,  width=8, height=8)#, bg = "transparent")
   
   if(plot_exp_dataset) {
     # Let's add the experimental data set to the plot
     # ONLY PRINT THE DATA POINTS FOR THE LENGTH OF THIS SIMULATION
     df_max_time <- max(df$a)
     df_exp_dataset <- df_exp_dataset[df_exp_dataset$Time <= df_max_time,]
     if(readout %in% colnames(df_exp_dataset)) {
         g <- g + geom_point(data=df_exp_dataset, aes_string(x="Time", y=readout), shape=1, size=4, stroke=1.5)
         ggsave(gsub(".png","_w_dataset.png",filename), dpi=300,  width=8, height=8)#, bg = "transparent")   
     }
   }
}



# Plot model readouts with statistics for each time point.
#
# :param inputdir: the input directory containing the time course files
# :param outputdir: the output directory
# :param model: the model name
# :param outputfile: the name of the file to store the statistics
# :param exp_dataset: a full path file containing the experimental data.
# :param plot_exp_dataset: TRUE if the experimental data should also be plotted
# :param xaxis_label: the xaxis label 
# :param yaxis_label: the yaxis label 
plot_error_bars_plus_statistics <- function(inputdir, outputdir, model, outputfile, exp_dataset, plot_exp_dataset=FALSE, xaxis_label="", yaxis_label="") {
    
    theme_set(tc_theme(36)) #28
    
    # create the directory of output
    if (!file.exists(outputdir)){ 
        dir.create(outputdir) 
    }
    
    df_exp_dataset <- data.frame()
    # check that exp_dataset exists and that the file ends with .csv (it is not a dir!)
    if (file.exists(exp_dataset) && grepl('.csv$', exp_dataset)){     
        df_exp_dataset <- data.frame(read.table(exp_dataset, header=TRUE, na.strings="NA", dec=".", sep="\t"))    
    } else {
        print(paste("Error: file ", exp_dataset, " does not exist. Skip plots.", sep=""))
        plot_exp_dataset = FALSE
    }
    
    # collect all files in the directory
    files <- list.files( path=inputdir, pattern=model )
    print(files)
        
    # Read the simulated time course data sets
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
    colidx <- 2
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
        data <-list("mean"=c(),"sd"=c(),"var"=c(),"skew"=c(),"kurt"=c(),"ci95"=c(),
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
                timepoint <- compute_descriptive_statistics(timepoint.values, length(files))
                # put data in lists
                data$mean <- c ( data$mean, timepoint$mean )
                data$sd <- c ( data$sd, timepoint$sd )
                data$var <- c ( data$var, timepoint$var )
                data$skew <- c ( data$skew, timepoint$skew )
                data$kurt <- c ( data$kurt, timepoint$kurt )
                data$ci95 <- c ( data$ci95, timepoint$ci95 )
                data$coeffvar <- c ( data$coeffvar, timepoint$coeffvar )
                data$min <- c ( data$min, timepoint$min )
                data$stquantile <- c ( data$stquantile, timepoint$stquantile )
                data$median <- c ( data$median, timepoint$median )
                data$rdquantile <- c ( data$rdquantile, timepoint$rdquantile )
                data$max <- c ( data$max, timepoint$max )
                
                #print(data)
                k <- k + 1
            }
        }
        column.names <- get_column_names_statistics(column.names, column[j])
        statistics <- get_statistics_table(statistics, data, colidx)
        colidx <- colidx+13
        plot_error_bars(outputdir, model, column[j], data, timepoints, df_exp_dataset, plot_exp_dataset, xaxis_label, yaxis_label, "none")
        plot_error_bars(outputdir, model, column[j], data, timepoints, df_exp_dataset, plot_exp_dataset, xaxis_label, yaxis_label, "sd")  
        plot_error_bars(outputdir, model, column[j], data, timepoints, df_exp_dataset, plot_exp_dataset, xaxis_label, yaxis_label, "sd_n_ci95")  	
      }
    }
    #print (statistics)
    write.table(statistics, outputfile, sep="\t", col.names = column.names, row.names = FALSE) 
}


