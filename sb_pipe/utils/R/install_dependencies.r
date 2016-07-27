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
# Object: install required dependencies automatically
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-26 19:48:32 $


set_r_libs <- function() {
    R_LIBS <- Sys.getenv(c("R_LIBS"))
    if(R_LIBS == "") {
        HOME <- Sys.getenv(c("HOME"))
        r_folder <- file.path(HOME, 'R')
	Sys.setenv(R_LIBS = r_folder)
	dir.create(r_folder, showWarnings = FALSE)
	R_LIBS <- r_folder
    }
}    

    
install_r_deps <- function(x, r_libs) {
    # no need to be noisy here.
    if (!suppressMessages(suppressWarnings(require(x, character.only=TRUE)))) {
        install.packages(x, lib=r_libs, dep=TRUE, repos='http://cran.r-project.org')
        if(!suppressMessages(suppressWarnings(require(x,character.only = TRUE)))) {
            print(paste("R Package", x, "not found.", sep=" "))
        }
    }
}


main <- function(args) {
   r_libs <- set_r_libs()
   for(i in 1:length(args)) {
       install_r_deps(args[i], r_libs)
   }
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
