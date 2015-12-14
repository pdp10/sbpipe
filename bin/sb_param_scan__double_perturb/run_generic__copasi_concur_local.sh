#!/bin/bash
 

PATH=$1
MODEL=$2
START=$3
END=$4
MAX_NPROC=$5

NUM=0
QUEUE=""

USAGE="run_concur_copasi_local.sh [path] [model_pattern] [start_ind] [end_idx] [ncpus]"




function queue {
	QUEUE="$QUEUE $1"
	NUM=$(($NUM+1))
}

function regeneratequeue {
	OLDREQUEUE=$QUEUE
	QUEUE=""
	NUM=0
	for PID in $OLDREQUEUE
	do
		if [ -d /proc/$PID  ] ; then
			QUEUE="$QUEUE $PID"
			NUM=$(($NUM+1))
		fi
	done
}

function checkqueue {
	OLDCHQUEUE=$QUEUE
	for PID in $OLDCHQUEUE
	do
		if [ ! -d /proc/$PID ] ; then
			regeneratequeue # at least one PID has finished
			break
		fi
	done
}


function main {
	echo "$USAGE"
	echo "Using $MAX_NPROC parallel threads"
	sleep="/bin/sleep 2s"
	# Run the MODELs in parallel
	for ((i=${START};i<=${END};i+=1))
	do
	      echo "CopasiSE --nologo -s ${PATH}/${MODEL}${i}.cps ${PATH}/${MODEL}${i}.cps &"
	      CopasiSE --nologo -s ${PATH}/${MODEL}${i}.cps ${PATH}/${MODEL}${i}.cps &
	      #CopasiSE "${MODEL}${i}.cps" &
	      PID=$!
	      queue $PID
	      while [ $NUM -ge $MAX_NPROC ]; do
		    checkqueue
		    `$sleep`
	      done
	done
	wait # wait for all processes to finish before exit
}

main
