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
# Object: A script to check whether an R package is installed. Callable from other programming languages using Rscript.
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-12-07 21:14:32 $



# Return TRUE if the package is installed, FALSE otherwise
#
# :param x: the package name to check
# :return: TRUE if the x is installed.
is_package_installed <- function(x) {
    # no need to be noisy here.
    if (!suppressMessages(suppressWarnings(require(x, character.only=TRUE)))) {
        FALSE
    } else {
        TRUE
    }
}

main <- function(args) {
    package <- args[1]
    print(is_package_installed(package))
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
