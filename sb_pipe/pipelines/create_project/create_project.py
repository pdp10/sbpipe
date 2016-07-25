#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-03-21 14:34:32 $


import sys
import os
import logging
logger = logging.getLogger('sbpipe')


"""
This module initialises the folder tree for a new project project.
"""

def main(project):
  """
  Create a project tree.
  Keyword arguments:
      project -- the project name
  """
  
  if not os.path.exists(project):
    os.mkdir(project)

  if not os.path.exists(os.path.join(project,'Data')):
    os.mkdir(os.path.join(project,'Data'))
  if not os.path.exists(os.path.join(project,'Models')):
    os.mkdir(os.path.join(project,'Models'))
  if not os.path.exists(os.path.join(project,'Working_Folder')):
    os.mkdir(os.path.join(project,'Working_Folder'))
  if not os.path.exists(os.path.join(project,'tmp')):
    os.mkdir(os.path.join(project,'tmp'))

  if not os.path.exists(os.path.join(project,'Models','previous_models')):
    os.mkdir(os.path.join(project,'Models','previous_models'))    
  if not os.path.exists(os.path.join(project,'paper')):
    os.mkdir(os.path.join(project,'paper'))
  if not os.path.exists(os.path.join(project,'paper','figures')):
    os.mkdir(os.path.join(project,'paper','figures'))    
  if not os.path.exists(os.path.join(project,'SBGN_graphic_models')):
    os.mkdir(os.path.join(project,'SBGN_graphic_models'))
  if not os.path.exists(os.path.join(project,'SBGN_graphic_models','previous_models')):
    os.mkdir(os.path.join(project,'SBGN_graphic_models','previous_models'))        

  #if not os.path.exists(os.path.join(project,'GENSSI_struct_identif')):
    #os.mkdir(os.path.join(project,'GENSSI_struct_identif'))
  #if not os.path.exists(os.path.join(project,'MOTA_identif')):
    #os.mkdir(os.path.join(project,'MOTA_identif'))
  #if not os.path.exists(os.path.join(project,'sbtoolbox2')):
    #os.mkdir(os.path.join(project,'sbtoolbox2'))
  #if not os.path.exists(os.path.join(project,'sbtoolbox2','project')):
    #os.mkdir(os.path.join(project,'sbtoolbox2','project'))
  #if not os.path.exists(os.path.join(project,'sbtoolbox2','project','estimations')):
    #os.mkdir(os.path.join(project,'sbtoolbox2','project','estimations'))
  #if not os.path.exists(os.path.join(project,'sbtoolbox2','project','experiments')):
    #os.mkdir(os.path.join(project,'sbtoolbox2','project','experiments'))        
  #if not os.path.exists(os.path.join(project,'sbtoolbox2','project','models')):
    #os.mkdir(os.path.join(project,'sbtoolbox2','project','models'))
        
  logger.info("Project " + project + " created.")
  return 0
