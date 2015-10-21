#!/bin/bash


# mirror backup on the Daryl Shanley's cluster. 
# This script is executed by iah-huygens.

# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013



# cp -plRu /home/* /media/backup 
# Note: add -z option if transferring on another computer.
printf "\nSynchronisation of the modellers cluster\n"
#rsync -auv --progress /home/* /media/backup/
rsync -auvz --quiet --delete /home/modellers/* /mnt/modelling_nfs_users_backup/
printf "\nSynchronisation completed\n"
