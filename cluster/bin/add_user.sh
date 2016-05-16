#!/bin/bash
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $


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

