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
# $Date: 2016-11-01 15:43:32 $

import logging
from ..pl_simul import PLSimul

logger = logging.getLogger('sbpipe')


class Python(PLSimul):
    """
    Python Simulator.
    """

    def __init__(self):
        __doc__ = PLSimul.__init__.__doc__

        PLSimul.__init__(self, "python", "Python not found! Please check that python is installed.", "")
        if self._language is None:
            logger.error(self._language_not_found_msg)
