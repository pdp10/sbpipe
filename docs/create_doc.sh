#!/bin/bash
# -*- coding: utf-8 -*-
#
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
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-09-14 13:38:32 $


echo "cleaning previous source code documentation"
rm -rf source/source_code


echo "creating DAG files for SBpipe pipelines using snakemake..."
./create_snakemake_dags.sh


echo "generating documentation in LaTeX/PDF format ..."
# we only distribute the manual for SBpipe in PDF format.
#make html
make latexpdf
#make man


echo "moving sbpipe.pdf file to ."
mv build/latex/sbpipe.pdf .


echo "cleaning output files ..."
# clean previously generated documentation
make clean
rm -rf build
