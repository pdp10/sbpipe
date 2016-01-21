# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should hade received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $


library(abind)




# Load a collection of files in a three dimensional matrix
load_files_columns_in_matrix <- function(inputdir, files, col_names) {

    # Load files in memory
    dataset <- read.table(paste(inputdir,files[1],sep=""),header=TRUE,colClasses=col_names,na.strings="NA",dec=".",sep="\t")
    #print(dataset)
    if(length(files) > 1) {
      for(i in 2:length(files)) {
	# add a matrix to dataset containing the next table (file)
	# dataset becomes tridimensional
	dataset <- abind(dataset, read.table(paste(inputdir,files[i],sep=""),header=TRUE,colClasses=col_names,na.strings="NA",dec=".",sep="\t"), along=3)
      }
    }
    return (dataset)
}


# Load a collection of files in a three dimensional matrix
load_files_in_matrix <- function(inputdir, files) {
    # Load files in memory
    dataset <- read.table(paste(inputdir,files[1],sep=""),header=TRUE,na.strings="NA",dec=".",sep="\t")
    if(length(files) > 1) {
      for(i in 2:length(files)) {
	# add a matrix to dataset containing the next table (file)
	# dataset becomes tridimensional
	dataset <- abind(dataset, read.table(paste(inputdir,files[i],sep=""),header=TRUE,na.strings="NA",dec=".",sep="\t"), along=3)
      }
    }
    return (dataset)
}


# Load a collection of files in a three dimensional matrix
load_files_in_matrix_wlevels <- function(inputdir, files, levels) {
    dataset <- read.table(paste(inputdir,files[levels[1]],sep=""),header=TRUE,
		na.strings="NA",dec=".",sep="\t")
    if(length(levels) > 1) {
      for(i in 2:length(levels)) {
	# add a matrix to dataset containing the next table (file)
	# dataset becomes tridimensional
	dataset <- abind(dataset, read.table(paste(inputdir,files[levels[i]],sep=""),header=TRUE,na.strings="NA",
		   dec=".",sep="\t"), along=3)
      }
    }
    return (dataset)
}
