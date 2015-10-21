#!/bin/bash

# Mirror backup on the Daryl Shanley's cluster. 
# This script is executed by iah527.

# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013


# Note: add -z option if transferring on another computer.
printf "\nSynchronisation of the modellers cluster\n"
rsync -auvz --quiet --delete /home/modellers/* /media/backup/
printf "\nSynchronisation completed\n"
