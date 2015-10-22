#!/bin/bash

# Piero Dalle Pezze (2013)

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



