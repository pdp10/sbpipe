#!/bin/bash

# Script for full backup of the cluster server.
# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013


# Place in cron to execute it automatically (sudo crontab -e)
# # m h  dom mon dow   command
# 0 7 * * MON,THU sh /home/clst_server_cloning.sh

# references:
# (1) http://www.lullabot.com/blog/articles/simple-site-backups-rsync-ssh-and-sudo
# (2) https://gist.github.com/deviantintegral/0f1066650e3ea5c5ffc1
# This is executed on the backup machine ($DEST) (client)
# To allow backup, folders need permissions 755 


SOURCE=iah372.ncl.ac.uk
DEST=iah372backup.ncl.ac.uk

echo ""
echo "#############################################"
echo "Server backup ($SOURCE => $DEST)"
echo "#############################################"

# the user doing rsync
USER="rsync"

# Set the path to rsync on the remote server so it runs with sudo. NOTE 'single quotes' are required due to the space
RSYNC='/usr/bin/sudo /usr/bin/rsync'
 
# This is a list of files to ignore from backups.
EXCLUDES="/home/modellers/clst_admin/excludes"

# Retrieve the date_time
TODAY=$(date "+%y%m%d_%H%M")

# The path of the logs 
log_path="/home/modellers/clst_admin/logs/"

 
# This command rsync's files from the remote server to the local server.
# Flags:
#   -z enables gzip compression of the transport stream.
#   -e enables using ssh as the transport prototcol.
#   --rsync-path lets us pass the remote rsync command through sudo.
#   --archive preserves all file attributes and permissions.
#   --exclude-from points to our configuration of files and directories to skip.
#   --numeric-ids is needed if user ids don't match between the source and
#       destination servers.
#   --link-dest is a key flag. It tells the local rsync process that if the
#       file on the server is identical to the file in ../$YESTERDAY, instead
#       of transferring it create a hard link. You can use the "stat" command
#       on a file to determine the number of hard links. Note that when
#       calculating disk space, du includes disk space used for the first
#       instance of a linked file it encounters. To properly determine the disk
#       space used of a given backup, include both the backup and it's previous
#       backup in your du command.
#
#
#
# The "rsync" user is a special user on the remote server and client. 
# ON THE SERVER, the "rsync" user has permissions to run 
# a specific rsync command as sudo. 
# $sudo visudo
# 
# Add at the end " rsync   ALL=(ALL) NOPASSWD: /usr/bin/rsync "
#
# This is only required in a server to be backed up (e.g. iah372) or in a backup-server configuration (e.g. iah372backup).
# It is *NOT* required in a client configuration (e.g. iah530) that needs to be cloned from a server (e.g. iah372).
#
# Of course rsync@client needs to login passwordless to his account on the server. However, since it is root@client 
# who rsyncs through the rsync@server (the command will be `sudo rsync .... rsync@server`), we need to pass 
# a root@client RSA public key to rsync@server.
# To do this, simply create a password-less SSH key using root (sudo -i). 
# Then edit the file /root/.ssh/id_rsa.pub to represent rsync@client . Then add this public key 
# to the ./ssh/authorized_keys of the rsync@server.
# 
# In this way, the user "rsync" on the client can log to rsync@server through 'sudo', skipping the password.
# Actually, we achieve a 'root rsync' avoiding a full root ssh connection.


# Only run rsync if $SOURCE responds.                                                                                                         
VAR=`ping -s 1 -c 1 $SOURCE > /dev/null; echo $?`
if [ $VAR -eq 0 ]; then

    # copy the root tree (without the /home folder)
    #--dry-run (n)       # test

    rsync -azAXv -e "ssh" --rsync-path="$RSYNC" --exclude-from=$EXCLUDES --exclude 'home' --stats --progress --numeric-ids --force --ignore-errors --log-file=${log_path}/backup__$TODAY.log $USER@$SOURCE:/  /  

    # copy the /home folder separately creating a mirror backup of the data)
        ## Weird NOTE: it needs the option --ignore-errors to make the option --delete work !
        ## see: http://www.linuxquestions.org/questions/linux-networking-3/rsync-io-error-490030/
    #--dry-run (n)       # test

    rsync -auzAXv -e "ssh" --rsync-path="$RSYNC" --exclude-from=$EXCLUDES --stats --progress --numeric-ids --delete --force --ignore-errors --log-file=${log_path}/backup_home__$TODAY.log $USER@$SOURCE:/home/ /home/

    # changes the permissions so that only root can access these files
    chmod 600 ${log_path}/backup__${TODAY}.log ${log_path}/backup_home__${TODAY}.log


    # reload NFS services (if any) in the backup server (ignored in a client :) )
    exportfs -a
    service nfs-kernel-server reload

else
    echo "Cannot connect to $SOURCE."
fi
