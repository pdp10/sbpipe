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
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $

# mirror backup on the Daryl Shanley's cluster. 
# This script is executed by iah-huygens.




# cp -plRu /home/* /media/backup 
# Note: add -z option if transferring on another computer.
printf "\nSynchronisation of the modellers cluster\n"
#rsync -auv --progress /home/* /media/backup/
rsync -auvz --quiet --delete /home/modellers/* /mnt/modelling_nfs_users_backup/
printf "\nSynchronisation completed\n"
