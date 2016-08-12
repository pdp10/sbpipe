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
# Object: Plotting of time courses columns wrt time. 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-6 12:14:32 $


 
library(ggplot2)

# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(file.path(SB_PIPE, 'sb_pipe','utils','R','sb_pipe_ggplot2_themes.r'))
source(file.path(SB_PIPE, 'sb_pipe','utils','R','plots.r'))


plot_double_param_scan_data <- function(model_noext, scanned_par1, scanned_par2, inputdir, outputdir) {
	
    theme_set(tc_theme(24))    
    
    writeLines(paste("1st var: ", scanned_par1, sep=""))
    writeLines(paste("2st var: ", scanned_par2, sep=""))    
    # create the directory of output
    if (!file.exists(outputdir)){ 
	dir.create(outputdir) 
    }

    df <- read.table(file.path(inputdir, paste(model_noext, ".csv", sep="")), header=TRUE, na.strings="NA", dec=".", sep="\t")
    
    # discard the first column (Time) and the columns of the two scanned parameters
    columns2discard <- c(colnames(df)[1], scanned_par1, scanned_par2)
    df.compact <- df[,!(colnames(df) %in% columns2discard)]
    # extract the tuples with minimum and maximum values. These are used for scaling the plot colours.    
    min_values <- apply(df.compact, 2, min)
    max_values <- apply(df.compact, 2, max)  
    # extract the columns
    columns <- colnames(df.compact)

    # Iterate for each file representing time point data
    files <- list.files(path=inputdir, pattern=paste(model_noext, '__tp_', sep=""))
    files <- sort(files)
    
    # Extract the coordinates of the data frame to plot
    df.coordinates <- data.frame()
    if(length(files) > 0) {
      df.tp <- read.table(file.path(inputdir, files[1]), header=TRUE, na.strings="NA", dec=".", sep="\t")
      df.coordinates <- subset(df.tp, select=c(scanned_par1, scanned_par2))
    }
    #print(df.coordinates)

    # Construct a generic palette
    colfunc <- colorRampPalette(c("red","yellow2","springgreen","dodgerblue", "purple"))
    #colfunc <- colorRampPalette(c("red","yellow","springgreen","navyblue"))
    palette.generic <- colfunc(100)    
    
    for(k in 1:length(files)) { 
      print(paste('Processing file:', files[k], sep=" "))
      # Read variable
      df.tp <- read.table(file.path(inputdir, files[k]), header=TRUE, na.strings="NA", dec=".", sep="\t")

      for(i in 1:length(columns)) {
          # add the column to plot (the colour) to the coordinate data in df.coordinates
	  df.plot <- data.frame(df.coordinates, subset(df.tp, select=c(columns[i])))

	  # Calculate the range of interest for this palette so that the colours are better represented.
	  # Therefore, scale the column min/max for this time point by column min/max of the whole time course
	  # so that the colour bar for each plot (time point) is consistent throught the time course.
  	  col.min <- min(df.plot[,c(columns[i])])
	  col.max <- max(df.plot[,c(columns[i])])
	  colour.minidx <- as.integer(col.min*100/max_values[i])
	  colour.maxidx <- as.integer(col.max*100/max_values[i])
	  if(colour.minidx == colour.maxidx) { 
	    colour.maxidx <- colour.maxidx + 1 
	  }
	  palette.plot <- palette.generic[colour.minidx:colour.maxidx]

	  g <- scatterplot_w_colour(df.plot, scanned_par1, scanned_par2, columns[i], colours=palette.plot) + 
	       ggtitle(paste(columns[i], ", time=", k-1, sep=""))
	  ggsave(file.path(outputdir, paste(model_noext, "__eval_", columns[i], "__tp_", k-1, ".png", sep="" )), 
		dpi=300,  width=8, height=6)
      }
  }
  
}


