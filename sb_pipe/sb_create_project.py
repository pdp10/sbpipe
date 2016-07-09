#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-03-21 14:34:32 $


import sys
import os, os.path


"""
This module initialises the folder tree for a new project project.
"""

def main(project):
  """
  Create a project tree.
  Keyword arguments:
      project -- the project name
  """
  
  print("Create new folder tree for the new project "+project+" ... \n")

  if not os.path.exists(project):
    os.mkdir(project)

  if not os.path.exists(project+"/Data"):
    os.mkdir(project+"/Data")
  if not os.path.exists(project+"/Models"):
    os.mkdir(project+"/Models")
  if not os.path.exists(project+"/Working_Folder"):
    os.mkdir(project+"/Working_Folder")
  if not os.path.exists(project+"/tmp"):
    os.mkdir(project+"/tmp")

  if not os.path.exists(project+"/Models/previous_models"):
    os.mkdir(project+"/Models/previous_models")    
  if not os.path.exists(project+"/paper"):
    os.mkdir(project+"/paper")
  if not os.path.exists(project+"/paper/figures"):
    os.mkdir(project+"/paper/figures")    
  if not os.path.exists(project+"/SBGN_graphic_models"):
    os.mkdir(project+"/SBGN_graphic_models")
  if not os.path.exists(project+"/SBGN_graphic_models/previous_models"):
    os.mkdir(project+"/SBGN_graphic_models/previous_models")        

  if not os.path.exists(project+"/GENSSI_struct_identif"):
    os.mkdir(project+"/GENSSI_struct_identif")
  if not os.path.exists(project+"/MOTA_identif"):
    os.mkdir(project+"/MOTA_identif")
  if not os.path.exists(project+"/sbtoolbox2"):
    os.mkdir(project+"/sbtoolbox2")
  if not os.path.exists(project+"/sbtoolbox2/project"):
    os.mkdir(project+"/sbtoolbox2/project")
  if not os.path.exists(project+"/sbtoolbox2/project/estimations"):
    os.mkdir(project+"/sbtoolbox2/project/estimations")
  if not os.path.exists(project+"/sbtoolbox2/project/experiments"):
    os.mkdir(project+"/sbtoolbox2/project/experiments")        
  if not os.path.exists(project+"/sbtoolbox2/project/models"):
    os.mkdir(project+"/sbtoolbox2/project/models")
        
  print("DONE!\n")
  return 0
