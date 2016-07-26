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
# $Date: 2016-07-26 19:48:32 $

  

def install_r_deps(pkgs):
    """
     Install R packages using rpy2.robjects. 
    """
    # This requires lazy import for rpy2.robjects 
    # since rpy2 might not yet be available when this 
    # sb_pipe is started and this function is called
    # To prevent an ImportError message, we catch this 
    # as an exception if rpy2 is not found. When it is, 
    # the try block will pass correctly.
    try:
	exec 'import rpy2.robjects'
    except ImportError:
	return False

    import rpy2.robjects as robjects
    print('HERE')
    rpy2.robjects.r('''
	install_r_deps <- function(x) {
	    if (!suppressMessages(suppressWarnings(require(x, character.only=TRUE)))) {
		install.packages(x, dep=TRUE, repos='http://cran.us.r-project.org')
		if(!suppressMessages(suppressWarnings(require(x,character.only=TRUE)))) {
		    print(paste("R Package", x, "not found.", sep=" "))
		    FALSE
		}
	    }
	    TRUE
	}
    ''')    
    install_r_deps_py = rpy2.robjects.r['install_r_deps']
    pkgs_status = True
    for pkg in pkgs:
      if not install_r_deps_py(pkg):
	  pkgs_status = False
    return pkgs_status
