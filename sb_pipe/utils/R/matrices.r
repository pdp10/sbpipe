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
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-7 16:14:32 $


library(abind)




# Load a collection of files in a three dimensional matrix
load_files_columns_in_matrix <- function(inputdir, files, col_names) {

    # Load files in memory
    dataset <- read.table(file.path(inputdir,files[1]),header=TRUE,colClasses=col_names,na.strings="NA",dec=".",sep="\t")
    #print(dataset)
    if(length(files) > 1) {
      for(i in 2:length(files)) {
	# add a matrix to dataset containing the next table (file)
	# dataset becomes tridimensional
	dataset <- abind(dataset, read.table(file.path(inputdir,files[i]),header=TRUE,colClasses=col_names,na.strings="NA",dec=".",sep="\t"), along=3)
      }
    }
    return (dataset)
}


# Load a collection of files in a three dimensional matrix
load_files_in_matrix <- function(inputdir, files) {
    # Load files in memory
    dataset <- read.table(file.path(inputdir,files[1]),header=TRUE,na.strings="NA",dec=".",sep="\t")
    if(length(files) > 1) {
      for(i in 2:length(files)) {
	# add a matrix to dataset containing the next table (file)
	# dataset becomes tridimensional
	dataset <- abind(dataset, read.table(file.path(inputdir,files[i]),header=TRUE,na.strings="NA",dec=".",sep="\t"), along=3)
      }
    }
    return (dataset)
}


# Load a collection of files in a three dimensional matrix
load_files_in_matrix_wlevels <- function(inputdir, files, levels) {
    dataset <- read.table(file.path(inputdir,files[levels[1]]),header=TRUE,
		na.strings="NA",dec=".",sep="\t")
    if(length(levels) > 1) {
      for(i in 2:length(levels)) {
	# add a matrix to dataset containing the next table (file)
	# dataset becomes tridimensional
	dataset <- abind(dataset, read.table(file.path(inputdir,files[levels[i]]),header=TRUE,na.strings="NA",
		   dec=".",sep="\t"), along=3)
      }
    }
    return (dataset)
}
