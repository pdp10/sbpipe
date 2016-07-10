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
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $
#
# Desc: A basic callback counter


# On client side, run this program

import thread, sys

# This is a monitor.
# Callback class for collecting information about finished processes
class BasicSyncCounter:
    _count = 0
    _value = True
    # class constructor
    def __init__(self):
        self.lock = thread.allocate_lock()
        self._count = 0
    # the callback function
    # Note: pid is callbackargs passed to submit
    # value is the return value of the function part_sum (which is parallelised), 
    # so it is the callback value.
    def add(self, pid, value):
        # we must use lock here because += is not atomic
        self.lock.acquire()
        self._count = self._count + 1
        # We don't do much with this value, but the idea is that one could combine the values 
        # with a desired logic. Here we only use it to collect an overall status of the parallel computation.
        self._value = self._value and value
        self.lock.release()
        print("Process P" + str(pid) + " completed")
    # get methods
    def get_value(self):
        temp = 0.0
        self.lock.acquire()
        temp = self._value
        self.lock.release()
        return temp
    def get_count(self):
        temp = 0.0
        self.lock.acquire()
        temp = self._count
        self.lock.release()
        return temp
