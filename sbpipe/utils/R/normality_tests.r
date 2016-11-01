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
# Object: Collect some statistics and plots for the following datasets.
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-04-29 13:45:32 $



library(xlsx)
library(moments)
library(nortest)
# qqplot
library(qualityTools)
# probplot
#library(e1071)
# plotCI
library(gplots)
#qqplot
require(graphics)


# Shapiro test
my_shapiro_test = function(x){
  if(length(unique(x)) > 1) {
    shapiro.test(x)
  } else {
    cat('Skip Shapiro test: all \'x\' values are identical\n')
  }
}

# Kolmogorov-Smirnov test
my_ks_test = function(x){
  if(length(x)>0) {
    ks.test(x,"pnorm",mean(x),sqrt(var(x)))
  } else {
    cat('Error in ks.test(x, "pnorm", mean(x), sqrt(var(x))) : not enough x data \n')
  }  
}

# Anderson-Darling test
my_ad_test = function(x){
  if(length(x)>7) {
    ad.test(x)
  } else {
    cat('Skip Anderson-Darling test: sample size must be greater than 7\n')
  }
}

# Plot QQs
qq_plots = function(x, m, ds){
  column <- m[,x]
  if(length(unique(column)) > 1) {
    col=gsub("X", "", x)
    png(paste('stats__', ds, '__qqplot_norm_t', col, '.png', sep=""))
    qqnorm(column, main=paste("QQ plot (norm) for t",col, sep=""))
    qqline(column)
    dev.off()
    
    png(paste('stats__', ds, '__qqplot_lognorm_t', col, '.png', sep=""))
    colWOzeros <- column
    colWOzeros[colWOzeros<=0] <- 0.1
    qqnorm(log(colWOzeros), main=paste("QQ plot (log-norm) for t",col, sep=""))
    qqline(log(colWOzeros))
    dev.off()
  
    #png(paste('stats__', ds, '__probplot_t', col, '.png', sep=""))
    # p-plot: you should observe a good fit of the straight line
    #probplot(column, qdist=qnorm)  
    #dev.off()
    
    #png(paste('stats__', ds, '__normal_density_t', x, '.png', sep=""))    
    # fitted normal density
    #f.den <- function(t) dnorm(t,mean(column),sqrt(var(column)))
    #curve(f.den,xlim=c(6,14))
    #hist(column,prob=T,add=T)
    #dev.off()
  } else {
    cat('Skip QQ-plots: all \'x\' values are identical\n')
  }
}

# Geometric mean - THIS IS CORRECT according to stats.stackexchange.com
gm_mean = function(x, na.rm=TRUE){
  exp(mean(log(x), na.rm=na.rm))
}

# Geometric sd - THIS IS CORRECT according to stats.stackexchange.com
gm_sd = function(x, na.rm=TRUE){
  exp(sd(log(x), na.rm=na.rm))
}



# Sample time courses (samples.num) from the original data. The xlsx file is organised so that each sheet is 
# a readout. In each sheet, the columns are the time points whereas the rows are the repeats. The first raw is 
# the header and contains the time points.
normality_tests <- function(xlsxname.file, xlsxname.sheets) {

  for (ds in xlsxname.sheets){
      cat(paste('DATA SET:', ds, '\n'))
      cat('#######################\n\n')  
  
      # read in the worksheet named mysheet
      mydata <- read.xlsx(xlsxname.file, sheetName=ds)
      xlabels <- gsub("X", "", colnames(mydata))
      
      print(xlabels)
      
      cat('Summary of statistics:\n')
      cat('----------------------\n')      
      print(summary(mydata))
      png(paste('stats__', ds, '__boxplot.png', sep=""))
      boxplot(mydata, xlab='Time [days]', ylab='Level [a.u.]', names=xlabels, main=paste(ds))
      dev.off()

      
      cat('\nSkewness and kurtosis, they should be around (0,3)\n')
      cat('--------------------------------------------------\n')           
      print(sapply(as.data.frame(mydata), skewness, na.rm=TRUE))
      print(sapply(as.data.frame(mydata), kurtosis, na.rm=TRUE))

      
      cat('\nNormality tests\n')
      cat('---------------\n')       
      # Shapiro-Wilks test
      print(sapply(as.data.frame(mydata), my_shapiro_test))

      # Kolmogorov-Smirnov test
      print(sapply(as.data.frame(mydata), my_ks_test))

      # Anderson-Darling test
      print(sapply(as.data.frame(mydata), my_ad_test))

      
      # qq-plot: you should observe a good fit of the straight line
      sapply(colnames(mydata), qq_plots, as.data.frame(mydata), ds)
      
      
      
      # compute arithmetic mean and arithmetic standard deviation
      amean <- sapply(as.data.frame(mydata), mean, na.rm=TRUE)
      asd <- sapply(as.data.frame(mydata), sd, na.rm=TRUE)
      cat('\nArithmetic mean and standard deviation:\n')
      cat('---------------------------------------\n')     
      print(amean)
      print(asd) 
      # normalise am and asd
      ameanT0 <- amean[1]
      #print(ameanT0)  
      ameanNormT0 <- amean/ameanT0
      asdNormT0 <- asd/ameanT0
      cat('\nnormalised at T0:\n')
      cat('-----------------\n')      
      print(ameanNormT0)      
      print(asdNormT0)
      png(paste('stats__', ds, '__mean_sd__arith.png', sep=""))      
      plotCI(x=ameanNormT0,
	    uiw=asdNormT0,
	    pch=21,
	    gap=0.0,
	    xaxt="n",
	    xlab="Time [days]", 
	    ylab="Level [a.u.]",
	    main=paste("Arithm. Mean + SD for ", ds)
	    )
      axis(side=1, at=1:length(xlabels), labels=xlabels)
      dev.off()
      
      
      # compute geometric mean and geometric standard deviation
      mydataWOzeros <- mydata
      mydataWOzeros[mydataWOzeros<=0] <- 0.1
      
      #print(mydata)
      #print(mydataWOzeros)
      ## REMOVE
      #print(as.data.frame(mydataWOzeros))
      #print(as.data.frame(mydataWOzeros[mydataWOzeros>0]))   
      
      geomean <- sapply(as.data.frame(mydataWOzeros), gm_mean)
      geosd <- sapply(as.data.frame(mydataWOzeros), gm_sd)
      cat('\nGeometric mean and standard deviation:\n')
      cat('--------------------------------------\n')      
      print(geomean)
      print(geosd)
      # normalise gm and gsd
      geomeanT0 <- geomean[1]
      #print(geomeanT0)  
      geomeanNormT0 <- geomean/geomeanT0
      geosdNormT0 <- geosd/geomeanT0
      cat('\nnormalised at T0:\n')
      cat('-----------------\n')
      print(geomeanNormT0)      
      print(geosdNormT0)     
      png(paste('stats__', ds, '__mean_sd__geom.png', sep=""))      
      plotCI(x=geomeanNormT0,
	    uiw=geosdNormT0,
	    pch=21,
	    gap=0.0,
	    xaxt="n",
	    xlab="Time [days]", 
	    ylab="Level [a.u.]",
	    main=paste("Geom. Mean + SD for ", ds)
	    )
      axis(side=1, at=1:length(xlabels), labels=xlabels)
      dev.off()  

      cat('\n\n\n')   
  }
}





