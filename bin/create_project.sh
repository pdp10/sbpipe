#!/bin/bash

# Piero Dalle Pezze (2013)

# This script initialises the folder tree for a new project


# The project name
project=$1


printf "Create new folder tree for the new project ${project} ... \n"


mkdir -p ${PROJ_DIR}/${project}

mkdir -p ${PROJ_DIR}/${project}/Data
mkdir -p ${PROJ_DIR}/${project}/GENSSI_struct_identif
mkdir -p ${PROJ_DIR}/${project}/Models
mkdir -p ${PROJ_DIR}/${project}/MOTA_identif
mkdir -p ${PROJ_DIR}/${project}/paper
mkdir -p ${PROJ_DIR}/${project}/SBGN_graphic_models
mkdir -p ${PROJ_DIR}/${project}/sbtoolbox2
mkdir -p ${PROJ_DIR}/${project}/simulations
mkdir -p ${PROJ_DIR}/${project}/working_folder
mkdir -p ${PROJ_DIR}/${project}/tmp


mkdir -p ${PROJ_DIR}/${project}/Models/previous_models

mkdir -p ${PROJ_DIR}/${project}/paper/figures

mkdir -p ${PROJ_DIR}/${project}/SBGN_graphic_models/previous_models


mkdir -p ${PROJ_DIR}/${project}/sbtoolbox2/project
mkdir -p ${PROJ_DIR}/${project}/sbtoolbox2/project/estimations
mkdir -p ${PROJ_DIR}/${project}/sbtoolbox2/project/experiments
mkdir -p ${PROJ_DIR}/${project}/sbtoolbox2/project/models


printf "DONE!\n"



