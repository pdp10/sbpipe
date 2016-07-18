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


# Plot a histogram
# dfCol : a data frame with exactly one column.
# fileout : the output file name
histogramplot <- function(dfCol, fileout) {
  ggplot(dfCol, aes_string(x=colnames(dfCol))) +
    geom_histogram(binwidth=density(dfCol[,])$bw, colour="black", fill="blue") +
    theme(axis.text.x=element_text(angle = -45, hjust = 0))    
}


# Plot a scatter plot
# df : a data frame
# colNameX : the name of the column for the X axis
# colNameY : the name of the column for the Y axis
# colNameColor : the name of the column whose values are used as 3rd dimension
# fileout : the output file name
scatterplot_w_color <- function(df, colNameX, colNameY, colNameColor, fileout) {
  ggplot(df, aes_string(x=colNameX, y=colNameY, color=colNameColor)) +
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
}


# Plot a scatter plot
# df : a data frame
# colNameX : the name of the column for the X axis
# colNameY : the name of the column for the Y axis
# fileout : the output file name
# conf_level_66 : horizontal line to plot
scatterplot_ple <- function(df, colNameX, colNameY, fileout, conf_level_66, conf_level_95) {
  ggplot(df, aes_string(x=colNameX, y=colNameY)) +
      geom_point(size=0.1) + 
      geom_hline(aes(yintercept=conf_level_66, color="_66", linetype="_66"), size=2, show.legend=TRUE) +
      geom_hline(aes(yintercept=conf_level_95, color="_95", linetype="_95"), size=2, show.legend=TRUE) + 
      scale_colour_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="blue","_66"="red")) +
      scale_linetype_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="dashed", "_66"="dotted")) +
      theme(axis.text.x=element_text(angle = -45, hjust = 0))      
}


scatterplot <-function(df, colNameX, colNameY) {
  ggplot(df, aes_string(x=colNameX, y=colNameY)) +
       geom_point(size=0.1) +
       theme(axis.text.x=element_text(angle = -45, hjust = 0))
}


scatterplot_log10 <-function(df, colNameX, colNameY) {
  scatterplot(df, colNameX, colNameY) + 
       scale_x_continuous(trans=log10_trans(), breaks=c(1,10,100,1000,10000,100000,1000000)) +
       scale_y_continuous(trans=log10_trans(), breaks=c(1,10,100,1000,10000,100000,1000000)) +
       xlab(paste("log10(", colNameX, ")", sep="")) +       
       ylab(paste("log10(", colNameY, ")", sep=""))
}



# plot sensitivity sens_matrix by row in a multi plot
plot.sensitivities <- function(filename, kinetics) {
  sens_matrix <- read.table(filename, header=TRUE, row.names=1, na.strings="NA", dec=".", sep="\t")
  #print(sens_matrix)
  model <- ""
  
  names.row <- row.names(sens_matrix)
  names.col <- names(sens_matrix)
  if(kinetics==FALSE) {
    names.row <- substr(names.row,2, nchar(names.row)-1)
    names.col <- substr(names.col,3, nchar(names.col)-3)
    #names.col <- gsub("unknown", "x", names.col)
    #names.row <- gsub("unknown", "x", names.row)
    #print(names.row)
    #print(names.col)
    png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), height=1000, width=1000, bg="transparent") 
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
 	   main = paste("Initial concentrations sensitivities  -  ", model, sep=""))
  } else{
    names.row <- substr(names.row,2, nchar(names.row)-1)
    names.col <- substr(names.col,3, nchar(names.col)-4)
    names.col <- gsub("phosphorylation", "phosp", names.col)
    #names.col <- gsub("unknown", "x", names.col)
    #names.row <- gsub("unknown", "x", names.row)
    #print(names.row)
    #print(names.col)
    png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), height=1200, width=1200, bg="transparent") 
    heatmap.2(as.matrix(sens_matrix), 
	   key=TRUE, keysize=0.6, symkey=TRUE, 
	   density.info="none", 
           trace="none", 
	   col=diverge_hcl(256), #, c=130, l=c(30,95)),
	   #col=diverge_hsv(256),
           dendrogram="none",
 	   Rowv=NA, Colv=NA, na.rm,
           colsep=c(1:(length(names.col)-1)),
           rowsep=c(1:(length(names.row)-1)),
           sepcolor="white",
           sepwidth=c(0.01,0.01),
 	   scale="none",
 	   labRow=names.row, labCol=names.col, 
 	   margins=c(36,19), cex.main=5, cexRow=2, cexCol=2,
 	   main = paste("Kinetic rates sensitivities  -  ", model, sep=""))
  }

  dev.off()
}



# plot the parameter correlation matrix corr_matrix by row in a multi plot
plot.param_correlations <- function(filename, valmargin, valcex) {
  corr_matrix <- read.table(filename, header=TRUE, row.names=1, na.strings="NA", dec=".", sep="\t")
  #print(corr_matrix)
  model <- ""
  names.row <- row.names(corr_matrix)
  names.col <- names(corr_matrix)
  names.row <- gsub("phosphorylation", "phosp", names.row)
  names.col <- gsub("phosphorylation", "phosp", names.col)
  #names.row <- substr(names.row,2, nchar(names.row)-5)
  #names.col <- substr(names.col,3, nchar(names.col)-5)
  #names.col <- gsub("unknown", "x", names.col)
  #names.row <- gsub("unknown", "x", names.row)
  #print(names.row)
  #print(names.col)
  abs_matrix <- abs(as.matrix(corr_matrix))
  if(model=="General model (phase 2)") {
    png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), height=1800, width=1800, bg="white") 
    heatmap.2(abs_matrix, 
	   key=TRUE, keysize=0.6, symkey=FALSE, 
	   density.info="none", 
           trace="none",
	   denscol="blue",
	   col=rev(c(gray.colors(256) )), # add black "1"
	   symm=TRUE,
           dendrogram="none",
 	   Rowv=NA, Colv=NA, na.rm=TRUE,
 	   scale="none",

           colsep=c(1:(length(names.col)-1)),
           rowsep=c(1:(length(names.row)-1)),
           sepcolor="white",
           sepwidth=c(0.01,0.01),

 	   labRow=names.row, labCol=names.col, 
 	   margins=c(60,60), cex=3, cexRow=3.5, cexCol=3.5,
 	   main = paste("Parameters Correlation Matrix  -  ", model, sep=""))
  } else {

   
   png(paste(substr(filename,0, nchar(filename)-4), ".png", sep="" ), width=11, height=11, units="in", res=300, bg="white")
 
   #tiff(file="test.tiff",width=11, height=11, units="in", res=300)   
    
    heatmap.2(abs_matrix, 
# # 	   key=false, 
# #	   keysize=0.4, 
	   symkey=FALSE, densadj=0.20,
	   density.info="none", 
           trace="none",
	   tracecol="blue",
	   #col=rev(c(gray.colors(256))), # add black "1"
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
# # # 	   margins=c(73,73), cex=3.5, cexRow=3.5, cexCol=3.5,

####### Default
#  	   margins=c(21,21), 
# 	   cex=0.9, cexRow=0.9, cexCol=0.9,

####### Change the values below to adjust it
	   margins=c(valmargin,valmargin), 
	   cex=valcex, cexRow=valcex, cexCol=valcex,

 	   main = paste("Parameters Correlation Matrix  -  ", model, sep=""))
  }
  dev.off()
}










