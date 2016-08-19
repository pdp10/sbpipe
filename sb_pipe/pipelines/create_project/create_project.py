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

SB_PIPE = os.environ["SB_PIPE"]

sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines"))
from pipeline import Pipeline


class CreateProject(Pipeline):
    """
    This module initialises the folder tree for a new project.
    """
      
    def __init__(self):
	Pipeline.__init__(self)




    def run(self, project_name):
      """
      Create a project tree.
      Keyword arguments:
	  project_name -- the project name
      """
      
      if not os.path.exists(project_name):
	os.mkdir(project_name)

      if not os.path.exists(os.path.join(project_name,'Data')):
	os.mkdir(os.path.join(project_name,'Data'))
      if not os.path.exists(os.path.join(project_name,'Models')):
	os.mkdir(os.path.join(project_name,'Models'))
      if not os.path.exists(os.path.join(project_name,'Working_Folder')):
	os.mkdir(os.path.join(project_name,'Working_Folder'))
      if not os.path.exists(os.path.join(project_name,'tmp')):
	os.mkdir(os.path.join(project_name,'tmp'))

      if not os.path.exists(os.path.join(project_name,'Models','previous_models')):
	os.mkdir(os.path.join(project_name,'Models','previous_models'))    
      if not os.path.exists(os.path.join(project_name,'paper')):
	os.mkdir(os.path.join(project_name,'paper'))
      if not os.path.exists(os.path.join(project_name,'paper','figures')):
	os.mkdir(os.path.join(project_name,'paper','figures'))    
      if not os.path.exists(os.path.join(project_name,'SBGN_graphic_models')):
	os.mkdir(os.path.join(project_name,'SBGN_graphic_models'))
      if not os.path.exists(os.path.join(project_name,'SBGN_graphic_models','previous_models')):
	os.mkdir(os.path.join(project_name,'SBGN_graphic_models','previous_models'))        

      #if not os.path.exists(os.path.join(project_name,'GENSSI_struct_identif')):
	#os.mkdir(os.path.join(project_name,'GENSSI_struct_identif'))
      #if not os.path.exists(os.path.join(project_name,'MOTA_identif')):
	#os.mkdir(os.path.join(project_name,'MOTA_identif'))
      #if not os.path.exists(os.path.join(project_name,'sbtoolbox2')):
	#os.mkdir(os.path.join(project_name,'sbtoolbox2'))
      #if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name')):
	#os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name'))
      #if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name','estimations')):
	#os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name','estimations'))
      #if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name','experiments')):
	#os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name','experiments'))        
      #if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name','models')):
	#os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name','models'))
	    
      logger.info("Project " + project_name + " created.")
      return 0
