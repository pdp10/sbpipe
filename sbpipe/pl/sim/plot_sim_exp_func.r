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
# Object: A collection of functions
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-7 16:14:32 $


# plotCI
library(gplots)


# Compute and return the chi_square
get_chi_square <- function(ntime_points, sim_mean, exp_mean, exp_std_err, wvariance) {
  chi_square <- 0
  if(wvariance == TRUE) {
    repeats <- 4
    variance <- repeats * exp_std_err^2
  }
  # implement chi^2 = sum_{i=0}^{k} ( (O_i - E_i)^2 / E_i )
  for(i in 1:ntime_points) {
    if(wvariance == TRUE) {
      ## it also considers the variance in the data 
      if(variance[i] > 0) {
	chi_square <- chi_square + ((sim_mean[i] - exp_mean[i])^2 / variance[i])
      } else {
	# avoid divisions by 0
	chi_square <- chi_square + (sim_mean[i] - exp_mean[i])^2
      }
    } else {
      ## PEARSON CORRELATION
      if(sim_mean[i] > 0) {
        chi_square <- chi_square + ((sim_mean[i] - exp_mean[i])^2 / sim_mean[i])
      } else {
      # avoid divisions by 0
        chi_square <- chi_square + (sim_mean[i] - exp_mean[i])^2
      }
    }

  }
  return(chi_square)
}




# plot generic data + standard error
plot_err_bars <- function(xmean, std_err, max_mean_std_err, time, name, linewidth, pch, lty, add) {
    # plot simulation
    plotCI(x=xmean,
	    uiw=std_err,
	    col="black", barcol="black",
	    xlim=c(1,length(time)),
	    ylim=c(0,max_mean_std_err+max_mean_std_err/4),
	    labels=FALSE,
	    xlab="", ylab="", 
	    main="", las=1,
	    cex.main=3.5, cex.lab=3.4, cex.axis=3.4, font.axis=2, 
	    pch=pch,cex=3.4,lty=lty, lwd=linewidth,bty="n",lwd.ticks=6,
	    xaxt='n', gap=0.0, add=add)
	## set y axis
	# Set up x axis with tick marks alone
	#axis(side=2, labels=FALSE, at=c(1:length(time)), cex.axis=3.0, font.axis=2,xpd=TRUE,lwd.ticks=4)
	# Plot x axis labels at default tick marks
	#text(side=2, 1:length(time), par("usr")[3] - 1, srt=45, adj=1, labels=time, cex=3.0, font=2, xpd = TRUE)
	# Plot x axis label at line 6 (of 7)
	mtext(side=2, text=paste(name, " level (AU)", sep=""), line=7, cex=3.4, font=2) 
}


# plot means + std error of the simulated and experimental data
plot_sim_exp_error_bars <- function(sim_mean, sim_std_err, exp_mean, exp_std_err, max_mean_std_err, time, name, linewidth) {
    # plot simulation
    plot_err_bars(sim_mean, sim_std_err, max_mean_std_err, time, name, linewidth, '.', 1, FALSE)
    # plot experiment
    plot_err_bars(exp_mean, exp_std_err, max_mean_std_err, time, name, linewidth, 21, 6, TRUE)
    # SPAN: 0.25 (line is the mean), 0.90 (line approximates the mean)
    #exp_mean.loess <- loess(exp_mean ~ time, span=0.90, data.frame(x=time, y=exp_mean))
    #exp_mean.predict <- predict(exp_mean.loess, data.frame(x=time))
    #lines(spline(exp_mean.predict, method="natural", n = 10*length(exp_mean)), col="black", pch=21, lwd=linewidth, lty=2)

    # Comment the next line to remove the interpolation over experimental data
    #lines(spline(exp_mean, method="natural", n = 10*length(exp_mean)), col="black", pch=21, lwd=linewidth, lty=2)
      #lines(spline(exp_mean+exp_sderr, method="natural", n = 10*length(exp_mean)))
      #lines(spline(exp_mean-exp_sderr, method="natural", n = 10*length(exp_mean)))

    # LEGEND with Pearson and Spearman correlations
    #pearson <- cor.test(sim_mean, exp_mean, method="pearson")
    #spearman <- cor.test(sim_mean, exp_mean, method="spearman")
    # \u{00B1} is the unicode character for plus/minus
    #legend("topright", c("Simulation ","Experiments\n(mean\u{00B1}SEM, 4 repeats)",paste("Pearson correlation: ", round(pearson[[4]][[1]], digits = 4),sep=""),paste("Spearman correlation: ", round(spearman[[4]][[1]], digits = 4), sep="")), pch=c(15,5,26,26), cex=1.6, lty=c(1,3,0,0), lwd=linewidth, col=c("black","black"), bty="n")

    # LEGEND with chi-square fitting measure
    datapoints <- length(time)
    chi_square <- round( get_chi_square(datapoints, sim_mean, exp_mean, exp_std_err, TRUE), digits=4 )
    #par(font=2)
    legend("topright", legend=substitute(paste(chi^2==x, ", ", n==dp, sep=""), list(x=chi_square, dp=datapoints)), cex=4.0, col=c("black"), bty="n")    

    # BASIC LEGEND
    #legend("topright", c("Simulation ","Experiments\n(mean\u{00B1}SEM, 4 repeats)"), pch=c('.','o'), cex=3.2, lty=c(1,6), lwd=linewidth, col=c("black","black"), bty="n")
    
    return(chi_square)

}



# plot simulated data only
plot_sim_error_bars <- function(sim_mean, sim_std_err, max_mean_std_err, time, name, linewidth) {
    plot_err_bars(sim_mean, sim_std_err, max_mean_std_err, time, name, linewidth, '.', 1, FALSE)
    #legend("topright","Simulation ", pch=15, cex=2.5, lty=1, lwd=linewidth, col=c("black"), bty="n")
}



# Main function which plot the simulated and experimental data together
sim_exp_error_bars_main <- function(sim_stat, sim_column, exp_stat, exp_column, outputdir, version, lookup_table) {
    linewidth <- 8
    time <- sim_stat[,c(sim_column[1])]
    total_chi_square <- 0.0
    total_timepoints <- 0
    for(j in seq(2,length(sim_column),13)) {
	sim_mean <- sim_stat[,c(sim_column[j])]
	sim_std_err <- sim_stat[,c(sim_column[j+6])]
	name <- substr(sim_column[j],0, nchar(sim_column[j])-5)
	print(name)
	print(sim_mean)
	max_mean_std_err <- max(sim_mean+sim_std_err)
	# plot mean line with standard error together with experimental data
	png(file.path(outputdir, paste(version, "_sem_", name, ".png", sep="" )), height=600, width=800, bg="transparent") 
	# increase the margin on the right of the plot
	par(mar=c(7,9.5,4,0)+0.1)

	# add experimental curve if it exists
	exp_mean <- c()
	exp_std_err <- c()
	found = FALSE
	for(k in 1:length(lookup_table[,1])) {
	  if(name == lookup_table[k,1]) {
	    # retrieve mean and std_err from exprimental data if it matches in the lookup table
	    for(l in seq(2,length(exp_column),13)) {
	      name_exp <- substr(exp_column[l],0, nchar(exp_column[l])-5)
	      if(lookup_table[k,2] == name_exp) {
		found = TRUE
		exp_mean <- exp_stat[,c(exp_column[l])]
		exp_std_err <- exp_stat[,c(exp_column[l+6])]
		if(max_mean_std_err < max(exp_mean+exp_std_err)) { 
		    max_mean_std_err = max(exp_mean+exp_std_err) 
		}
		total_chi_square <- total_chi_square + plot_sim_exp_error_bars(sim_mean, sim_std_err, exp_mean, exp_std_err, max_mean_std_err, time, name, linewidth)
		total_timepoints <- total_timepoints + length(time) 
		break;
	      }
	    }
	    break;
	  }
	}
	if(found == FALSE) {
	  plot_sim_error_bars(sim_mean, sim_std_err, max_mean_std_err, time, name, linewidth)
	}
	# SPAN: 0.25 (line is the mean), 0.90 (line approximates the mean)
	#sim_mean.loess <- loess(sim_mean ~ time, span=0.90, data.frame(x=time, y=sim_mean))
	#sim_mean.predict <- predict(sim_mean.loess, data.frame(x=time))
	#lines(spline(sim_mean.predict, method="natural", n = 10*length(sim_mean)), col="black", pch=21, lty=1, lwd=linewidth)
	lines(spline(sim_mean, method="natural", n = 10*length(sim_mean)), col="black", pch=21, lwd=linewidth, lty=1)
	#lines(spline(sim_mean+sim_sderr, method="natural", n = 10*length(sim_mean)))
	#lines(spline(sim_mean-sim_sderr, method="natural", n = 10*length(sim_mean)))

	## set x axis
	# Set up x axis with tick marks alone
	axis(side=1, labels=FALSE, at=c(1:length(time)), cex.axis=3.4, font.axis=2,lwd.ticks=6)
	# Plot x axis labels at default tick marks
	text(side=1, 1:length(time), par("usr")[3]-0.0, srt=30, adj=c(1.1,1.2), labels=time, cex=3.4, font=2, xpd=TRUE)
	# Plot x axis label at line 6 (of 7)
	mtext(side=1, text="Time (min)", line=5.5, cex=3.4, font=2) 


	
	#axis(side=1, labels=time, at=c(1:length(time)), cex.axis=3.0, font.axis=2,xpd=TRUE,lwd.ticks=4, las=2)

	box(bty="l", lwd=8, lty=1)
	dev.off()
    }
					    # statistical table (to export)
    results <- data.frame(tot_chisquare=total_chi_square, tot_timepoints=total_timepoints)
    #results[1,1] <- total_chi_square
    #results[1,2] <- total_timepoints
    
    ## write total_chi_square and total_timepoints
    return(results)
}




