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


mkdir -p ${SB_PIPE}/${project}

mkdir -p ${SB_PIPE}/${project}/Data
mkdir -p ${SB_PIPE}/${project}/GENSSI_struct_identif
mkdir -p ${SB_PIPE}/${project}/Models
mkdir -p ${SB_PIPE}/${project}/MOTA_identif
mkdir -p ${SB_PIPE}/${project}/paper
mkdir -p ${SB_PIPE}/${project}/SBGN_graphic_models
mkdir -p ${SB_PIPE}/${project}/sbtoolbox2
mkdir -p ${SB_PIPE}/${project}/simulations
mkdir -p ${SB_PIPE}/${project}/working_folder
mkdir -p ${SB_PIPE}/${project}/tmp


mkdir -p ${SB_PIPE}/${project}/Models/previous_models

mkdir -p ${SB_PIPE}/${project}/paper/figures

mkdir -p ${SB_PIPE}/${project}/SBGN_graphic_models/previous_models


mkdir -p ${SB_PIPE}/${project}/sbtoolbox2/project
mkdir -p ${SB_PIPE}/${project}/sbtoolbox2/project/estimations
mkdir -p ${SB_PIPE}/${project}/sbtoolbox2/project/experiments
mkdir -p ${SB_PIPE}/${project}/sbtoolbox2/project/models


printf "DONE!\n"



