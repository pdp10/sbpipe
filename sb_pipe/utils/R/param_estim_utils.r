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


library(ggplot2)
# library(scales)
source(file.path(SB_PIPE, 'sb_pipe','utils','R','sb_pipe_ggplot2_themes.r'))
source(file.path(SB_PIPE, 'sb_pipe','utils','R','plots.r'))



final_fits_analysis <- function(filenamein, plots_dir, plot_filename_prefix, best_fits_percent) {
  
  best_fits_percent <- as.numeric(best_fits_percent)
  
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
  
  # Calculate the number of rows to extract.
  selected_rows <- nrow(df)*best_fits_percent/100
  # sort by Chi^2 (descending) so that the low Chi^2 parameter tuples 
  # (which are the most important) are plotted in front. 
  # Then extract the tail from the data frame. 
  df <- df[order(-df[,2]),]
  df <- tail(df, selected_rows)

  
  #print(df)
  #print(dfCols)
  
  # Set my ggplot theme here
  theme_set(basic_theme(22))
  fileout <- ""
  
  for (i in seq(3,length(dfCols))) { 
    for (j in seq(i, length(dfCols))) {
      if(i==j) {
        fileout <- file.path(plots_dir, paste(plot_filename_prefix, dfCols[i], ".png", sep=""))
        g <- histogramplot(df[i], fileout)
      } else {
        fileout <- file.path(plots_dir, paste(plot_filename_prefix, dfCols[i], "_", dfCols[j], ".png", sep=""))
        g <- scatterplot_w_color(df, colnames(df)[i], colnames(df)[j], colnames(df)[2], fileout)
      }
    }
  }
  
}


# m = number of model parameters
# n = number of data points
# p = significance level
compute_fratio_threshold <- function(m, n, p=0.05) {
  1 + (m/(n-m)) * qf(1.0-p, df1=m, df2=n-m)
}

# return the left value confidence interval
leftCI <- function(cut_dataset, full_dataset, chisquare_col_idx, param_col_idx, chisquare_conf_level) {
   # retrieve the minimum parameter value for cut_dataset
    min_ci <- min(cut_dataset[[param_col_idx]])    
    # retrieve the Chi^2 of the parameters with value smaller than the minimum value retrieved from the cut_dataset, within the full dataset. 
    # ...[min95, )  (we are retrieving those ...)
    lt_min_chisquares <- full_dataset[full_dataset[,param_col_idx] < min_ci, chisquare_col_idx] 
    if(min(lt_min_chisquares) < chisquare_conf_level) 
      min_ci <- "inf"
    min_ci
}

# return the right value confidence interval
rightCI <- function(cut_dataset, full_dataset, chisquare_col_idx, param_col_idx, chisquare_conf_level) {
   # retrieve the minimum parameter value for cut_dataset
    max_ci <- max(cut_dataset[[param_col_idx]])    
    # retrieve the Chi^2 of the parameters with value greater than the maximum value retrieved from the cut_dataset, within the full dataset. 
    # (, max95]...  (we are retrieving those ...)
    gt_max_chisquares <- full_dataset[full_dataset[,param_col_idx] > max_ci, chisquare_col_idx] 
    if(min(gt_max_chisquares) < chisquare_conf_level) 
      max_ci <- "inf"
    max_ci
}


all_fits_analysis <- function(filenamein, plots_dir, plot_filename_prefix, data_point_num, fileout_approx_ple_stats) {
  
  data_point_num <- as.numeric(data_point_num)
  
  if(data_point_num <= 0.0) {
    error("data_point_num is negative.")
    return
  }
  
  df = read.csv(filenamein, head=TRUE,sep="\t")
  
  # rename columns
  dfCols <- colnames(df)
  dfCols <- gsub("Values.", "", dfCols)
  dfCols <- gsub("..InitialValue.", "", dfCols)  
  colnames(df) <- dfCols
  
  #print(df)
  
  parameter_num = length(colnames(df)) - 1
  conf_level_99 = compute_fratio_threshold(parameter_num, data_point_num, .01)
  conf_level_95 = compute_fratio_threshold(parameter_num, data_point_num, .05)  
  conf_level_66 = compute_fratio_threshold(parameter_num, data_point_num, .33)
  
  chisquare_at_conf_level_99 <- 0  
  chisquare_at_conf_level_95 <- 0    
  chisquare_at_conf_level_66 <- 0   
  if(length(dfCols) > 1) {
    chisquare_at_conf_level_99 <- min(df[,1]) * conf_level_99  
    chisquare_at_conf_level_95 <- min(df[,1]) * conf_level_95
    chisquare_at_conf_level_66 <- min(df[,1]) * conf_level_66    
  }

  # select the rows with chi^2 smaller than our max threshold
  df99 <- df[df[,1] <= chisquare_at_conf_level_99, ]  
  df95 <- df[df[,1] <= chisquare_at_conf_level_95, ]
  df66 <- df95[df95[,1] <= chisquare_at_conf_level_66, ]  
  
  #print(df95)
  #print(dfCols)
  
  # Set my ggplot theme here
  theme_set(basic_theme(22))
  fileout <- ""

  # plot
  for (i in seq(2,length(dfCols))) { 
    fileout <- file.path(plots_dir, paste(plot_filename_prefix, dfCols[i], ".png", sep=""))
    g <- scatterplot_ple(df95, colnames(df95)[i], colnames(df95)[1], fileout, 
			 chisquare_at_conf_level_66, chisquare_at_conf_level_95)
  }
 
 
  # extract statistics
  min_chisquare <- min(df95[[1]])
  #file.remove(fileout_approx_ple_stats, showWarnings=FALSE)
  fileoutPLE <- sink(fileout_approx_ple_stats)
  
  #file.remove("cancel.txt", showWarnings=FALSE)
  #fileoutPLE <- sink("cancel.txt")
  
  cat(paste("Conf_Level_95", "Conf_Level_66\n", sep="\t"))
  cat(paste(conf_level_95, conf_level_66, sep="\t"), append=TRUE)
  cat("\n\n", append=TRUE)
  cat(paste("Parameter", "Value", "CI_95_left", "CI_95_right", "CI_66_left", "CI_66_right\n", sep="\t"), append=TRUE)      
  for (i in seq(2,length(dfCols))) {
    # retrieve a parameter value associated to the minimum Chi^2
    par_value <- sample(df95[df95[,1] <= min_chisquare, i], 1)    
    # retrieve the confidence intervals
    min_ci_95 <- leftCI(df95, df99, 1, i, chisquare_at_conf_level_95)
    max_ci_95 <- rightCI(df95, df99, 1, i, chisquare_at_conf_level_95)    
    min_ci_66 <- leftCI(df66, df95, 1, i, chisquare_at_conf_level_66)
    max_ci_66 <- rightCI(df66, df95, 1, i, chisquare_at_conf_level_66)
    # save the result
    cat(paste(colnames(df95)[i], par_value, min_ci_95, max_ci_95, min_ci_66, max_ci_66, sep="\t"), append=TRUE)
    cat("\n", append=TRUE)    
  }
  sink()    
}

