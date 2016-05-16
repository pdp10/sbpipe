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
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $
 
 
path=$1
name=$2
ext=$3
replicates=$4

# Creates replicates
for (( i=1; i<=$replicates; i+=1 ))
do
  echo "cp ${path}/${name}.${ext} ${path}/${name}${i}.${ext}"
  cp ${path}/${name}.${ext} ${path}/${name}${i}.${ext}
done
