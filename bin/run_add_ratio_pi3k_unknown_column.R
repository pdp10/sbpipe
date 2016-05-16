# License (GPLv3):
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Add column Ratio and Knock down after Time_Point column and before the columns of the species
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $


main <- function(args) {
    # the filename
    filename <- args[1]
    # the output filename
    filename_out <- args[2]
    timecourses <- read.table(filename, header=TRUE, na.strings="NA", dec=".", sep="\t")
    columns <- names(timecourses)
    # create column ratio (category)
    ratio <- c("100:0","90:10","80:20","70:30","60:40","50:50","40:60","30:70","20:80","10:90","0:100")
    ratio <- rev(ratio)
    ratio <- rep(ratio, each=11)
    # create column knockdown (category)
    kd <- seq(100, 0, by=-10)
    kd <- rep(kd, times=11)
    df <- data.frame(timecourses$Time, ratio, kd, row.names = NULL)
    names <- c("Time_Point", "Ratio(%)(unknown:PI3K_like)", "Knockdown(%)")
    #print(df)
    # print(timecourses[,2])
    # print(length(timecourses[,2]))
    # add the other columns
    for(i in 2:length (columns)) {
      df <- cbind(df,timecourses[,i])
      names <- c(names, columns[i])
    }
    names(df) <- names
    print(df)
    write.table(df, file=filename_out, row.names=FALSE, sep="\t")
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())
