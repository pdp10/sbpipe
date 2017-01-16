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
# Object: Plots
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-01 14:14:32 $


library(reshape2)
library(ggplot2)
library(scales)
#library(gridExtra)

require(graphics)


# Plot a generic histogram
#
# :param dfCol: a data frame with exactly one column.
# :param g: the current ggplot to overlap
histogramplot <- function(dfCol, g=ggplot()) {
    g <- g +
        geom_histogram(data=dfCol, aes_string(x=colnames(dfCol)), binwidth=density(dfCol[,])$bw, colour="black", fill="blue") +
        theme(axis.text.x=element_text(vjust = 1))
    return(g)
}



# Plot a scatter plot using a coloured palette
#
# :param df: a data frame
# :param g: the current ggplot to overlap
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param colNameColor: the name of the column whose values are used as 3rd dimension
# :param dot_size: the size of the dots in the scatterplot
# :param colours: the palette to use
# :param limits: the limits for the palette (NULL if no limit is used)
scatterplot_w_colour <- function(df, g=ggplot(), colNameX, colNameY, colNameColor, dot_size=1.0, colours=colorRampPalette(c("blue4", "blue", "cyan", "green", "yellow", "orange", "red", "red4"))(100), limits=NULL) {

# If the third coordinate has equal values, then use the first value (default: red)
  colorCol <- df[,c(colNameColor)]
  countFirst <- length(grep(colorCol[1], colorCol))
  if(countFirst == length(colorCol)) {
    colours <- colours[0:1]
  }

  g <- g + geom_point(data=df, aes_string(x=colNameX, y=colNameY, color=colNameColor), size=dot_size) +
       scale_colour_gradientn(colours=colours, limits) +
       #geom_rug(col="darkblue",alpha=.1) +    
       theme(axis.text.x=element_text(vjust = 1))  
  # #add marginal histograms
  #ggExtra::ggMarginal(g, type = "histogram")
  return(g)
}



# Plot a profile likelihood estimation (PLE) scatter plot
#
# :param df: a data frame
# :param g: the current ggplot to overlap
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param conf_level_66: the 66% confidence level to plot
# :param conf_level_95: the 95% confidence level to plot
# :param dot_size: the size of the dots in the scatterplot
scatterplot_ple <- function(df, g=ggplot(), colNameX, colNameY, conf_level_66, conf_level_95, dot_size=0.1) {
  g <- g +
      geom_point(data=df, aes_string(x=colNameX, y=colNameY), size=dot_size) +
      geom_hline(df.last, aes(yintercept=conf_level_66, color="_66", linetype="_66"), size=2, show.legend=TRUE) +
      geom_hline(df.last, aes(yintercept=conf_level_95, color="_95", linetype="_95"), size=2, show.legend=TRUE) +
      scale_colour_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="blue","_66"="red")) +
      scale_linetype_manual(name="", labels=c("_95"="CL 95%","_66"="CL 66%"), values=c("_95"="dashed", "_66"="dotted")) +
      ylab(expression(chi^{2})) +
      theme(axis.text.x=element_text(vjust = 1))
  return(g)
}



# Plot a profile likelihood estimation (PLE) scatter plot
#
# :param df: a data frame
# :param g: the current ggplot to overlap
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param conf_level_66: the 66% confidence level to plot
# :param conf_level_95: the 95% confidence level to plot
# :param conf_level_99: the 99% confidence level to plot
# :param dot_size: the size of the dots in the scatterplot
scatterplot_ple <- function(df, g=ggplot(), colNameX, colNameY, conf_level_66, conf_level_95, conf_level_99, dot_size=0.1) {
  df.thresholds <- data.frame(conf_level_66, conf_level_95, conf_level_99)
  g <- g +
      geom_point(data=df, aes_string(x=colNameX, y=colNameY), size=dot_size) +
      geom_hline(data=df.thresholds, aes(yintercept=conf_level_66, color="_66", linetype="_66"), size=2, show.legend=TRUE) +
      geom_hline(data=df.thresholds, aes(yintercept=conf_level_66, color="_66", linetype="_66"), size=2, show.legend=TRUE) +
      geom_hline(data=df.thresholds, aes(yintercept=conf_level_95, color="_95", linetype="_95"), size=2, show.legend=TRUE) +
      geom_hline(data=df.thresholds, aes(yintercept=conf_level_99, color="_99", linetype="_99"), size=2, show.legend=TRUE) +
      scale_colour_manual(name="", labels=c("_99"="CL 99%","_95"="CL 95%","_66"="CL 66%"), values=c("_99"="dodgerblue","_95"="green2","_66"="magenta1")) +
#      scale_linetype_manual(name="", labels=c("_99"="CL 99%","_95"="CL 95%","_66"="CL 66%"), values=c("_99"="solid", "_95"="solid", "_66"="solid")) +
      scale_linetype_manual(name="", labels=c("_99"="CL 99%","_95"="CL 95%","_66"="CL 66%"), values=c("_99"="dashed", "_95"="dashed", "_66"="dashed")) +
      guides(colour = guide_legend(reverse=T), linetype = guide_legend(reverse=T)) +
      ylab(expression(chi^{2})) +
      theme(axis.text.x=element_text(vjust = 1))
  return(g)
}



# Plot a generic scatter plot
#
# :param df: a data frame
# :param g: the current ggplot to overlap
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param dot_size: the size of the dots in the scatterplot
scatterplot <-function(df, g=ggplot(), colNameX, colNameY, dot_size=0.5) {
  g <- g +
       geom_point(data=df, aes_string(x=colNameX, y=colNameY), size=dot_size) +
       theme(axis.text.x=element_text(vjust = 1))
  return(g)
}



# Plot a generic scatter plot in log10 scale
#
# :param df: a data frame to trasform to log10 scale
# :param g: the current ggplot to overlap
# :param colNameX: the name of the column for the X axis
# :param colNameY: the name of the column for the Y axis
# :param dot_size: the size of the dots in the scatterplot
scatterplot_log10 <-function(df, g=ggplot(), colNameX, colNameY, dot_size=0.5) {
  df <- log10(df)
  g <- scatterplot(df, g, colNameX, colNameY, dot_size) +
       #scale_x_log10() +
       #scale_y_log10() +
       xlab(paste("log10(", colNameX, ")", sep="")) +
       ylab(paste("log10(", colNameY, ")", sep="")) #+
       #annotation_logticks()
  return(g)
}



# Plot the number of iterations vs Chi^2 in log10 scale.
#
# :param g: the current ggplot to overlap
# :param chi2_array: the array of Chi^2.
plot_fits <- function(chi2_array, g=ggplot()) {
  iters <- c()
  j <- 0
  k <- 0

  # We intentionally consider only the Chi^2 above 100*median(Chi2_array).
  # Often the very first Chi^2 can be extremely large (e^[hundreds]). When so,
  # ggsave() does not process correctly, potentially due to a bug.
  med_chi2 <- median(chi2_array[is.finite(chi2_array)])
  chi2_array <- chi2_array[chi2_array < med_chi2*100]

  for(i in 1:length(chi2_array)) {
    if(k < chi2_array[i]) {
      j <- 0
    }
    iters <- c(iters, j)
    j <- j+1
    k <- chi2_array[i]
  }
  df <- data.frame(Iter=iters, Chi2=chi2_array)
  g <- scatterplot_log10(df, g, "Iter", "Chi2") +
            # Re paint the y lab as we want to use the Greek letter chi.
            ylab(expression(paste("log10(",chi^{2},")", sep="")))
  return(g)
}



# Add experimental data points to a plot. The length of the experimental time course to plot is limited by the length of the simulated time course (=max_sim_tp).
#
# :param df_exp_dataset: the experimental data set
# :param g: the current ggplot to overlap
# :param readout: the name of the readout
# :param max_sim_tp: the maximum simulated time point
plot_raw_dataset <- function(df_exp_dataset, g=ggplot(), readout="time", max_sim_tp=0) {
    # Let's add the experimental data set to the plot
    time <- colnames(df_exp_dataset)[1]
    df_exp_dataset <- df_exp_dataset[df_exp_dataset[1] <= max_sim_tp,]
    g <- g + geom_point(data=df_exp_dataset, aes_string(x=time, y=readout), shape=1, size=2, stroke=1, colour='red2')
    return(g)
}



# Plot repeated time courses in the same plot with mean, 1 standard deviation, and 95% confidence intervals.
#
# :param df: a data frame
# :param g: the current ggplot to overlap
# :param title: the title
# :param xaxis_label: the xaxis label
# :param yaxis_label: the yaxis label
# :param bar_type: the type of bar ("mean", "mean_sd", "mean_sd_ci95")
plot_combined_tc <- function(df, g=ggplot(), title="", xaxis_label="", yaxis_label="", bar_type="mean") {
    mdf <- melt(df,id.vars="Time",variable.name="species",value.name="conc")
    if(bar_type == "mean_sd" || bar_type == "mean_sd_ci95") {
        g <- g + stat_summary(data=mdf, aes(x=Time, y=conc), geom="ribbon", fun.data = mean_sdl, fill="#99CCFF")
        if(bar_type == "mean_sd_ci95") {
            g <- g + stat_summary(data=mdf, aes(x=Time, y=conc), geom="ribbon", fun.data=mean_cl_normal,
                     fun.args=list(conf.int=0.95), fill="#CCFFFF")
        }
    }
    g <- g + stat_summary(data=mdf, aes(x=Time, y=conc), geom="line", fun.y=mean, size=1.0, color="black") +
         xlab(xaxis_label) + ylab(yaxis_label) + ggtitle(title) +
         theme(plot.title = element_text(hjust = 0.5))
    return(g)
}



# Plot repeated time courses in the same plot separately. First column is Time.
#
# :param df: a data frame
# :param g: the current ggplot to overlap
# :param title: the title
# :param xaxis_label: the xaxis label
# :param yaxis_label: the yaxis label
plot_repeated_tc <- function(df, g=ggplot(), title='', xaxis_label="", yaxis_label="") {
    mdf <- melt(df,id.vars="Time",variable.name="species",value.name="conc")
    g <- g + geom_line(data=mdf,aes(x=Time,y=conc,color=species), size=1.0) +
         xlab(xaxis_label) + ylab(yaxis_label) + ggtitle(title) +
         theme(legend.position="none", plot.title = element_text(hjust = 0.5))
    return(g)
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
