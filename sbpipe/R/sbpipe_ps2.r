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

# retrieve SBpipe folder containing R scripts
args <- commandArgs(trailingOnly = FALSE)
SBPIPE_R <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))
source(file.path(SBPIPE_R, 'sbpipe_plots.r'))
source(file.path(SBPIPE_R, 'sbpipe_ggplot2_themes.r'))




# Plot model double parameter scan time courses.
#
# :param model: the model name without extension
# :param scanned_par1: the 1st scanned parameter
# :param scanned_par2: the 2nd scanned parameter
# :param inputdir: the input directory
# :param outputdir: the output directory
# :param run: the simulation run
plot_double_param_scan_data <- function(model, scanned_par1, scanned_par2, inputdir, outputdir, run) {

    theme_set(basic_theme(36))

    writeLines(paste("1st var: ", scanned_par1, sep=""))
    writeLines(paste("2st var: ", scanned_par2, sep=""))
    # create the directory of output
    if (!file.exists(outputdir)){
        dir.create(outputdir)
    }

    # EXTRACT the tuples of min and max values FROM the complete dataset. Doing so, we don't need to iterate.
    df <- read.table(file.path(inputdir, paste(model, "_", run, ".csv", sep="")), header=TRUE,
                     na.strings="NA", dec=".", sep="\t")

    # discard the first column (Time) and the columns of the two scanned parameters
    columns2discard <- c(colnames(df)[1], scanned_par1, scanned_par2)
    # drop=FALSE is necessary because we don't want R converts 1 data frames into an array.
    df.compact <- df[,!(colnames(df) %in% columns2discard), drop = FALSE]
    # extract the tuples with minimum and maximum values. These are used for scaling the plot colours.
    df.compact <- data.frame(df.compact)
    min_values <- apply(df.compact, 2, min)
    max_values <- apply(df.compact, 2, max)

    # extract the columns
    columns <- colnames(df.compact)

    # READ the files containing the time points. These will be plotted.

    # Iterate for each file representing time point data
    files <- list.files(path=inputdir, pattern=paste(model, '__rep_', run, '__tp_', sep=""))
    files <- sort(files)

    if(length(files) < 1) {
        return
    }


    df.coordinates <- data.frame()
    # Extract the coordinates of the data frame to plot
    if(length(files) > 0)
        df.tp <- read.table(file.path(inputdir, files[1]), header=TRUE, na.strings="NA", dec=".", sep="\t")
        df.coordinates <- subset(df.tp, select=c(scanned_par1, scanned_par2))
    #print(df.coordinates)

    # Construct a generic palette
    colfunc <- colorRampPalette(c("blue4", "blue", "cyan", "green", "yellow", "orange", "red", "red4"))
    palette.generic <- colfunc(100)

    for(j in 1:length(files)) {
      print(paste('Processing file:', files[j], sep=" "))
      # Read variable
      df.tp <- read.table(file.path(inputdir, files[j]), header=TRUE, na.strings="NA", dec=".", sep="\t")

      for(k in 1:length(columns)) {
        # add the column to plot (the colour) to the coordinate data in df.coordinates
        df.plot <- data.frame(df.coordinates, subset(df.tp, select=c(columns[k])))

        # Calculate the range of interest for this palette so that the colours are better represented.
        # Therefore, scale the column min/max for this time point by column min/max of the whole time course
        # so that the colour bar for each plot (time point) is consistent through the time course.
        col.min <- min(df.plot[,c(columns[k])])
        col.max <- max(df.plot[,c(columns[k])])
        colour.minidx <- as.integer(col.min*100/max_values[k])
        colour.maxidx <- as.integer(col.max*100/max_values[k])
        if(colour.minidx == colour.maxidx) {
            colour.maxidx <- colour.maxidx + 1
        }
        palette.plot <- palette.generic[colour.minidx:colour.maxidx]

        g <- scatterplot_w_colour(df.plot, ggplot(), scanned_par1, scanned_par2, columns[k], colours=palette.plot) +
            ggtitle(paste(columns[k], ", t=", j-1, sep="")) +
            theme(legend.key.height = unit(0.5, "in"), plot.title = element_text(hjust = 0.5))
        ggsave(file.path(outputdir, paste(model, "__eval_", columns[k], '__rep_', run, "__tp_", j-1, ".png", sep="" )),
            dpi=300,  width=8, height=6)
      }
  }
}