#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
#
# Desc: A simple callback counter


###############################################################
# You can put this into a script and run it on server side..
# on server side (here: 127.0.0.1), start:
# ppserver.py -p 65000 -i 127.0.0.1 -s -w 5 "donald_duck" &
#
# NB: -w is the number of core YOU can use. If a server is used by more users, 
# set the number lower than the number of cpus
#
# Command line options, ppserver.py
# Usage: ppserver.py [-hda] [-i interface] [-b broadcast] [-p port] [-w nworkers] [-s secret] [-t seconds]
# Options:
# -h                 : this help message
# -d                 : debug
# -a                 : enable auto-discovery service
# -i interface       : interface to listen
# -b broadcast       : broadcast address for auto-discovery service
# -p port            : port to listen
# -w nworkers        : number of workers to start
# -s secret          : secret for authentication
# -t seconds         : timeout to exit if no connections with clients exist
###############################################################


# On client side, run this program

import thread, sys


# Callback class for collecting information about finished processes
class SyncCounter:
    _count = 0
    # class constructor
    def __init__(self):
        self.lock = thread.allocate_lock()
        self._count = 0
    # the callback function
    # Note: pid is callbackargs passed to submit
    def add(self, pid):
        # we must use lock here because += is not atomic
        self.lock.acquire()
        self._count = self._count + 1
        # print() is inside the monitor..  mmh! :(
        print("Process P" + str(pid) + " completed")
        self.lock.release()
    # get methods
    def get_count(self):
        temp = 0.0
        self.lock.acquire()
        temp = self._count
        self.lock.release()
        return temp
