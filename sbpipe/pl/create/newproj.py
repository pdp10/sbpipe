#!/usr/bin/env python
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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-03-21 14:34:32 $


import logging
import os
from sbpipe.pl.pipeline import Pipeline

logger = logging.getLogger('sbpipe')


class NewProj(Pipeline):
    """
    This module initialises the folder tree for a new project.

    :param data_folder: the folder containing the data
    :param models_folder: the folder containing the models
    :param working_folder: the folder to store the results    
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder'):
        """
        Constructor.
        """
        Pipeline.__init__(self, data_folder, models_folder, working_folder)

    def run(self, project_name):
        """
        Create a project directory tree.

        :param project_name: the name of the project
        :return: 0
        """
        if not os.path.exists(project_name):
            os.mkdir(project_name)

        if not os.path.exists(os.path.join(project_name, self.get_data_folder())):
            os.mkdir(os.path.join(project_name, self.get_data_folder()))
        if not os.path.exists(os.path.join(project_name, self.get_models_folder())):
            os.mkdir(os.path.join(project_name, self.get_models_folder()))
        if not os.path.exists(os.path.join(project_name, self.get_working_folder())):
            os.mkdir(os.path.join(project_name, self.get_working_folder()))

        if not os.path.exists(os.path.join(project_name, self.get_models_folder(), 'previous_models')):
            os.mkdir(os.path.join(project_name, self.get_models_folder(), 'previous_models'))
        if not os.path.exists(os.path.join(project_name, 'Manuscript')):
            os.mkdir(os.path.join(project_name, 'Manuscript'))
        if not os.path.exists(os.path.join(project_name, 'Manuscript', 'figures')):
            os.mkdir(os.path.join(project_name, 'Manuscript', 'figures'))
        if not os.path.exists(os.path.join(project_name, 'SBGN_graphic_models')):
            os.mkdir(os.path.join(project_name, 'SBGN_graphic_models'))
        if not os.path.exists(os.path.join(project_name, 'SBGN_graphic_models', 'previous_models')):
            os.mkdir(os.path.join(project_name, 'SBGN_graphic_models', 'previous_models'))

        # if not os.path.exists(os.path.join(project_name,'GENSSI_struct_identif')):
        # os.mkdir(os.path.join(project_name,'GENSSI_struct_identif'))
        # if not os.path.exists(os.path.join(project_name,'MOTA_identif')):
        # os.mkdir(os.path.join(project_name,'MOTA_identif'))
        # if not os.path.exists(os.path.join(project_name,'sbtoolbox2')):
        # os.mkdir(os.path.join(project_name,'sbtoolbox2'))
        # if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name')):
        # os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name'))
        # if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name','estimations')):
        # os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name','estimations'))
        # if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name','experiments')):
        # os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name','experiments'))
        # if not os.path.exists(os.path.join(project_name,'sbtoolbox2','project_name','models')):
        # os.mkdir(os.path.join(project_name,'sbtoolbox2','project_name','models'))

        logger.info("Project " + project_name + " created.")
        return True
