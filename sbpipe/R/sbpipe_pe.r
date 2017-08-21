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


# retrieve SBpipe folder containing R scripts
args <- commandArgs(trailingOnly = FALSE)
SBPIPE_R <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))
source(file.path(SBPIPE_R, 'sbpipe_plots.r'))
source(file.path(SBPIPE_R, 'sbpipe_ggplot2_themes.r'))



# Compute the fratio threshold for the confidence level.
#
# :param m: number of model parameters
# :param n: number of data points
# :param p: significance level
compute_fratio_threshold <- function(m, n, p=0.05) {
  if(n-m < 1) {
    warning("`data_point_num` is less than the number of estimated parameters. Skipping thresholds.")
    0
  } else {
    1 + (m/(n-m)) * qf(1.0-p, df1=m, df2=n-m)
  }
}



# Return the left value confidence interval.
#
# :param cut_dataset: a subset of the full dataset (e.g. the best 66%, the best 95%)
# :param full_dataset: the full dataset
# :param objval_col_idx: the index for the objective function column in the dataset
# :param param_col_idx: the index for the parameter column in the dataset
# :param objval_conf_level: the objective function confidence level
leftCI <- function(cut_dataset, full_dataset, objval_col_idx, param_col_idx, objval_conf_level) {
  # retrieve the minimum parameter value for cut_dataset
  min_ci <- min(cut_dataset[,param_col_idx])
  # retrieve the objective function values of the parameters with value smaller than the minimum value retrieved
  # from the cut_dataset, within the full dataset.
  # ...[min95, )  (we are retrieving those ...)
  lt_min_objvals <- full_dataset[full_dataset[,param_col_idx] < min_ci, objval_col_idx]
  if(length(lt_min_objvals) == 0 || min(lt_min_objvals) <= objval_conf_level) {
    min_ci <- "-inf"
  }
  min_ci
}



# Return the right value confidence interval.
#
# :param cut_dataset: a subset of the full dataset (e.g. the best 66%, the best 95%)
# :param full_dataset: the full dataset
# :param objval_col_idx: the index for the objective function column in the dataset
# :param param_col_idx: the index for the parameter column in the dataset
# :param objval_conf_level: the objective function confidence level
rightCI <- function(cut_dataset, full_dataset, objval_col_idx, param_col_idx, objval_conf_level) {
  # retrieve the minimum parameter value for cut_dataset
  max_ci <- max(cut_dataset[,param_col_idx])
  # retrieve the objective function of the parameters with value greater than the maximum value retrieved from
  # the cut_dataset, within the full dataset.
  # (, max95]...  (we are retrieving those ...)
  gt_max_objvals <- full_dataset[full_dataset[,param_col_idx] > max_ci, objval_col_idx]
  if(length(gt_max_objvals) == 0 || min(gt_max_objvals) <= objval_conf_level) {
    max_ci <- "+inf"
  }
  max_ci
}




# Rename data frame columns. `ObjectiveValue` is renamed as `ObjVal`. Substrings `Values.` and `..InitialValue` are
# removed.
#
# :param dfCols: The columns of a data frame.
replace_colnames <- function(dfCols) {
  dfCols <- gsub("ObjectiveValue", "ObjVal", dfCols)
  # global variables
  dfCols <- gsub("Values.", "", dfCols)
  dfCols <- gsub("..InitialValue", "", dfCols)
  # compartments
  dfCols <- gsub("Compartments.", "", dfCols)
  dfCols <- gsub("..InitialVolume", "", dfCols)
  # species
  dfCols <- gsub("X.", "", dfCols)
  dfCols <- gsub("._0", "", dfCols)
  dfCols <- gsub(".InitialParticleNumber", "", dfCols)
}



# Plot parameter correlations.
#
# :param df: the data frame
# :param dfCols: the columns of the data frame. Each column is a parameter. Only parameters to the left of objval_col_idx are plotted.
# :param plots_dir: the directory for storing the plots
# :param plot_filename_prefix: the prefix for the plot filename
# :param title: the plot title (default: "")
# :param objval_col_idx: the index of the column containing the objective value (default: 1)
# :param logspace: true if the parameters should be plotted in logspace (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
plot_parameter_correlations <- function(df, dfCols, plots_dir, plot_filename_prefix, title="", objval_col_idx=1,
                                        logspace=TRUE, scientific_notation=TRUE) {
      fileout <- ""
      for (i in seq(objval_col_idx+1,length(dfCols))) {
        print(paste('sampled param corr (', title, ') for ', dfCols[i], sep=''))
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
            g <- scatterplot_w_colour(df, g, colnames(df)[i], colnames(df)[j], colnames(df)[objval_col_idx]) +
                 ggtitle(title) +
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


# Plot the Objective values vs Iterations
#
# :param objval_array: the array of objective function values.
# :param plots_dir: the directory to save the generated plots
# :param model: the model name
plot_objval_vs_iters <- function(objval_array, plots_dir, model) {
    print('plotting objective value vs iteration')
    # save the objective value vs iteration
    g <- plot_fits(objval_array, ggplot())
    ggsave(file.path(plots_dir, paste(model, "_objval_vs_iter.png", sep="")), dpi=300, width=8, height=6)
}


# Plot the sampled profile likelihood estimations (PLE)
#
# :param df99: the 99% confidence level data frame
# :param objval_col: the objective value column name
# :param cl66_objval: the 66% confidence level objective value
# :param cl95_objval: the 95% confidence level objective value
# :param cl99_objval: the 99% confidence level objective value
# :param plots_dir: the directory to save the generated plots
# :param model: the model name
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
plot_sampled_ple <- function(df99, objval_col, cl66_objval, cl95_objval, cl99_objval, plots_dir, model,
                            logspace=TRUE, scientific_notation=TRUE) {
    dfCols <- colnames(df99)
    for (i in seq(2,length(dfCols))) {
        print(paste('sampled PLE for', dfCols[i]))
        # extract statistics
        fileout <- file.path(plots_dir, paste(model, "_approx_ple_", dfCols[i], ".png", sep=""))
        g <- scatterplot_ple(df99, ggplot(), dfCols[i], objval_col, cl66_objval, cl95_objval, cl99_objval) +
            theme(legend.key.height = unit(0.5, "in"))
#       g <- scatterplot_ple(df95, ggplot(), dfCols[i], objval_col, cl66_objval, cl95_objval) +
#            theme(legend.key.height = unit(0.5, "in"))
        if(logspace) {
            g <- g + xlab(paste("log10(",dfCols[i],")",sep=""))
        }
        if(scientific_notation) {
            g <- g + scale_x_continuous(labels=scientific) + scale_y_continuous(labels=scientific)
        }
        g <- g + ggtitle("PLE (sampled)")
        ggsave(fileout, dpi=300, width=8, height=6)

        # Add density information (removed as it was not showing much more..)
        #g <- g + stat_density2d(color="green")
        #fileout = gsub('.png', '_density.png', fileout)
        #ggsave(fileout, dpi=300, width=8, height=6)
    }
}


# Compute the confidence level based on the minimum objective value.
#
# :param min_objval: the minimum objective value
# :param params: the number of parameters
# :param data_points: the number of data points
# :param level: the confidence level threshold (e.g. 0.1, 0.5)
compute_cl_objval <- function(min_objval, params, data_points, level=0.5) {
    min_objval * compute_fratio_threshold(params, data_points, level)
}


# Plot parameter correlations using the 66%, 95%, or 99% confidence level data sets
#
# :param df66: the data frame filtered at 66%
# :param df95: the data frame filtered at 95%
# :param df99: the data frame filtered at 95%
# :param objval_col: the objective value column name
# :param dfCols: the column names of the dataset
# :param plots_dir: the directory to save the generated plots
# :param model: the model name
# :param plot_2d_66cl_corr: true if the 2D parameter correlation plots for 66% confidence intervals should be plotted. This is time consuming. (default: FALSE)
# :param plot_2d_95cl_corr: true if the 2D parameter correlation plots for 95% confidence intervals should be plotted. This is time consuming. (default: FALSE)
# :param plot_2d_99cl_corr: true if the 2D parameter correlation plots for 99% confidence intervals should be plotted. This is time consuming. (default: FALSE)
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
plot_2d_cl_corr <- function(df66, df95, df99, objval_col, dfCols, plots_dir, model,
                            plot_2d_66cl_corr=FALSE, plot_2d_95cl_corr=FALSE, plot_2d_99cl_corr=FALSE,
                            logspace=TRUE, scientific_notation=TRUE) {
  if(plot_2d_66cl_corr) {
    plot_parameter_correlations(df66, dfCols, plots_dir, paste(model, "_cl66_fits_", sep=""),
        expression("obj val"<="CL66%"), which(dfCols==objval_col), logspace, scientific_notation)
  }
  if(plot_2d_95cl_corr) {
    plot_parameter_correlations(df95, dfCols, plots_dir, paste(model, "_cl95_fits_", sep=""),
        expression("obj val"<="CL95%"), which(dfCols==objval_col), logspace, scientific_notation)
  }
  if(plot_2d_99cl_corr) {
    plot_parameter_correlations(df99, dfCols, plots_dir, paste(model, "_cl99_fits_", sep=""),
        expression("obj val"<="CL99%"), which(dfCols==objval_col), logspace, scientific_notation)
  }
  if(nrow(df66) == nrow(df95) && nrow(df95) == nrow(df99)) {
    plot_parameter_correlations(df99, dfCols, plots_dir, paste(model, "_all_fits_", sep=""),
        expression("all fits"), which(dfCols==objval_col), logspace, scientific_notation)
  }
}



# Compute the table for the sampled PLE statistics.
#
# :param df66: the data frame filtered at 66%
# :param df95: the data frame filtered at 95%
# :param df99: the data frame filtered at 95%
# :param df: the complete data frame
# :param objval_col: the objective value column name
# :param objval_col_idx: the objective value column index
# :param param_col_idx: the param column index
# :param cl66_objval: the 66% confidence level objective value
# :param cl95_objval: the 95% confidence level objective value
# :param cl99_objval: the 99% confidence level objective value
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
compute_sampled_ple_stats <- function(df66, df95, df99, df, objval_col, objval_col_idx, param_col_idx,
                                        cl66_objval, cl95_objval, cl99_objval, logspace=TRUE) {

    min_objval <- min(df99[,objval_col])
    par_value <- min(df99[df99[,objval_col] <= min_objval, param_col_idx])

    min_ci_66 <- leftCI(df66, df95, objval_col_idx, param_col_idx, cl66_objval)
    max_ci_66 <- rightCI(df66, df95, objval_col_idx, param_col_idx, cl66_objval)
    min_ci_95 <- "-inf"
    max_ci_95 <- "+inf"
    min_ci_99 <- "-inf"
    max_ci_99 <- "+inf"
    if(is.numeric(min_ci_66)) { min_ci_95 <- leftCI(df95, df99, objval_col_idx, param_col_idx, cl95_objval) }
    if(is.numeric(max_ci_66)) { max_ci_95 <- rightCI(df95, df99, objval_col_idx, param_col_idx, cl95_objval) }
    if(is.numeric(min_ci_95)) { min_ci_99 <- leftCI(df99, df, objval_col_idx, param_col_idx, cl99_objval) }
    if(is.numeric(max_ci_95)) { max_ci_99 <- rightCI(df99, df, objval_col_idx, param_col_idx, cl99_objval) }

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
# :param df: the dataset containing all the parameter estimation fits.
# :param plots_dir: the directory to save the generated plots
# :param data_point_num: the number of data points used for parameterise the model
# :param fileout_param_estim_details: the name of the file containing the detailed statistics for the estimated parameters
# :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation
# :param plot_2d_66cl_corr: true if the 2D parameter correlation plots for 66% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param plot_2d_95cl_corr: true if the 2D parameter correlation plots for 95% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param plot_2d_99cl_corr: true if the 2D parameter correlation plots for 99% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
all_fits_analysis <- function(model, df, plots_dir, data_point_num,
                              fileout_param_estim_details, fileout_param_estim_summary,
                              plot_2d_66cl_corr=FALSE, plot_2d_95cl_corr=FALSE, plot_2d_99cl_corr=FALSE,
                              logspace=TRUE, scientific_notation=TRUE) {

  data_point_num <- as.numeric(data_point_num)
  if(data_point_num < 0.0) {
    warning("`data_point_num` must be >= 0. To visualise thresholds, `data_point_num` must be greater than the number of estimated parameters.")
    stop()
  }

  dfCols <- replace_colnames(colnames(df))
  colnames(df) <- dfCols
  objval_col_idx <- 1
  objval_col <- dfCols[objval_col_idx]

  if(logspace) {
    # Transform the parameter space to a log10 parameter space.
    # The column for the objective value score is maintained instead.
    df[,-objval_col_idx] <- log10(df[,-objval_col_idx])
  }

  parameter_num = length(colnames(df)) - 1
  # compute the confidence levels
  cl99_objval <- compute_cl_objval(min(df[,objval_col]), parameter_num, data_point_num, .01)
  cl95_objval <- compute_cl_objval(min(df[,objval_col]), parameter_num, data_point_num, .05)
  cl66_objval <- compute_cl_objval(min(df[,objval_col]), parameter_num, data_point_num, .33)

  # select the rows with objective value smaller than our max threshold
  if(cl99_objval > 0) { df99 <- df[df[,objval_col] <= cl99_objval, ] } else { df99 <- df }
  if(cl95_objval > 0) { df95 <- df[df[,objval_col] <= cl95_objval, ] } else { df95 <- df }
  if(cl66_objval > 0) { df66 <- df[df[,objval_col] <= cl66_objval, ] } else { df66 <- df }

  min_objval <- min(df99[,objval_col])

  # Set my ggplot theme here
  theme_set(basic_theme(36))

  # Plot the objective value vs Iterations
  plot_objval_vs_iters(df[,objval_col], plots_dir, model)

  # Write the summary for the parameter estimation analysis
  fileoutPLE <- sink(fileout_param_estim_summary)
  cat(paste("MinObjVal", "AIC", "AICc", "BIC", "ParamNum", "DataPointNum", "CL66ObjVal", "CL66FitsNum", "CL95ObjVal", "CL95FitsNum", "CL99ObjVal", "CL99FitsNum\n", sep="\t"))
  cat(paste(min_objval, compute_aic(min_objval, parameter_num), compute_aicc(min_objval, parameter_num, data_point_num), compute_bic(min_objval, parameter_num, data_point_num), parameter_num, data_point_num, cl66_objval, nrow(df66), cl95_objval, nrow(df95), cl99_objval, nrow(df99), sep="\t"), append=TRUE)
  cat("\n", append=TRUE)
  sink()

  # Plot the sampled profile likelihood estimations (PLE)
  plot_sampled_ple(df99, objval_col, cl66_objval, cl95_objval, cl99_objval, plots_dir, model, logspace, scientific_notation)

  # Write the table containing the parameter estimation details.
  fileoutPLE <- sink(fileout_param_estim_details)
  cat(paste("Parameter", "Value", "LeftCI66", "RightCI66", "LeftCI95", "RightCI95", "LeftCI99", "RightCI99", "Value_LeftCI66_ratio", "RightCI66_Value_ratio", "Value_LeftCI95_ratio", "RightCI95_Value_ratio", "Value_LeftCI99_ratio", "RightCI99_Value_ratio\n", sep="\t"), append=TRUE)
  for (i in seq(2,length(dfCols))) {
    # compute the confidence levels and the value for the best parameter
    ci_obj <- compute_sampled_ple_stats(df66, df95, df99, df, objval_col, objval_col_idx, i,
                                        cl66_objval, cl95_objval, cl99_objval, logspace)

    # write on file
    cat(paste(dfCols[i], ci_obj$par_value, ci_obj$min_ci_66, ci_obj$max_ci_66, ci_obj$min_ci_95, ci_obj$max_ci_95,
    ci_obj$min_ci_99, ci_obj$max_ci_99, ci_obj$min_ci_66_par_value_ratio, ci_obj$max_ci_66_par_value_ratio,
    ci_obj$min_ci_95_par_value_ratio, ci_obj$max_ci_95_par_value_ratio, ci_obj$min_ci_99_par_value_ratio,
    ci_obj$max_ci_99_par_value_ratio, sep="\t"), append=TRUE)
    cat("\n", append=TRUE)
  }
  sink()

  # plot parameter correlations using the 66%, 95%, or 99% confidence level data sets
  dfCols <- colnames(df99)
  if(cl99_objval > 0) {
      plot_2d_cl_corr(df66[order(-df66[,objval_col]),],
                      df95[order(-df95[,objval_col]),],
                      df99[order(-df99[,objval_col]),],
                      objval_col,
                      dfCols, plots_dir, model,
                      plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
                      logspace, scientific_notation)
   } else {
      plot_2d_cl_corr(df66[order(-df99[,objval_col]),],
                      df95[order(-df99[,objval_col]),],
                      df99[order(-df99[,objval_col]),],
                      objval_col,
                      dfCols, plots_dir, model,
                      FALSE, FALSE, FALSE,
                      logspace, scientific_notation)
   }

}



# Run model parameter estimation analysis and plot results. It analyses
# only the best fits using a percent threshold.
#
# :param model: the model name without extension
# :param df: the dataset containing the best parameter estimation fits.
# :param plots_dir: the directory to save the generated plots
# :param best_fits_percent: the percent of best fits to analyse.
# :param logspace: true if parameters should be plotted in logspace.
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
final_fits_analysis <- function(model, df, plots_dir, best_fits_percent, logspace=TRUE, scientific_notation=TRUE) {

  best_fits_percent <- as.numeric(best_fits_percent)
  if(best_fits_percent <= 0.0 || best_fits_percent > 100.0) {
    warning("best_fits_percent is not in (0, 100]. Now set to 100")
    best_fits_percent = 100
  }

  if(logspace) {
    # Transform the parameter space to a log10 parameter space.
    # The 2nd column containing the objective value is maintained
    # as well as the 1st containing the parameter estimation name.
    df[,c(-1,-2)] <- log10(df[,c(-1,-2)])
  }

  dfCols <- replace_colnames(colnames(df))
  colnames(df) <- dfCols

  # Calculate the number of rows to extract.
  selected_rows <- nrow(df)*best_fits_percent/100
  # sort by objective value (descending) so that the low objective value parameter tuples
  # (which are the most important) are plotted in front.
  # Then extract the tail from the data frame.
  df <- df[order(-df[,2]),]
  df <- tail(df, selected_rows)

  # Set my ggplot theme here
  theme_set(basic_theme(36))

  plot_parameter_correlations(df, dfCols, plots_dir, paste(model, "_best_fits_", sep=""),
    "best obj val", 2, logspace, scientific_notation)

}



# Run model parameter estimation analysis and plot results.
#
# :param model: the model name without extension
# :param finalfits_filenamein: the dataset containing the best parameter fits
# :param allfits_filenamein: the dataset containing all the parameter fits
# :param plots_dir: the directory to save the generated plots
# :param data_point_num: the number of data points used for parameterise the model
# :param fileout_param_estim_details: the name of the file containing the detailed statistics for the estimated parameters
# :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation
# :param best_fits_percent: the percent of best fits to analyse.
# :param plot_2d_66cl_corr: true if the 2D parameter correlation plots for 66% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param plot_2d_95cl_corr: true if the 2D parameter correlation plots for 95% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param plot_2d_99cl_corr: true if the 2D parameter correlation plots for 99% confidence intervals should be plotted. This can be time consuming. (default: FALSE)
# :param logspace: true if parameters should be plotted in logspace. (default: TRUE)
# :param scientific_notation: true if the axis labels should be plotted in scientific notation (default: TRUE)
fits_analysis <- function(model, finalfits_filenamein, allfits_filenamein, plots_dir, data_point_num,
                          fileout_param_estim_details, fileout_param_estim_summary, best_fits_percent,
                          plot_2d_66cl_corr=FALSE, plot_2d_95cl_corr=FALSE, plot_2d_99cl_corr=FALSE,
                          logspace=TRUE, scientific_notation=TRUE) {
    finalfits = TRUE
    dim_final_fits = dim(read.table(finalfits_filenamein, sep="\t"))[1]
    dim_all_fits = dim(read.table(allfits_filenamein, header=TRUE, sep="\t"))[1]

    if(dim_final_fits-1 <= 1) {
      warning('Best fits analysis requires at least two parameter estimations. Skip.')
      finalfits = FALSE
    }
    if(dim_all_fits-1 <= 0) {
      warning('All fits analysis requires at least one parameter set. Cannot continue.')
      stop()
    }

    df_all_fits = read.table(allfits_filenamein, header=TRUE, dec=".", sep="\t")

    # non-positive entries test
    # If so, logspace will be set to FALSE, otherwise SBpipe will fail due to NaN values.
    # This is set once for all
    nonpos_entries <- sum(df_all_fits <= 0)
    if(nonpos_entries > 0) {
      warning('Non-positive values found for one or more parameters. `logspace` option set to FALSE')
      logspace = FALSE
    }

    if(finalfits) {
        df_final_fits = read.table(finalfits_filenamein, header=TRUE, dec=".", sep="\t")
        final_fits_analysis(model, df_final_fits, plots_dir, best_fits_percent, logspace, scientific_notation)
    }

    all_fits_analysis(model, df_all_fits, plots_dir, data_point_num, fileout_param_estim_details,
                        fileout_param_estim_summary, plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
                        logspace, scientific_notation)
}

