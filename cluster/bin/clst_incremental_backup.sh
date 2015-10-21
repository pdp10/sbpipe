#!/bin/bash


# incremental backup on the Daryl Shanley's cluster. 
# This script is executed by iah-huygens.

# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013



# cp -plRu /home/* /media/backup 
# Note: add -z option if transferring on another computer.
printf "\nSynchronisation of the modellers cluster\n"
#rsync -auz --quiet /home/modellers/* /media/backup/
rsync -auz --quiet /home/modellers/* /mnt/iah526_nfs_users_backup/
printf "\nSynchronisation completed\n"
