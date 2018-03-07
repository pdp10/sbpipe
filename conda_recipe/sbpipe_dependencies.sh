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


# NOTE: THIS IS NO LONGER NEEDED AS ALL THE REQUIRED PACKAGES ARE STORED IN CONDA-FORGE CHANNEL.


# create conda packages for SBpipe dependencies so that they are stored in pdp10 channel.
# This helps avoid conflicts between channels



#conda install conda-build

## R package colorramps
#conda skeleton cran colorramps
#conda build r-colorramps
#conda install -c local r-colorramps


## python package colorlog (this fails in the second instruction)
#conda skeleton pypi colorlog
#conda build colorlog
#conda install -c local colorlog
