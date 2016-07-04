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
# $Date: 2016-07-01 14:14:32 $


library(ggplot2)


basic_theme <- function (base_size=12, base_family="") {
  theme_bw(base_size=base_size, base_family=base_family) %+replace% 
  theme(aspect.ratio=1,
        axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank())
}



# Plot a histogram
# dfCol : a data frame with exactly one column.
# fileout : the output file name
histogramplot <- function(dfCol, fileout) {
  g = ggplot(dfCol, aes_string(x=colnames(dfCol))) +
    # LEAVE THIS ONE AS IT IS THE ONLY ONE WITH CORRECT Y-AXIS values
    geom_histogram(binwidth=density(dfCol[,])$bw, colour="black", fill="blue") +
    #geom_density(colour="black", fill="blue") +
    #geom_histogram(aes(y = ..density..), binwidth=density(dfCol[,])$bw, colour="black", fill="blue") +
    #geom_density(color="red")
  ggsave(fileout, dpi=300)
  return(g)
}

# Plot a scatter plot
# df : a data frame
# colNameX : the name of the column for the X axis
# colNameY : the name of the column for the Y axis
# colNameColor : the name of the column whose values are used as 3rd dimension
# fileout : the output file name
scatterplot <- function(df, colNameX, colNameY, colNameColor, fileout) {
  g = ggplot(df, aes_string(x=colNameX, y=colNameY, color=colNameColor)) +
    geom_point() +
    scale_colour_gradientn(colours=rainbow(4)) +
    #scale_colour_gradient(low="red", high="darkblue") +
    #scale_colour_gradient(low="magenta", high="blue") +
    #geom_rug(col="darkred",alpha=.1)
  ggsave(fileout, dpi=300)
  return(g)
}



fit_sequence_analysis <- function(filenamein, plots_dir, plot_filename_prefix, best_fits_percent) {
  
  if(best_fits_percent <= 0.0 || best_fits_percent > 100.0) {
    warning("best_fits_percent is not in (0, 100]. Now set to 100")
    best_fits_percent = 100
  }
  
  df = read.csv(filenamein, head=TRUE,sep="\t")
  
  # rename columns
  dfCols <- colnames(df)
  dfCols <- gsub("Values.", "", dfCols)
  dfCols <- gsub("..InitialValue.", "", dfCols)  
  colnames(df) <- dfCols
  
  #print(df)
  
  # sort by Chi^2 and extract threshold row number
  selected_rows <- nrow(df)*best_fits_percent/100
  df <- df[order(df[,2]),]
  df <- df[1:selected_rows,]
  
  #print(df)
  #print(dfCols)
  
  # Set my ggplot theme here
  theme_set(basic_theme(22))
  fileout <- ""
  
  for (i in seq(3,length(dfCols))) { 
    for (j in seq(i, length(dfCols))) {
      if(i==j) {
        fileout <- paste(plots_dir, "/", plot_filename_prefix, dfCols[i], ".png", sep="")
        g <- histogramplot(df[i], fileout)
      } else {
        fileout <- paste(plots_dir, "/", plot_filename_prefix, dfCols[i], "_", dfCols[j], ".png", sep="")
        g <- scatterplot(df, colnames(df)[i], colnames(df)[j], colnames(df)[2], fileout)
      }
    }
  }
  
}

