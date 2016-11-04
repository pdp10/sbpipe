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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $
#
# Desc: A basic callback counter


# On client side, run this program

import logging
import thread

logger = logging.getLogger('sbpipe')


class Monitor:
    """
    This is a monitor. It is a callback class for collecting information about finished processes. It 
    is used by Parallel Python (pp).
    """

    __count = 0
    __value = True

    def __init__(self):
        """
        Constructor.
        """
        self.lock = thread.allocate_lock()
        self.__count = 0

    def add(self, pid, value):
        """
        The callback function

        :param pid: this is callbackargs passed to parallel python `submit()` method
        :param value: the return value of the parallelised function. It is the callback value.        
        """
        # we must use lock here because += is not atomic
        self.lock.acquire()
        self.__count += 1
        # We don't do much with this value, but the idea is that one could combine the values 
        # with a desired logic. Here we only use it to collect an overall status of the parallel computation.
        self.__value = self.__value and value
        self.lock.release()

    # get methods
    def get_value(self):
        """
        Return the internal status.
        
        :return: True if the counter is empty.
        """
        temp = 0.0
        self.lock.acquire()
        temp = self.__value
        self.lock.release()
        return temp

    def get_count(self):
        """
        Return the counter
        
        :return: the number of running processes.
        """
        temp = 0.0
        self.lock.acquire()
        temp = self.__count
        self.lock.release()
        return temp
