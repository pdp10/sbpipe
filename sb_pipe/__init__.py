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
# $Date: 2016-06-26 23:00:32 $


def package_name():
    return ('sb_pipe')
  
  
def help():
    return ('See github.com page for sb_pipe')
  


  
"""Module docstring.

This serves as a long usage message.

Based on http://www.artima.com/weblogs/viewpost.jsp?thread=4829 
""" 
import sys
import getopt

# pipelines
import sb_simulate
import sb_param_estim__copasi
import sb_param_scan__single_perturb



class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            print args[0]
	    if args[0] == "sb_simulate":
		print("sb_simulate")
		sb_simulate.main(args[1])
		
	    if args[0] == "sb_param_scan__single_perturb":
		print("sb_param_scan__single_perturb")
		sb_param_scan__single_perturb.main(args[1])
	    
	    if args[0] == "sb_param_estim__copasi":
		print("sb_param_estim__copasi")
		sb_param_estim__copasi.main(args[1])
	    
	    if args[0] == "sb_sensitivity":
		print("sb_sensitivity")
		sb_sensitivity.main(args[1])
	    
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())    
    
    
    