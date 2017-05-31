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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-05-17 10:43:12 $


# NOTE: xlsx depends on rJava. IF rJava does not work, follow the procedure shown here: 
# https://orajavasolutions.wordpress.com/2014/06/03/installing-and-loading-xlsx-package-in-r-with-ubuntu/
library(xlsx)




# Generate time courses by extracting original data (using sample()).
# Sample time courses (samples.num) from the original data. The xlsx file is organised so that each sheet is 
# a readout. In each sheet, the columns are the time points whereas the rows are the repeats. The first raw is 
# the header and contains the time points. This works for both CopasiUI and CopasiSE.
#
# :param timecourse: a vector of time courses
# :param xlsxname.file: the xlsx file name
# :param xlsxname.sheets: the sheet names in the xlsx file
# :param file.samples: the output file containing the generated samples
# :param samples.num: the number of samples to generate
sample_from_data <- function(timecourse, xlsxname.file, xlsxname.sheets, file.samples, samples.num) {

  samples.rows <- length(timecourse)           
  samples.cols <- length(xlsxname.sheets) + 1  # add `Time` col
  mat3d <- array(NA, dim=c(samples.rows, samples.cols, samples.num))
  #print(mat3d)

  # add column names and update the Time column.
  columnNames <- c('Time', xlsxname.sheets)  
  #colnames(mat3d) <- c('Time', xlsxname.sheets)
  for(i in 1:samples.num) {
    mat3d[,1,i] <- timecourse
  }
  #print(mat3d)
  
  # The worksheet information is reorganised so that 
  # sheet.name (readout) -> matrix.cols; sheet.cols (timepoints) -> matrix.row (time points). 
  # The third dimension of the matrix contains the samples.
  for (i in 1:length(xlsxname.sheets)) {

    # read a sheet in the worksheet
    readout.data <- read.xlsx(xlsxname.file, sheetName=xlsxname.sheets[i])
    #print(readout.data)
    readout.tps <- gsub("X", "", colnames(readout.data))
    #print(readout.tps)
     
    # extract columns from the readout. This corresponds to the repeats for of the time points.
    for(j in 1:length(readout.data)) {

      readout.tpdata <- readout.data[,j][!is.na(readout.data[,j])]
      #print(readout.tpdata)

      # extract the index for the corresponding time point (readout.tps[j]) in timecourse
      tp.idx <- match(readout.tps[j], timecourse)
      
      # generate samples for the available time points and store the whole vector directly.
      mat3d[tp.idx,1+i,] <- sample(readout.tpdata, samples.num, replace=TRUE)  
    } 
  }
  #print(mat3d)
  
  # delete a previous file if this exists
  if (file.exists(file.samples)) {
    file.remove(file.samples)
  }
  # save data on file
  write.table(as.data.frame.list(columnNames), file=file.samples, append=FALSE, quote=FALSE, sep=",",
            na="", row.names=FALSE, col.names=FALSE)   
  for(k in 1:samples.num) {
    write.table(mat3d[, , k], file=file.samples, append=TRUE, quote=FALSE, sep=",",
            na="", row.names=FALSE, col.names=FALSE)
  }
  
}


# Generate time courses by sampling from data distribution.
# For geometric mean and standard deviation, read this: 
# http://stats.stackexchange.com/questions/114087/summarizing-a-lognormal-distribution-with-geometric-mean-and-standard-deviation
#
# :param datafile: a file containing readouts specified as time,mean,sd,mean,sd, ...
# :param samplefile: the output file containing the generated samples.
# :param samples.num: the number of samples
# :param lognormal: TRUE if log normal distribution is used. If this is used data must be geometric mean and sd.
# :param resampling: TRUE if resampling is desired when a NA or negative value is computed.
sample_from_distribution <- function(datafile, samplefile, samples.num, lognormal, resampling) {
    samples.num <- as.numeric(samples.num)
    
    data <- read.table(datafile,header=TRUE,na.strings="NaN",dec=".",sep=",")

    column.name <- names(data)
    column.number <- length(column.name)
    column.export <- c("time")
    
    samples.rows <- length(data[,1])
    samples.cols <- ((column.number-1)/2)+1
    
    data.length <- samples.rows * samples.cols * samples.num
    
    mat3d <- array(NA, dim=c(samples.rows, samples.cols, samples.num))
    #print(mat3d)
    
    time <- data[,1]
    d <- 2
    s.i <- 1
    
    # parse the columns from the input files (time,mean,sd,mean,sd, ..)
    while(d <= column.number) {
      print(column.name[d])
      column.export <- c(column.export, column.name[d])
      # condense mean + sd into one column (a sample)
      s.i <- s.i + 1
      
      mat3d[,1,] <- time
      for(s.j in 1:samples.rows) { 

        if(lognormal == "true") {
    
            # Use of geometric mean, sd and Log-Normal distribution.
            tp.mean <- data[s.j, d]
            tp.sd <- data[s.j, d+1]
            sample <- rlnorm(samples.num, meanlog=tp.mean, sdlog=tp.sd)

            if(resampling == "false") {
                # DISCARD IF NA or O
                for(s.k in 1:samples.num) {
                logSample = log(sample[s.k])
                ##logSample = sample[s.k]
                if(!is.na(logSample) && logSample > 0) {
                    mat3d[s.j, s.i, s.k] = logSample
                }
                }
            } else {
                # RE-SAMPLE IF NA or O
                for(s.k in 1:samples.num) { 
                while(!is.na(log(sample[s.k])) && log(sample[s.k]) <= 0) {
                    sample[s.k] <- rlnorm(1, meanlog=tp.mean, sdlog=tp.sd)
                }      
                # copy the data
                mat3d[s.j, s.i, s.k] = log(sample[s.k])
                }
            }
        
        
        } else {
            # Use of arithmetic mean, sd and Normal distribution.
            tp.mean <- data[s.j, d]
            tp.sd <- data[s.j, d+1]
            sample <- rnorm(samples.num, mean=tp.mean, sd=tp.sd)

            if(resampling == "false") {
                # DISCARD IF NA or O
                for(s.k in 1:samples.num) {
                if(!is.na(sample[s.k]) && sample[s.k] > 0) {
                    mat3d[s.j, s.i, s.k] = sample[s.k]
                }
                }  
            } else {
                # RE-SAMPLE IF NA or O
                for(s.k in 1:samples.num) { 
                while(!is.na(sample[s.k]) && sample[s.k] <= 0) {
                    sample[s.k] <- rnorm(1, tp.mean, tp.sd) 
                }
                # copy the data
                mat3d[s.j, s.i, s.k] = sample[s.k]
                }
            }
        }

      }
      d <- d+2     
    }
    
    #print(mat3d)
    print(column.export)

    # delete a previous file if this exists
    if (file.exists(samplefile)) file.remove(samplefile)
    
    # save data on file
    for(k in 1:samples.num) {
      if(samples.rows == 1) {
        # take the transpose to print it as a row and not as a column.
        write.table(t(mat3d[, , k]), file = samplefile, append = TRUE, quote = FALSE, sep = ",",
                    na = "", row.names = FALSE, col.names = c(column.export))
      } else {
        write.table(mat3d[, , k], file = samplefile, append = TRUE, quote = FALSE, sep = ",",
                    na = "", row.names = FALSE, col.names = c(column.export))      
      }
      # Copasi throws an Error if an empty line is added between repeats. 
      # Weird as the documentation says to add it!            
      # write.table(array(NA, dim=c(1, samples.cols)), file = samplefile, append = TRUE, quote = FALSE, sep = ",",
      #             na = "", row.names = FALSE, col.names = FALSE)            
    }
    
}

