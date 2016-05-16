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

# exec a command in cluster of computers specified in clst_list.txt
#note that 
# <<'EOF'
#$PASS
#EOF
#"
# MUST NOT HAVE ANY CHARACTER at the end of EACH STRING. NEWLINE IS MANDATORY


# This script allows the administrator to send a sudo command to each node of the cluster


#MY_DIR=`dirname $0`
. ${CLST_LIB}/io/clst_read_db.sh


# # # Retrieve the admin name
admin=`get_admin "${CLST_DIR}/etc/db/admin"`

# Retrieve the full list of hosts
db=`get_list_hosts "${CLST_DIR}/etc/db/clst_db_nodes"`
hosts=(`get_comp db[@] "hosts"`)
ips=(`get_comp db[@] "ips"`)
mac=(`get_comp db[@] "mac"`)

# Exclude the following nodes
clean_db=`exclude_hosts "${CLST_DIR}/etc/db/clst_excl_nodes" hosts[@] ips[@] mac[@]`
hosts=(`get_comp clean_db[@] "hosts"`)
ips=(`get_comp clean_db[@] "ips"`)
mac=(`get_comp clean_db[@] "mac"`)

# Attach the admin name to the host.
hosts=(`bind_user_host $admin hosts[@]`)




# Does not execute commands on owner machines
echo; echo -n "HOSTS: ${hosts[@]}"; echo; echo;
echo -n "List the host names to be excluded (e.g. iah522.ncl.ac.uk): "; read -r excl_hosts; echo;
excl_hosts=(${excl_hosts});
for excl_host in ${excl_hosts[@]}
do
  declare -a hosts=( ${hosts[@]/"${admin}@${excl_host}"/} )
done


echo; echo -n "HOSTS: ${hosts[@]}"; echo; echo;
echo -n "Enter the sudo command to execute: "; read -r EXEC; echo; 
echo -n "Do you want to inform every logged users [yY/nN]: "; read -r WALL; echo;
echo -n "Enter cluster password: "; read -r -s PASS; echo; 



# send 3 warning messages to all logged users.
# 2>&- is required for avoiding "cannot get tty name: Invalid argument linux"
if [ ${WALL} = "y" -o ${WALL} = "Y" ]; then

  for ((i=${#hosts[*]}-1 ; $i >=0 ; i-- )); 
  do
      eval ping -c 3 ${ips[i]}
      if [ "$?" == "0" ]; then
	ssh ${hosts[$i]} "wall <<< ' This machine will shut down within 5 minute! 
Please, save your data and logout! ' "
      fi
  done

  
  sleep 4m

  
  
  for ((i=${#hosts[*]}-1 ; $i >=0 ; i-- )); 
  do
      eval ping -c 3 ${ips[i]}
      if [ "$?" == "0" ]; then
	ssh ${hosts[$i]} "wall <<< 'Last call!!!!!!
This machine is shutting down within 1 minute!!!!
Please, save your data and logout!!!!!!'  "
      fi
  done
  
  
  sleep 55s

  
  
  for ((i=${#hosts[*]}-1 ; $i >=0 ; i-- )); 
  do
      eval ping -c 3 ${ips[i]}
      if [ "$?" == "0" ]; then
	ssh ${hosts[$i]} "wall <<< 'By-ye !!! :-)' "
      fi
  done
  
  
  sleep 5s

  
fi




# apply the command: first the clients, then the server. 
for ((i=${#hosts[*]}-1 ; $i >=0 ; i-- )); 
do 
    eval ping -c 3 ${ips[i]}
    if [ "$?" == "0" ]; then
      echo;
      echo -n "${hosts[$i]}";echo;
      ssh -t -t -t ${hosts[$i]} "sudo -S $EXEC << 'EOF'
$PASS
EOF
"
    else
      echo "---- COULD NOT CONNECT TO ${hosts[$i]} ----"
    fi
done


