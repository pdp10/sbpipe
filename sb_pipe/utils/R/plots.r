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
# $Date: 2016-07-01 14:14:32 $



# Plot a histogram
# dfCol : a data frame with exactly one column.
# fileout : the output file name
histogramplot <- function(dfCol, fileout) {
  g = ggplot(dfCol, aes_string(x=colnames(dfCol))) +
    # LEAVE THIS ONE AS IT IS THE ONLY ONE WITH CORRECT Y-AXIS values
    geom_histogram(binwidth=density(dfCol[,])$bw, colour="black", fill="blue")
#     scale_x_continuous(labels=scientific) +
#     scale_y_continuous(labels=scientific)  
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
scatterplot_w_color <- function(df, colNameX, colNameY, colNameColor, fileout) {
  g = ggplot(df, aes_string(x=colNameX, y=colNameY, color=colNameColor)) +
    geom_point() +
    scale_colour_gradientn(colours=rainbow(4))
#     scale_x_continuous(labels=scientific) +
#     scale_y_continuous(labels=scientific)
    #scale_colour_gradient(low="red", high="darkblue") +
    #scale_colour_gradient(low="magenta", high="blue") +
    #geom_rug(col="darkred",alpha=.1)
  ggsave(fileout, dpi=300)
  return(g)
}

# Plot a scatter plot
# df : a data frame
# colNameX : the name of the column for the X axis
# colNameY : the name of the column for the Y axis
# fileout : the output file name
# conf_level_66 : horizontal line to plot
scatterplot_ple <- function(df, colNameX, colNameY, fileout, 
conf_level_66, conf_level_95) {
  g = ggplot(df, aes_string(x=colNameX, y=colNameY)) +
      geom_point() + 
      geom_hline(yintercept=conf_level_66, size=1.5, color="red", linetype=2, show.legend=TRUE) +
      geom_hline(yintercept=conf_level_95, size=1.5, color="blue", linetype=1, show.legend=TRUE) +      
      #scale_linetype_manual(name="", values=c("blue","red"), labels=c("PLE C.I. 95%", "PLE C.I. 66%"))
  ggsave(fileout, dpi=300)
  return(g)
}

