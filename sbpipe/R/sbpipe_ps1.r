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
# $Date: 2016-07-6 12:14:32 $


 
library(ggplot2)
library(reshape2)

# Retrieve the environment variable SBPIPE
SBPIPE <- Sys.getenv(c("SBPIPE"))
source(file.path(SBPIPE, 'sbpipe','R','sbpipe_ggplot2_themes.r'))





# Return the indexes of the files as sorted by levels.
#
# :param files: the scanned files.
get_sorted_level_indexes <- function(files) {
  levels <- c()
  levels.index <- c()

  # the array files MUST be sorted. Required to convert the string into numeric.
  # this is important because the legend must represent variable's knockdown in order.
  for(i in 1:length(files)) {
      num_of_underscores <- length(gregexpr("_", files[i])[[1]])
      levels <- c(levels, as.numeric(gsub(".csv", "", strsplit( files[i], "_")[[1]][num_of_underscores + 1]) ))
  }
  levels.temp <- c(levels)
  newmax <- max(levels)+1
  for(i in 1:length(levels)) {
      min <- which.min(levels.temp)
      #print(min(levels.temp))
      levels.index <- c(levels.index, min)
      levels.temp[min] <- newmax
  }
  return(levels.index)
}





# Plot model single parameter scan time courses
#
# :param model: The model name
# :param variable: The model variable to scan
# :param inhibition_only: true if the scanning only decreases the variable amount (inhibition only)
# :param outputdir: the output directory
# :param sim_data_folder: the name of the folder containing the simulated data
# :param sim_plots_folder: the name of the folder containing the simulated plots
# :param xaxis_label: the label for the x axis (e.g. Time (min))
# :param runs: the number of repeated simulations
# :param percent_levels: true if scanning levels are in percent (default: TRUE)
# :param min_level: the minimum level (default: 0)
# :param max_level: the maximum level (default: 100)
# :param levels_number: the number of levels (default: 10)
# :param xaxis_label: the label for the x axis (e.g. Time [min])
# :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
plot_single_param_scan_data <- function(model, variable, inhibition_only, 
					outputdir, sim_data_folder, sim_plots_folder, runs,
					percent_levels=TRUE, min_level=0, 
					max_level=100, levels_number=10, 
					xaxis_label="", yaxis_label="") {
    
    # Set the labels for the plot legend
    labels <- seq(as.numeric(min_level), as.numeric(max_level), (as.numeric(max_level)-as.numeric(min_level))/(as.numeric(levels_number)))    
    labels <- round(labels, digits = 0)
    
    # Set the color and linetype for the plot
    colors <- c()
    linetype <- c()
    
    # Add percentages to the labels
    if(percent_levels) {
      labels <- paste(labels, " %", sep="")
    }
    # Scanning using a virtual variable (A_percent_level) defining the percent level of its corresponding real variable (A). 
    # The scanninig is therefore done by percent levels and at the beginning.
    # NOTE: A_percent_level=0  ==> A is knocked out (so 0%)
    if(inhibition_only) {
      # Including knockout (first number is knock out (bright blue), last number 24 is control (black))  (0%,10%,20%,..,100%)
      colors <- c("dodgerblue", "dodgerblue1", "dodgerblue2", "dodgerblue3", "dodgerblue4", "blue", "blue1", "blue2", "blue3", "blue4", "black")
      linetype <- c(1,6,4,3,2,1,6,4,3,2,1)
    } else {
      # Including knockout (first number is knock out (bright blue), last number 96 is control (overexpression))  (0%,25%,50%,..,100%,125%,150%,..250%)
      colors <- colors()[c(27,28,29,30,24,99,115,95,98,97,96)]
      linetype <- c(6,4,3,2,1,6,5,4,3,2,6)
    }
    
    
    writeLines(paste("Model: ", model, ".cps", sep=""))
    writeLines(paste("Scanning variable: ", variable, sep=""))
    #writeLines(outputdir)
    # variables
    inputdir <- c(file.path(outputdir, sim_data_folder))
    outputdir <- c(file.path(outputdir, sim_plots_folder))
    #writeLines(inputdir)
    #writeLines(outputdir)
    
    # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }    

    theme_set(tc_theme(36)) #28
    
    for(k_sim in 1:runs) {
      print(paste('Processing simulation:', k_sim))

	  files <- list.files( path=inputdir, pattern=paste(model, '__sim_', k_sim, '__', sep=""))
	  #print(files)
	  levels.index <- get_sorted_level_indexes(files)
	  #print(levels.index)

	  # Read variable
	  timecourses <- read.table( file.path(inputdir, files[1]), header=TRUE, na.strings="NA", dec=".", sep="\t" )
	  column <- names(timecourses)

	  # let's plot now! :) 

	  for(j in 2:length(column)) {
        print(column[j])

   	    g <- ggplot()
	    for(m in 1:length(levels.index)) {
	        #print(files[levels.index[m]])
            dataset <- read.table(file.path(inputdir,files[levels.index[m]]),header=TRUE,na.strings="NA",
                    dec=".",sep="\t")[,j]
            df <- data.frame(time=timecourses[,1], b=dataset)
            # NOTE: df becomes: time, variable (a factor, with "b" items), value (with previous items in b)	
            df <- melt(df, id=c("time"))
            df$value <- dataset
            df$variable <- as.character(m+10) # No idea why, but it works if m+10 ... 
            
            #print(df$variable)
            g <- g + geom_line(data=df, 
                    aes(x=time, y=value, color=variable, linetype=variable), 
                    size=1.0)
	    }
	    g <- g + xlab(xaxis_label) + ylab(yaxis_label) + ggtitle(column[j]) + 
	         theme(legend.title=element_blank(), legend.position="bottom", legend.key.height=unit(0.5, "in")) +
	         scale_colour_manual("Levels", values=colors, labels=labels) + 
	         scale_linetype_manual("Levels", values=linetype, labels=labels)
        ggsave(file.path(outputdir, paste(model, "__eval_", column[j], "__sim_", k_sim, ".png", sep="" )), 
		   dpi=300,  width=8, height=8)#, bg = "transparent")
   
	  }
	  
  }
  
}



# Plot model single parameter scan time courses using homogeneous lines.
#
# :param model: The model name
# :param variable: The model variable to scan
# :param outputdir: the output directory
# :param sim_data_folder: the name of the folder containing the simulated data
# :param sim_plots_folder: the name of the folder containing the simulated plots
# :param runs: the number of repeated simulations
# :param xaxis_label: the label for the x axis (e.g. Time [min])
# :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
plot_single_param_scan_data_homogen <- function(model, variable, 
					outputdir, sim_data_folder, 
					sim_plots_folder, runs,
					xaxis_label="", yaxis_label="") {
					
    writeLines(paste("Model: ", model, ".cps", sep=""))
    writeLines(paste("Scanning variable: ", variable, sep=""))
    #writeLines(outputdir)
    # variables
    inputdir <- c(file.path(outputdir, sim_data_folder))
    outputdir <- c(file.path(outputdir, sim_plots_folder))
    #writeLines(inputdir)
    #writeLines(outputdir)
    # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }
    
    theme_set(tc_theme(36)) #28
    
    for(k_sim in 1:runs) {
	  files <- list.files( path=inputdir, pattern=paste(model, '__sim_', k_sim, '__', sep=""))
	  # Read variable
	  timecourses <- read.table( file.path(inputdir, files[1]), header=TRUE, na.strings="NA", dec=".", sep="\t" )
	  column <- names(timecourses)
	  
	  for(j in 2:length(column)) {
   	    g <- ggplot()
	    for(m in 1:length(files)) {
            df <- read.table(file.path(inputdir,files[m]),header=TRUE,na.strings="NA",
                    dec=".",sep="\t")[,j]
            df <- data.frame(time=timecourses[,1], value=df)
            g <- g + geom_line(data=df, aes(x=time, y=value), color='blue', size=1.0)   
	    }
	    g <- g + xlab(xaxis_label) + ylab(yaxis_label) + ggtitle(column[j])
        ggsave(file.path(outputdir, paste(model, "__eval_", column[j], "__sim_", k_sim, ".png", sep="" )), 
		   dpi=300,  width=8, height=8)#, bg = "transparent")
	  }
  }
  
}

