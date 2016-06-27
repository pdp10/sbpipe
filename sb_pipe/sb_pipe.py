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
# Object: sb_pipe main 
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-27 10:18:32 $


  

import sys
import getopt

# pipelines
import sb_create_project
import sb_simulate
import sb_param_estim__copasi
import sb_param_scan__single_perturb
import sb_sensitivity


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg




# E.g. command: python sb_pipe.py sb_simulate model_ins_rec_v1_det_simul.conf 


"""Module docstring.

This serves as a long usage message.

Based on http://www.artima.com/weblogs/viewpost.jsp?thread=4829 
""" 
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            print args[0]

	    if args[0] == "create_project":
		sb_create_project.main(args[1])            
            
	    if args[0] == "simulate":
		sb_simulate.main(args[1])
		
	    if args[0] == "single_perturb":
		sb_param_scan__single_perturb.main(args[1])
	    
	    if args[0] == "param_estim":
		sb_param_estim__copasi.main(args[1])
	    
	    if args[0] == "sensitivity":
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
    
    
    