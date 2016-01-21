#!/bin/bash
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#    
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $


# This script executes CopasiSE ntimes. 
# The computation is on an openlava cluster


# the path of the model
PATH=$1
# the model pattern name (e.g. mtor_model_ )
MODEL=$2
# the number of models (e.g. 3 if: mtor_model_1.cps, mtor_model_2.cps, mtor_model_3.cps)
NUM=$3



USAGE="run_concur_copasi_cluster.sh [path] [model_pattern] [n_times]"


echo "$USAGE"
for (( i=1; i<=${NUM}; i+=1 ))
do
  # run copasi on openlava on the cluster
  echo "bsub CopasiSE ${PATH}/${MODEL}${i}.cps"
  bsub -q npdp2_queue CopasiSE "${PATH}/${MODEL}${i}.cps"  
done

