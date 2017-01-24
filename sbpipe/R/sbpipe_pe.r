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
# $Date: 2016-07-01 14:14:32 $


library(ggplot2)
#library(scales)
source(file.path(SBPIPE, 'sbpipe','R','sbpipe_ggplot2_themes.r'))
source(file.path(SBPIPE, 'sbpipe','R','sbpipe_plots.r'))




# Compute the fratio threshold for the confidence level. 
#
# :param m: number of model parameters
# :param n: number of data points
# :param p: significance level
compute_fratio_threshold <- function(m, n, p=0.05) {
  1 + (m/(n-m)) * qf(1.0-p, df1=m, df2=n-m)
}



# Return the left value confidence interval.
#
# :param cut_dataset: a subset of the full dataset (e.g. the best 66%, the best 95%)
# :param full_dataset: the full dataset
# :param chi2_col_idx: the index for the Chi^2 column in the dataset
# :param param_col_idx: the index for the parameter column in the dataset
# :param chi2_conf_level: the Chi^2 confidence level
leftCI <- function(cut_dataset, full_dataset, chi2_col_idx, param_col_idx, chi2_conf_level) {
  # retrieve the minimum parameter value for cut_dataset
  min_ci <- min(cut_dataset[,param_col_idx])    
  # retrieve the Chi^2 of the parameters with value smaller than the minimum value retrieved from the cut_dataset, within the full dataset. 
  # ...[min95, )  (we are retrieving those ...)
  lt_min_chi2s <- full_dataset[full_dataset[,param_col_idx] < min_ci, chi2_col_idx]
  if(length(lt_min_chi2s) == 0 || min(lt_min_chi2s) <= chi2_conf_level) {
    min_ci <- "-inf"
  }
  min_ci
}



# Return the right value confidence interval.
#
# :param cut_dataset: a subset of the full dataset (e.g. the best 66%, the best 95%)
# :param full_dataset: the full dataset
# :param chi2_col_idx: the index for the Chi^2 column in the dataset
# :param param_col_idx: the index for the parameter column in the dataset
# :param chi2_conf_level: the Chi^2 confidence level
rightCI <- function(cut_dataset, full_dataset, chi2_col_idx, param_col_idx, chi2_conf_level) {
  # retrieve the minimum parameter value for cut_dataset
  max_ci <- max(cut_dataset[,param_col_idx])    
  # retrieve the Chi^2 of the parameters with value greater than the maximum value retrieved from the cut_dataset, within the full dataset. 
  # (, max95]...  (we are retrieving those ...)
  gt_max_chi2s <- full_dataset[full_dataset[,param_col_idx] > max_ci, chi2_col_idx] 
  if(length(gt_max_chi2s) == 0 || min(gt_max_chi2s) <= chi2_conf_level) {
    max_ci <- "+inf"
  }
  max_ci
}




# Rename data frame columns. `ObjectiveValue` is renamed as `Chi2`. Substrings `Values.` and `..InitialValue.` are 
# removed. 
# 
# :param dfCols: The columns of a data frame.
replace_colnames <- function(dfCols) {
  dfCols <- gsub("ObjectiveValue", "chi2", dfCols)
  dfCols <- gsub("Values.", "", dfCols)
  dfCols <- gsub("..InitialValue.", "", dfCols)
}



# Plot parameter correlations. 
# 
# :param df: the data frame
# :param dfCols: the columns of the data frame. Each column is a parameter. Only parameters to the left of chi2_col_idx are plotted. 
# :param plots_dir: the directory for storing the plots
# :param plot_filename_prefix: the prefix for the plot filename
# :param title: the plot title (default: "")
# :param chi2_col_idx: the index of the column containing the Chi^2 (default: 1)
# :param logspace: true if the parameters should be plotted in logspace (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
plot_parameter_correlations <- function(df, dfCols, plots_dir, plot_filename_prefix, title="", chi2_col_idx=1, 
                                        logspace=TRUE, scientific_notation=TRUE) {
  fileout <- ""
  for (i in seq(chi2_col_idx+1,length(dfCols))) {
    print(paste('sampled param corr (', title, ') for ', dfCols[i], sep=''))
    for (j in seq(i, length(dfCols))) {
    for (j in seq(i, length(dfCols))) {
      g <- ggplot()
      if(i==j) {
        fileout <- file.path(plots_dir, paste(plot_filename_prefix, dfCols[i], ".png", sep=""))
        g <- histogramplot(df[i], g) + ggtitle(title)
        if(logspace) {
            g <- g + xlab(paste("log10(",dfCols[i],")",sep=""))
        }
      } else {
        fileout <- file.path(plots_dir, paste(plot_filename_prefix, dfCols[i], "_", dfCols[j], ".png", sep=""))
        g <- scatterplot_w_colour(df, g, colnames(df)[i], colnames(df)[j], colnames(df)[chi2_col_idx]) +
             ggtitle(bquote(chi^2: .(title))) +
             theme(legend.key.height = unit(0.5, "in"))
        if(logspace) {
            g <- g + xlab(paste("log10(",dfCols[i],")",sep="")) + ylab(paste("log10(",dfCols[j],")",sep=""))
        }        
      }
      if(scientific_notation) {
         g <- g + scale_x_continuous(labels=scientific) + scale_y_continuous(labels=scientific)
      }
      ggsave(fileout, dpi=300, width=8, height=6)
    }    
  }
}


# Plot the Chi^2 vs Iterations
# 
# :param df: the complete data frame
# :param chi2_col: the chi2 column name
# :param plots_dir: the directory to save the generated plots
# :param model: the model name
plot_chi2_vs_iters <- function(df, chi2_col, plots_dir, model) {
    print('plotting chi^2 vs iterations')
    # save the chi2 vs iteration
    g <- plot_fits(df[,chi2_col], ggplot()) + ggtitle(expression(paste(chi^{2}, " vs iters", sep="")))
    ggsave(file.path(plots_dir, paste(model, "_chi2_vs_iters.png", sep="")), dpi=300, width=8, height=6)
}


# Plot the sampled profile likelihood estimations (PLE)
# 
# :param df99: the 99% confidence level data frame
# :param chi2_col: the chi2 column name
# :param cl66_chi2: the 66% confidence level chi2
# :param cl95_chi2: the 95% confidence level chi2
# :param cl99_chi2: the 99% confidence level chi2
# :param plots_dir: the directory to save the generated plots
# :param model: the model name
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
plot_sampled_ple <- function(df99, chi2_col, cl66_chi2, cl95_chi2, cl99_chi2, plots_dir, model,
                            logspace=TRUE, scientific_notation=TRUE) { 
    dfCols <- colnames(df99)
    for (i in seq(2,length(dfCols))) {
        print(paste('sampled PLE for', dfCols[i]))
        # extract statistics  
        fileout <- file.path(plots_dir, paste(model, "_approx_ple_", dfCols[i], ".png", sep=""))
        g <- scatterplot_ple(df99, ggplot(), dfCols[i], chi2_col, cl66_chi2, cl95_chi2, cl99_chi2) +
            theme(legend.key.height = unit(0.5, "in"))    
#       g <- scatterplot_ple(df95, ggplot(), dfCols[i], chi2_col, cl66_chi2, cl95_chi2) +
#            theme(legend.key.height = unit(0.5, "in"))
        if(logspace) {
            g <- g + xlab(paste("log10(",dfCols[i],")",sep=""))
        }
        if(scientific_notation) {
            g <- g + scale_x_continuous(labels=scientific) + scale_y_continuous(labels=scientific)
        }
        g <- g + ggtitle("Sampled PLE")
        ggsave(fileout, dpi=300, width=8, height=6)

        # Add density information (removed as it was not showing much more..)
        #g <- g + stat_density2d(color="green")
        #fileout = gsub('.png', '_density.png', fileout)
        #ggsave(fileout, dpi=300, width=8, height=6)
    }
}


# Compute the confidence level based on the minimum chi^2. 
#
# :param min_chi2: the minimum chi^2
# :param params: the number of parameters
# :param data_points: the number of data points
# :param level: the confidence level threshold (e.g. 0.1, 0.5)
compute_cl_chi2 <- function(min_chi2, params, data_points, level=0.5) {
    min_chi2 * compute_fratio_threshold(params, data_points, level) 
}


# Plot parameter correlations using the 66%, 95%, or 99% confidence level data sets
# 
# :param df66: the data frame filtered at 66%
# :param df95: the data frame filtered at 95%
# :param df99: the data frame filtered at 95%
# :param chi2_col: the chi2 column name
# :param plots_dir: the directory to save the generated plots
# :param model: the model name
# :param plot_2d_66cl_corr: true if the 2D parameter correlation plots for 66% confidence intervals should be plotted. This is time consuming. (default: FALSE)
# :param plot_2d_95cl_corr: true if the 2D parameter correlation plots for 95% confidence intervals should be plotted. This is time consuming. (default: FALSE)
# :param plot_2d_99cl_corr: true if the 2D parameter correlation plots for 99% confidence intervals should be plotted. This is time consuming. (default: FALSE)
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
plot_2d_cl_corr <- function(df66, df95, df99, chi2_col, plots_dir, model, 
                            plot_2d_66cl_corr=FALSE, plot_2d_95cl_corr=FALSE, plot_2d_99cl_corr=FALSE, 
                            logspace=TRUE, scientific_notation=TRUE) {
  dfCols <- colnames(df99)
  if(plot_2d_66cl_corr) {
    plot_parameter_correlations(df66[order(-df66[,chi2_col]),], dfCols, plots_dir, paste(model, "_ci66_fits_", sep=""), "CI66 fits", which(dfCols==chi2_col), logspace, scientific_notation)
  }
  if(plot_2d_95cl_corr) {
    plot_parameter_correlations(df95[order(-df95[,chi2_col]),], dfCols, plots_dir, paste(model, "_ci95_fits_", sep=""), "CI95 fits", which(dfCols==chi2_col), logspace, scientific_notation)
  }
  if(plot_2d_99cl_corr) {
    plot_parameter_correlations(df99[order(-df99[,chi2_col]),], dfCols, plots_dir, paste(model, "_ci99_fits_", sep=""), "CI99 fits", which(dfCols==chi2_col), logspace, scientific_notation)
  }  
}


    
# Compute the table for the sampled PLE statistics.
#
# :param df66: the data frame filtered at 66%
# :param df95: the data frame filtered at 95%
# :param df99: the data frame filtered at 95%
# :param df: the complete data frame
# :param chi2_col: the chi2 column name
# :param chi2_col_idx: the chi2 column index
# :param param_col_idx: the param column index
# :param cl66_chi2: the 66% confidence level chi2
# :param cl95_chi2: the 95% confidence level chi2
# :param cl99_chi2: the 99% confidence level chi2
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
compute_sampled_ple_stats <- function(df66, df95, df99, df, chi2_col, chi2_col_idx, param_col_idx, 
                                        cl66_chi2, cl95_chi2, cl99_chi2, logspace=TRUE) {

    min_chi2 <- min(df99[,chi2_col])                                         
    par_value <- sample(df99[df99[,chi2_col] <= min_chi2, param_col_idx], 1)
    
    min_ci_66 <- leftCI(df66, df95, chi2_col_idx, param_col_idx, cl66_chi2)
    max_ci_66 <- rightCI(df66, df95, chi2_col_idx, param_col_idx, cl66_chi2)    
    min_ci_95 <- "-inf"
    max_ci_95 <- "+inf"    
    min_ci_99 <- "-inf"
    max_ci_99 <- "+inf"
    if(is.numeric(min_ci_66)) { min_ci_95 <- leftCI(df95, df99, chi2_col_idx, param_col_idx, cl95_chi2) }
    if(is.numeric(max_ci_66)) { max_ci_95 <- rightCI(df95, df99, chi2_col_idx, param_col_idx, cl95_chi2) }
    if(is.numeric(min_ci_95)) { min_ci_99 <- leftCI(df99, df, chi2_col_idx, param_col_idx, cl99_chi2) }
    if(is.numeric(max_ci_95)) { max_ci_99 <- rightCI(df99, df, chi2_col_idx, param_col_idx, cl99_chi2) }
    
    if(logspace) {
        # log10 inverse
        par_value <- 10^par_value
        if(is.numeric(min_ci_99)) { min_ci_99 <- 10^min_ci_99 }
        if(is.numeric(max_ci_99)) { max_ci_99 <- 10^max_ci_99 }      
        if(is.numeric(min_ci_95)) { min_ci_95 <- 10^min_ci_95 }
        if(is.numeric(max_ci_95)) { max_ci_95 <- 10^max_ci_95 }
        if(is.numeric(min_ci_66)) { min_ci_66 <- 10^min_ci_66 }
        if(is.numeric(max_ci_66)) { max_ci_66 <- 10^max_ci_66 }      
    }
    min_ci_99_par_value_ratio <- "-inf"
    max_ci_99_par_value_ratio <- "+inf"    
    min_ci_95_par_value_ratio <- "-inf"
    max_ci_95_par_value_ratio <- "+inf"
    min_ci_66_par_value_ratio <- "-inf"
    max_ci_66_par_value_ratio <- "+inf"
    if(is.numeric(min_ci_99) && min_ci_99 != 0) {
        min_ci_99_par_value_ratio <- round(par_value/min_ci_99, digits=6)
    }
    if(is.numeric(max_ci_99) && par_value != 0) {
        max_ci_99_par_value_ratio <- round(max_ci_99/par_value, digits=6)
    }    
    if(is.numeric(min_ci_95) && min_ci_95 != 0) {
        min_ci_95_par_value_ratio <- round(par_value/min_ci_95, digits=6)
    }
    if(is.numeric(max_ci_95) && par_value != 0) {
        max_ci_95_par_value_ratio <- round(max_ci_95/par_value, digits=6)
    }
    if(is.numeric(min_ci_66) && min_ci_66 != 0) {
        min_ci_66_par_value_ratio <- round(par_value/min_ci_66, digits=6)
    }
    if(is.numeric(max_ci_66) && par_value != 0) {
        max_ci_66_par_value_ratio <- round(max_ci_66/par_value, digits=6)
    }

    ret_list <- list("par_value"=par_value, 
                "min_ci_66"=min_ci_66, "max_ci_66"=max_ci_66,  
                "min_ci_95"=min_ci_95, "max_ci_95"=max_ci_95,  
                "min_ci_99"=min_ci_99, "max_ci_99"=max_ci_99,                  
                "min_ci_66_par_value_ratio"=min_ci_66_par_value_ratio, "max_ci_66_par_value_ratio"=max_ci_66_par_value_ratio, 
                "min_ci_95_par_value_ratio"=min_ci_95_par_value_ratio, "max_ci_95_par_value_ratio"=max_ci_95_par_value_ratio, 
                "min_ci_99_par_value_ratio"=min_ci_99_par_value_ratio, "max_ci_99_par_value_ratio"=max_ci_99_par_value_ratio)
    return(ret_list)
}


# Compute the Akaike Information Criterion. Assuming additive Gaussian 
# measurement noise of width 1, the term -2ln(L(theta|y)) ~ SSR ~ Chi^2
# 
# :param chi2: the Chi^2 for the model
# :param k: the number of model parameters
compute_aic <- function(chi2, k) {
    chi2 + 2*k
}


# Compute the corrected Akaike Information Criterion. Assuming additive Gaussian 
# measurement noise of width 1, the term -2ln(L(theta|y)) ~ SSR ~ Chi^2
# 
# :param chi2: the Chi^2 for the model
# :param k: the number of model parameters
# :param n: the number of data points
compute_aicc <- function(chi2, k, n) {
    compute_aic(chi2, k) + (2*k*(k+1))/(n-k-1)
}


# Compute the Bayesian Information Criterion. Assuming additive Gaussian 
# measurement noise of width 1, the term -2ln(L(theta|y)) ~ SSR ~ Chi^2
# 
# :param chi2: the Chi^2 for the model
# :param k: the number of model parameters
# :param n: the number of data points
compute_bic <- function(chi2, k, n) {
    chi2 + k*log(n)
}


# Run model parameter estimation analysis and plot results. This script analyses
# all fits.
#
# :param model: the model name without extension
# :param filenamein: the dataset containing the parameter estimation data.
# :param plots_dir: the directory to save the generated plots
# :param data_point_num: the number of data points used for parameterise the model
# :param fileout_param_estim_details: the name of the file containing the detailed statistics for the estimated parameters
# :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation
# :param plot_2d_66cl_corr: true if the 2D parameter correlation plots for 66% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param plot_2d_95cl_corr: true if the 2D parameter correlation plots for 95% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param plot_2d_99cl_corr: true if the 2D parameter correlation plots for 99% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
all_fits_analysis <- function(model, filenamein, plots_dir, data_point_num, fileout_param_estim_details, fileout_param_estim_summary, plot_2d_66cl_corr=FALSE, plot_2d_95cl_corr=FALSE, plot_2d_99cl_corr=FALSE, logspace=TRUE, scientific_notation=TRUE) {

  data_point_num <- as.numeric(data_point_num)
  if(data_point_num <= 0.0) {
    error("data_point_num is non positive.")
    return
  }
  
  df = read.csv(filenamein, head=TRUE, dec=".", sep="\t")
   
  dfCols <- replace_colnames(colnames(df))
  colnames(df) <- dfCols
  chi2_col_idx <- 1
  chi2_col <- dfCols[chi2_col_idx]

  if(logspace) {
    # Transform the parameter space to a log10 parameter space. 
    # The column for the Chi^2 score is maintained instead. 
    df[,-chi2_col_idx] <- log10(df[,-chi2_col_idx])
  }
  
  parameter_num = length(colnames(df)) - 1
  # compute the confidence levels
  cl99_chi2 <- compute_cl_chi2(min(df[,chi2_col]), parameter_num, data_point_num, .01)
  cl95_chi2 <- compute_cl_chi2(min(df[,chi2_col]), parameter_num, data_point_num, .05)    
  cl66_chi2 <- compute_cl_chi2(min(df[,chi2_col]), parameter_num, data_point_num, .33)  

  # select the rows with chi^2 smaller than our max threshold
  df99 <- df[df[,chi2_col] <= cl99_chi2, ]  
  df95 <- df[df[,chi2_col] <= cl95_chi2, ]
  df66 <- df[df[,chi2_col] <= cl66_chi2, ]  
  
  min_chi2 <- min(df99[,chi2_col])  
  
  # Set my ggplot theme here
  theme_set(basic_theme(36))
 
  # Plot the Chi^2 vs Iterations
  plot_chi2_vs_iters(df, chi2_col, plots_dir, model)

  # Write the summary for the parameter estimation analysis
  fileoutPLE <- sink(fileout_param_estim_summary)
  cat(paste("MinChi2", "AIC", "AICc", "BIC", "ParamNum", "DataPointNum", "CL66Chi2", "CL66FitsNum", "CL95Chi2", "CL95FitsNum", "CL99Chi2", "CL99FitsNum\n", sep="\t"))
  cat(paste(min_chi2, compute_aic(min_chi2, parameter_num), compute_aicc(min_chi2, parameter_num, data_point_num), compute_bic(min_chi2, parameter_num, data_point_num), parameter_num, data_point_num, cl66_chi2, nrow(df66), cl95_chi2, nrow(df95), cl99_chi2, nrow(df99), sep="\t"), append=TRUE)
  cat("\n", append=TRUE)   
  sink()

  # Plot the sampled profile likelihood estimations (PLE)
  plot_sampled_ple(df99, chi2_col, cl66_chi2, cl95_chi2, cl99_chi2, plots_dir, model, logspace, scientific_notation)
  
  # Write the table containing the parameter estimation details.
  fileoutPLE <- sink(fileout_param_estim_details)
  cat(paste("Parameter", "Value", "LeftCI66", "RightCI66", "LeftCI95", "RightCI95", "LeftCI99", "RightCI99", "Value_LeftCI66_ratio", "RightCI66_Value_ratio", "Value_LeftCI95_ratio", "RightCI95_Value_ratio", "Value_LeftCI99_ratio", "RightCI99_Value_ratio\n", sep="\t"), append=TRUE)
  for (i in seq(2,length(dfCols))) {
    # compute the confidence levels and the value for the best parameter
    ci_obj <- compute_sampled_ple_stats(df66, df95, df99, df, chi2_col, chi2_col_idx, i, 
                                        cl66_chi2, cl95_chi2, cl99_chi2, logspace)

    # write on file
    cat(paste(dfCols[i], ci_obj$par_value, ci_obj$min_ci_66, ci_obj$max_ci_66, ci_obj$min_ci_95, ci_obj$max_ci_95, 
    ci_obj$min_ci_99, ci_obj$max_ci_99, ci_obj$min_ci_66_par_value_ratio, ci_obj$max_ci_66_par_value_ratio,
    ci_obj$min_ci_95_par_value_ratio, ci_obj$max_ci_95_par_value_ratio, ci_obj$min_ci_99_par_value_ratio,
    ci_obj$max_ci_99_par_value_ratio, sep="\t"), append=TRUE)
    cat("\n", append=TRUE)    
  }
  sink()
  
  # plot parameter correlations using the 66%, 95%, or 99% confidence level data sets  
  plot_2d_cl_corr(df66, df95, df99, chi2_col, plots_dir, model,
                  plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
                  logspace, scientific_notation)
  
}



# Run model parameter estimation analysis and plot results. It analyses
# only the best fits using a percent threshold.
#
# :param model: the model name without extension
# :param filenamein: the dataset containing the parameter estimation data.
# :param plots_dir: the directory to save the generated plots
# :param best_fits_percent: the percent of best fits to analyse.
# :param logspace: true if parameters should be plotted in logspace.
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
final_fits_analysis <- function(model, filenamein, plots_dir, best_fits_percent, logspace=TRUE, scientific_notation=TRUE) {

  best_fits_percent <- as.numeric(best_fits_percent)
  if(best_fits_percent <= 0.0 || best_fits_percent > 100.0) {
    warning("best_fits_percent is not in (0, 100]. Now set to 100")
    best_fits_percent = 100
  }
  
  df = read.csv(filenamein, head=TRUE,sep="\t")
  
  if(logspace) {
    # Transform the parameter space to a log10 parameter space. 
    # The 2nd column containing the Chi^2 score is maintained 
    # as well as the 1st containing the parameter estimation name. 
    df[,c(-1,-2)] <- log10(df[,c(-1,-2)])
  }
    
  dfCols <- replace_colnames(colnames(df))
  colnames(df) <- dfCols
  
  # Calculate the number of rows to extract.
  selected_rows <- nrow(df)*best_fits_percent/100
  # sort by Chi^2 (descending) so that the low Chi^2 parameter tuples 
  # (which are the most important) are plotted in front. 
  # Then extract the tail from the data frame. 
  df <- df[order(-df[,2]),]
  df <- tail(df, selected_rows)
  
  # Set my ggplot theme here
  theme_set(basic_theme(36))
  
  plot_parameter_correlations(df, dfCols, plots_dir, paste(model, "_best_fits_", sep=""), "best fits", 2, logspace, scientific_notation)
  
}


