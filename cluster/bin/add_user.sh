#!/bin/bash

# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013

# Script to add a user to Linux system.
# NOTE: NIS, NIS+ or LDAP should be employed for proper users management.


# Input strings. Note: fullname must receive a 'list of strings' between single quotes.
username=$1
password=$2
uid=$3
fullname=$4
def_home=$5
def_shell=$6


echo "Adding new user: ${username}:x:${uid}:${uid}:${fullname}:${def_home}:${def_shell} to "; hostname; echo;


# Script to add a user to Linux system (only root can do this)
if [ $(id -u) -eq 0 ]; then

  egrep "^${username}" /etc/passwd >/dev/null
  if [ $? -eq 0 ]; then
    echo "${username} exists!"
    exit 1;
  fi

  egrep "^${uid}" /etc/passwd >/dev/null
  if [ $? -eq 0 ]; then
    echo "${uid} exists!"
    exit 2;
  fi

  pass=$(perl -e 'print crypt($ARGV[0], "password")' ${password})
  useradd -m -p ${pass} ${username}
  if [ $? -eq 0 ] ; then
    usermod -u ${uid} ${username}
    groupmod -g ${uid} ${username}
    #usermod -g ${uid} ${username}
    usermod -d ${def_home}/${username} ${username}
    usermod -s ${def_shell} ${username}
    mkdir -p ${def_home}/${username}
    chown ${username}:${username} ${def_home}/${username}
    chfn -f "${fullname}" ${username}
    # remove automatically created home folder
    rm -rf /home/${username}
    echo "User has been added to the system!"
  else
    echo "Failed to add a user!"
    exit 3
  fi

fi

