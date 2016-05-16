#!/bin/bash

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




# clean the test results
cd tests
python clean_tests.py >/dev/null 2>/dev/null
cd -

# remove all .pyc files
pyclean .
rm -rf *~

# rm this silly file
rm -f test/ins_rec_model/Working_Folder/Rplots.pdf

