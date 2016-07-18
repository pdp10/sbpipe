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
# Object: Plots
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-01 14:14:32 $


library(ggplot2)
#library(gridExtra)


# Plot a histogram
# dfCol : a data frame with exactly one column.
# fileout : the output file name
histogramplot <- function(dfCol, fileout) {
  g = ggplot(dfCol, aes_string(x=colnames(dfCol))) +
    geom_histogram(binwidth=density(dfCol[,])$bw, colour="black", fill="blue") +
    theme(axis.text.x=element_text(angle = -45, hjust = 0))    
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
    scale_colour_gradientn(colours=rainbow(4))+
    #scale_x_continuous(labels=scientific) +
    #scale_y_continuous(labels=scientific)
    #scale_colour_gradient(low="red", high="darkblue") +
    #scale_colour_gradient(low="magenta", high="blue") +
    #geom_rug(col="darkblue",alpha=.1) +    
    theme(axis.text.x=element_text(angle = -45, hjust = 0))
  # #add marginal histograms
  #ggExtra::ggMarginal(g, type = "histogram")    
  return(g)
}


# Plot a scatter plot
# df : a data frame
# colNameX : the name of the column for the X axis
# colNameY : the name of the column for the Y axis
# fileout : the output file name
# conf_level_66 : horizontal line to plot
scatterplot_ple <- function(df, colNameX, colNameY, fileout, conf_level_66, conf_level_95) {
  g = ggplot(df, aes_string(x=colNameX, y=colNameY)) +
      geom_point(size=0.1) + 
      geom_hline(aes(yintercept=conf_level_66, color="_66", linetype="_66"), size=2, show.legend=TRUE) +
      geom_hline(aes(yintercept=conf_level_95, color="_95", linetype="_95"), size=2, show.legend=TRUE) + 
      scale_colour_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="blue","_66"="red")) +
      scale_linetype_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="dashed", "_66"="dotted")) +
      theme(axis.text.x=element_text(angle = -45, hjust = 0))      
  return(g)
}

