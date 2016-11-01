#!/bin/bash
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
# $Date: 2016-09-14 13:38:32 $


./clean_doc.sh



# Import manuals
# convert user_manual.md to user_manual.rst
pandoc --from=markdown --to=rst --output=source/user_manual.rst source/user_manual.md
# convert developer_manual.md to developer_manual.rst
pandoc --from=markdown --to=rst --output=source/developer_manual.rst source/developer_manual.md


# Import source code documentation
#sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/create_project/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/double_param_scan/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/param_estim/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/sensitivity/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/simulate/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/simulator/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/pipelines/single_param_scan/
sphinx-apidoc -P -T -o source/source_code $SBPIPE/sbpipe/utils/python/


# Generate documentation in html, LaTeX/PDF, and man
make html
make latexpdf
