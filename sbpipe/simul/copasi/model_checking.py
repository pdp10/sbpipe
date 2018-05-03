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
import sys
import os

from sbpipe.utils.io import write_mat_on_file

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


def copasi_model_checking(model_filename, fileout, task_name=""):
    """
    Perform a basic model checking for a COPASI model file.

    :param model_filename: the filename to a COPASI file
    :param fileout: the file containing the model checking results
    :param task_name: the task to check
    :return: a boolean indicating whether the model could be loaded successfully
    """

    try:
        data_model = COPASI.CCopasiRootContainer.addDatamodel()
    except:
        data_model = COPASI.CRootContainer.addDatamodel()

    # clear previous log messages
    COPASI.CCopasiMessage.clearDeque()

    outcome = []

    # list of checks
    if not check_model_loading(model_filename, data_model):
        outcome.append('model loading\tERROR')
        write_mat_on_file(fileout, outcome)
        return False
    else:
        outcome.append('model loading\tPASS')

    if not check_task_selection(model_filename, task_name, data_model):
        outcome.append('task selection\tERROR')
        write_mat_on_file(fileout, outcome)
        return False
    else:
        outcome.append('task selection\tPASS')

    write_mat_on_file(fileout, outcome)
    return True


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


def check_model_loading(model_filename, data_model):
    """
    Check whether the COPASI model can be loaded

    :param model_filename: the filename to a COPASI file
    :param data_model: the COPASI data model structure
    :return: a boolean indicating whether the model could be loaded successfully
    """

    # check whether the model cannot be loaded
    if not data_model.loadModel(model_filename):
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

    return True


def check_task_selection(model_filename, task_name, data_model):
    """
    Check whether the COPASI model task can be executed

    :param model_filename: the filename to a COPASI file
    :param task_name: the task to check
    :param data_model: the COPASI data model structure.
    :return: a boolean indicating whether the model task can be executed correctly
    """

    # MODEL TASK
    if task_name:
        task = data_model.getTask(task_name)

        # check whether no task was selected
        if task is None:
            logger.error('No task with name `{0}` was found'.format(task_name))
            return False

        # check whether the task is scheduled, otherwise it will not run from CopasiSE
        logger.debug('Task `{0}` is {1}'.format(task_name,
                                            "scheduled" if task.isScheduled() else "not scheduled"))

        # check whether the task cannot be initialized
        if not task.initialize(COPASI.CCopasiTask.OUTPUT_UI):
            logger.error('COPASI task `{0}` cannot be initialised'.format(task_name))
            task.process(True)
            logger.error(task.getProcessError())
            return False

        if not check_task_report(model_filename, task_name, data_model, task):
            return False

    return True


def check_task_report(model_filename, task_name, data_model, task):
    """
    Check whether the COPASI model task can be executed

    :param model_filename: the filename to a COPASI file
    :param task_name: the task to check
    :param data_model: the COPASI data model structure
    :param task: the COPASI task data structure
    :return: a boolean indicating whether the model task can be executed correctly
    """

    report_filename = task.getReport().getTarget()

    # check whether a report was not configured
    if not report_filename:
        logger.error('No report was configured for COPASI task `{0}`'.format(task_name))
        return False

    # check whether the report name is different from the model name
    model_name = os.path.splitext(os.path.basename(model_filename))[0]
    report_name = os.path.splitext(os.path.basename(report_filename))[0]
    report_ext = os.path.splitext(os.path.basename(report_filename))[1]
    change_report_name = False
    change_report_ext = False
    if model_name != report_name:
        logger.warning('The report filename differs from the model name.')
        report_name = model_name
        change_report_name = True
    if report_ext not in {'.csv', '.txt', '.tsv', '.dat'}:
        logger.warning('The report extension must be one of the following: .csv, .txt, .tsv, or .dat')
        report_ext = '.csv'
        change_report_ext = True
    if change_report_name or change_report_ext:
        logger.warning('SBpipe will update the report file name to `{0}{1}`'.format(report_name, report_ext))
        task.getReport().setTarget(report_name + report_ext)
        task.getReport().setAppend(False)
        # save the model to a COPASI file
        data_model.saveModel(model_filename, True)

    # dunno why this is generated.. it seems a bug in Copasi to me..
    fake_report = os.path.join(os.path.dirname(model_filename), report_filename)
    if os.path.exists(fake_report):
        os.remove(fake_report)

    logger.info('COPASI task `{0}` can be executed'.format(task_name))

    return True

