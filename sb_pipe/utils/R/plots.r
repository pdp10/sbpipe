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
library(scales)
#library(gridExtra)

require(graphics)


# Plot a generic histogram
#
# :param dfCol: a data frame with exactly one column.
histogramplot <- function(dfCol) {
  ggplot(dfCol, aes_string(x=colnames(dfCol))) +
    geom_histogram(binwidth=density(dfCol[,])$bw, colour="black", fill="blue") + 
    theme(axis.text.x=element_text(vjust = 1))    
}



# Plot a scatter plot using a coloured palette
#
# :param df: a data frame
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param colNameColor: the name of the column whose values are used as 3rd dimension
# :param dot_size: the size of the dots in the scatterplot
# :param colours: the palette to use
# :param limits: the limits for the palette (NULL if no limit is used)
scatterplot_w_colour <- function(df, colNameX, colNameY, colNameColor, dot_size=1.0, colours=colorRampPalette(c("blue4", "blue", "cyan", "green", "yellow", "orange", "red", "red4"))(100), limits=NULL) {

# If the third coordinate has equal values, then use the first value (default: red)
  colorCol <- df[,c(colNameColor)]
  countFirst <- length(grep(colorCol[1], colorCol))
  if(countFirst == length(colorCol)) {
    colours <- colours[0:1]
  }

  g <- ggplot(df, aes_string(x=colNameX, y=colNameY, color=colNameColor))
  g <- g + geom_point(size=dot_size) +
       scale_colour_gradientn(colours=colours, limits) +
       #geom_rug(col="darkblue",alpha=.1) +    
       theme(axis.text.x=element_text(vjust = 1))  
  # #add marginal histograms
  #ggExtra::ggMarginal(g, type = "histogram")
}



# Plot a profile likelihood estimation (PLE) scatter plot
#
# :param df: a data frame
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param conf_level_66: the 66% confidence level to plot
# :param conf_level_95: the 95% confidence level to plot
# :param dot_size: the size of the dots in the scatterplot
scatterplot_ple <- function(df, colNameX, colNameY, conf_level_66, conf_level_95, dot_size=0.1) {
  ggplot(df, aes_string(x=colNameX, y=colNameY)) +
      geom_point(size=dot_size) + 
      geom_hline(aes(yintercept=conf_level_66, color="_66", linetype="_66"), size=2, show.legend=TRUE) +
      geom_hline(aes(yintercept=conf_level_95, color="_95", linetype="_95"), size=2, show.legend=TRUE) + 
      scale_colour_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="blue","_66"="red")) +
      scale_linetype_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="dashed", "_66"="dotted")) +
      theme(axis.text.x=element_text(vjust = 1)) 
}



# Plot a profile likelihood estimation (PLE) scatter plot
#
# :param df: a data frame
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param conf_level_66: the 66% confidence level to plot
# :param conf_level_95: the 95% confidence level to plot
# :param conf_level_99: the 99% confidence level to plot
# :param dot_size: the size of the dots in the scatterplot
scatterplot_ple <- function(df, colNameX, colNameY, conf_level_66, conf_level_95, conf_level_99, dot_size=0.1) {
  ggplot(df, aes_string(x=colNameX, y=colNameY)) +
      geom_point(size=dot_size) + 
      geom_hline(aes(yintercept=conf_level_66, color="_66", linetype="_66"), size=2, show.legend=TRUE) +
      geom_hline(aes(yintercept=conf_level_95, color="_95", linetype="_95"), size=2, show.legend=TRUE) +
      geom_hline(aes(yintercept=conf_level_99, color="_99", linetype="_99"), size=2, show.legend=TRUE) +       
      scale_colour_manual(name="", labels=c("_99"="CL 99%","_95"="CL 95%","_66"="CL 66%"), values=c("_99"="slategrey","_95"="blue","_66"="red")) +
      scale_linetype_manual(name="", labels=c("_99"="CL 99%","_95"="CL 95%","_66"="CL 66%"), values=c("_99"="twodash", "_95"="dashed", "_66"="dotted")) +
      theme(axis.text.x=element_text(vjust = 1)) 
}



# Plot a generic scatter plot
#
# :param df: a data frame
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param dot_size: the size of the dots in the scatterplot
scatterplot <-function(df, colNameX, colNameY, dot_size=0.5) {
  ggplot(df, aes_string(x=colNameX, y=colNameY)) +
       geom_point(size=dot_size) +    
       theme(axis.text.x=element_text(vjust = 1)) 
}



# Plot a generic scatter plot in log10 scale
#
# :param df: a data frame
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param dot_size: the size of the dots in the scatterplot
scatterplot_log10 <-function(df, colNameX, colNameY, dot_size=0.5) {
  scatterplot(df, colNameX, colNameY, dot_size) + 
       scale_x_log10() + #continuous(trans=log10_trans()) +
       scale_y_log10() + #continuous(trans=log10_trans()) +
       xlab(paste("log10(", colNameX, ")", sep="")) +       
       ylab(paste("log10(", colNameY, ")", sep="")) +          
       annotation_logticks() 
}



# Plot a sensitivity matrix from a file containing a sensitivity table using a heatmap
#
# :param filename: the filename containing the sensitivity table
plot.sensitivities <- function(filename) {
  sens_matrix <- read.table(filename, header=TRUE, row.names=1, na.strings="NA", dec=".", sep="\t")
  #print(sens_matrix)
  
  names.row <- row.names(sens_matrix)
  names.col <- names(sens_matrix)

  names.row <- substr(names.row,2, nchar(names.row)-1)
  names.col <- substr(names.col,3, nchar(names.col)-3)
  png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), width=11, height=11, units="in", res=300, bg="white")
  heatmap.2(as.matrix(sens_matrix), 
            key=TRUE, keysize=0.6, symkey=TRUE, 
            density.info="none", 
            trace="none", 
            col=diverge_hcl(256), #c=130, l=c(30,95)),
            #col=diverge_hsv(256),
            dendrogram="none",
            Rowv=NA, Colv=NA, na.rm,
            colsep=c(1:(length(names.col)-1)),
            rowsep=c(1:(length(names.row)-1)),
            sepcolor="white",
            sepwidth=c(0.01,0.01),
            scale="none",
            labRow=names.row, labCol=names.col, 
            margins=c(19,19), cex.main=5, cexRow=2, cexCol=2,
            main = "")
  dev.off()
}



# Plot the parameter correlation matrix by row using a heatmap
# 
# :param filename: the filename containing the parameter correlation table
# :param valmargin: the margins for the heatmap
# :param valcex: the cex (font size) value.
plot.param_correlations <- function(filename, valmargin, valcex) {
  corr_matrix <- read.table(filename, header=TRUE, row.names=1, na.strings="NA", dec=".", sep="\t")
  #print(corr_matrix)
  model <- ""
  names.row <- row.names(corr_matrix)
  names.col <- names(corr_matrix)
  abs_matrix <- abs(as.matrix(corr_matrix))

  png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), width=11, height=11, units="in", res=300, bg="white")
  #tiff(file="test.tiff",width=11, height=11, units="in", res=300)   
    
  heatmap.2(abs_matrix, 
            # key=false, 
            # keysize=0.4, 
            symkey=FALSE,
            densadj=0.20,
            density.info="none", 
            trace="none",
            tracecol="blue",
            # col=rev(c(gray.colors(256))), # add black "1"
            col=rev(c("1",  gray.colors(256))), # add black "1"
            symm=TRUE,
            dendrogram="none",
            Rowv=NA, Colv=NA, na.rm=TRUE,
            scale="none",

            colsep=c(1:(length(names.col)-1)),
            rowsep=c(1:(length(names.row)-1)),
            sepcolor="white",
            sepwidth=c(0.01,0.01),

            labRow=names.row, labCol=names.col,
            # margins=c(73,73), cex=3.5, cexRow=3.5, cexCol=3.5,
            # margins=c(21,21), cex=0.9, cexRow=0.9, cexCol=0.9,
            margins=c(valmargin,valmargin), cex=valcex, cexRow=valcex, cexCol=valcex,

            main = "Parameters Correlation Matrix")
  dev.off()
}
