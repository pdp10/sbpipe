#!/bin/bash
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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-03-21 14:34:32 $

# This script initialises the folder tree for a new project


# The project name
project=$1


printf "Create new folder tree for the new project ${project} ... \n"


mkdir -p ${project}

mkdir -p ${project}/Data
mkdir -p ${project}/GENSSI_struct_identif
mkdir -p ${project}/Models
mkdir -p ${project}/MOTA_identif
mkdir -p ${project}/paper
mkdir -p ${project}/SBGN_graphic_models
mkdir -p ${project}/sbtoolbox2
mkdir -p ${project}/simulations
mkdir -p ${project}/Working_Folder
mkdir -p ${project}/tmp


mkdir -p ${project}/Models/previous_models

mkdir -p ${project}/paper/figures

mkdir -p ${project}/SBGN_graphic_models/previous_models


mkdir -p ${project}/sbtoolbox2/project
mkdir -p ${project}/sbtoolbox2/project/estimations
mkdir -p ${project}/sbtoolbox2/project/experiments
mkdir -p ${project}/sbtoolbox2/project/models


printf "DONE!\n"



