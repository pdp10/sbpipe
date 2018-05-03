#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
import os
from sbpipe.pl.pipeline import Pipeline

logger = logging.getLogger('sbpipe')


class NewProj(Pipeline):
    """
    This module initialises the folder tree for a new project.

    :param models_folder: the folder containing the models
    :param working_folder: the folder to store the results    
    """

    def __init__(self, models_folder='Models', working_folder='Results'):
        """
        Constructor.
        """
        Pipeline.__init__(self, models_folder, working_folder)

    def run(self, project_name):
        """
        Create a project directory tree.

        :param project_name: the name of the project
        :return: 0
        """
        if not os.path.exists(project_name):
            os.mkdir(project_name)

        if not os.path.exists(os.path.join(project_name, self.get_models_folder())):
            os.mkdir(os.path.join(project_name, self.get_models_folder()))
        if not os.path.exists(os.path.join(project_name, self.get_working_folder())):
            os.mkdir(os.path.join(project_name, self.get_working_folder()))

        logger.info("Project " + project_name + " created.")
        return True
