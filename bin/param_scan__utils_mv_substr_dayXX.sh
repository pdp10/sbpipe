#!/bin/bash
# Piero Dalle Pezze




# This script moves the substring "_dayXX" at the end of the file.

folder=$1


for filenamein in `ls $folder/*.png `
do
    daynum=`expr match "$filenamein" '.*_day\([[:digit:]]*\)_.*' `
    daynum="_day${daynum}"
#echo "${daynum}"

    filenameout=${filenamein/$daynum/""}
    filenameout=${filenameout/.png/${daynum}.png}

    echo "${filenamein} => ${filenameout}"
    mv ${filenamein} ${filenameout}
done
