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
# Performs some controls on the Copasi model.


import logging
import sys

if sys.version_info > (3,):
    import importlib
    COPASI_loader = importlib.util.find_spec('COPASI')
    found = COPASI_loader is not None
else:
    import imp
    try:
        imp.find_module('COPASI')
        found = True
    except ImportError:
        found = False

if found:
    import COPASI


logger = logging.getLogger('sbpipe')


def severity2string(severity):
    """
    Return a string representing the severity of the error message
    :param severity: an integer representing severity
    :return: a string of the error message
    """

    return {

        COPASI.CCopasiMessage.RAW: "RAW",
        COPASI.CCopasiMessage.TRACE: "TRACE",
        COPASI.CCopasiMessage.COMMANDLINE: "COMMANDLINE",
        COPASI.CCopasiMessage.WARNING: "WARNING",
        COPASI.CCopasiMessage.ERROR: "ERROR",
        COPASI.CCopasiMessage.EXCEPTION: "EXCEPTION",
        COPASI.CCopasiMessage.RAW_FILTERED: "RAW_FILTERED",
        COPASI.CCopasiMessage.TRACE_FILTERED: "TRACE_FILTERED",
        COPASI.CCopasiMessage.COMMANDLINE_FILTERED: "COMMANDLINE_FILTERED",
        COPASI.CCopasiMessage.WARNING_FILTERED: "WARNING_FILTERED",
        COPASI.CCopasiMessage.ERROR_FILTERED: "ERROR_FILTERED",
        COPASI.CCopasiMessage.EXCEPTION_FILTERED: "EXCEPTION_FILTERED"

    }.get(severity, COPASI.CCopasiMessage.RAW)


def check_model_file(model_filename, task_name=""):
    """
    Load the model into COPASI and checks whether the given task can be executed

    :param model_filename: the filename to a COPASI file
    :param task_name: the task to check
    :return: a boolean indicating whether the model could be loaded successfully
    """

    try:
        dataModel = COPASI.CCopasiRootContainer.addDatamodel()
    except:
        dataModel = COPASI.CRootContainer.addDatamodel()

    # clear previous log messages
    COPASI.CCopasiMessage.clearDeque()

    # CHECK WHETHER THE MODEL CAN BE LOADED

    # load the model
    if not dataModel.loadModel(model_filename):
        logger.error('The model cannot be loaded into COPASI and has serious issues')
        logger.error(COPASI.CCopasiMessage.getAllMessageText())
        return False

    # the model could be loaded fine, but we could still print possible warnings
    if COPASI.CCopasiMessage.size() > 1:
        logger.warning('The highest error severity encountered was: {0}'.
                       format(severity2string(COPASI.CCopasiMessage.getHighestSeverity())))
        logger.warning(COPASI.CCopasiMessage.getAllMessageText())
    else:
        logger.info('The model can be loaded without any apparent issues')

    # CHECK WHETHER MODEL TASK (IF ANY) IS SET CORRECTLY

    if task_name:
        task = dataModel.getTask(task_name)

        if task is None:
            logger.error('No task with name `{0}` was found'.format(task_name))
            return False

        # see whether the task is scheduled, otherwise it will not run from CopasiSE
        logger.debug('Task `{0}` is {1}'.format(task_name,
                                            "scheduled" if task.isScheduled() else "not scheduled"))

        # see whether the task can be initialized
        if not task.initialize(COPASI.CCopasiTask.OUTPUT_UI):
            logger.error('COPASI task `{0}` cannot be initialised'.format(task_name))

            task.process(True)
            logger.error(task.getProcessError())
            return False

        logger.info('COPASI task `{0}` can be executed'.format(task_name))

    return True
