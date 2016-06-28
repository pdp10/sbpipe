#!/bin/bash
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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $


path=$1
model_name=$2
start=$3
end=$4
ncpus=$5


proc_num=0
queue=""


function queue {
	queue="${queue} $1"
	proc_num=$((${proc_num}+1))
}

function regeneratequeue {
	old_queue=${queue}
	queue=""
	proc_num=0
	for PID in ${old_queue}
	do
		if [ -d /proc/${PID}  ] ; then
			queue="${queue} ${PID}"
			proc_num=$((${proc_num}+1))
		fi
	done
}

function checkqueue {
	old_queue=${queue}
	for PID in ${old_queue}
	do
		if [ ! -d /proc/${PID} ] ; then
			regeneratequeue # at least one PID has finished
			break
		fi
	done
}




function main {
	echo "run_generic__copasi_concur_local.sh [path] [model_pattern] [start_ind] [end_idx] [ncpus]"
	echo "Using $ncpus CPUs"
	sleep="/bin/sleep 2s"
	# Run the models in parallel
	for ((i=${start};i<=${end};i+=1))
	do
	      echo "CopasiSE --nologo -s ${path}/${model_name}${i}.cps ${path}/${model_name}${i}.cps &"
	      CopasiSE --nologo -s ${path}/${model_name}${i}.cps ${path}/${model_name}${i}.cps &
	      PID=$!
	      queue $PID
	      while [ ${proc_num} -ge ${ncpus} ]; do
		    checkqueue
		    `$sleep`
	      done
	done
	wait # wait for all processes to finish before exit
}

main