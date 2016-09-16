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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $
#
# Desc: A basic callback counter


# On client side, run this program

import thread
import sys
import logging
logger = logging.getLogger('sbpipe')

# This is a monitor.
# Callback class for collecting information about finished processes
class BasicSyncCounter:
    __count = 0
    __value = True
    
    # class constructor
    def __init__(self):
        self.lock = thread.allocate_lock()
        self.__count = 0
    
    # the callback function
    # Note: pid is callbackargs passed to submit
    # value is the return value of the function part_sum (which is parallelised), 
    # so it is the callback value.
    def add(self, pid, value):
        # we must use lock here because += is not atomic
        self.lock.acquire()
        self.__count = self.__count + 1
        # We don't do much with this value, but the idea is that one could combine the values 
        # with a desired logic. Here we only use it to collect an overall status of the parallel computation.
        self.__value = self.__value and value
        self.lock.release()
    
    # get methods
    def get_value(self):
        temp = 0.0
        self.lock.acquire()
        temp = self.__value
        self.lock.release()
        return temp
    
    def get_count(self):
        temp = 0.0
        self.lock.acquire()
        temp = self.__count
        self.lock.release()
        return temp
