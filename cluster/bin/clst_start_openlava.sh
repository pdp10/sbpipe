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


# start openlava on the cluster of computers specified in clst_list.txt



config=$1


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



#hosts=('npdp2@iah522.ncl.ac.uk')



openlava="openlava-2.2"
install_path="/usr/local"



echo ""
echo "#############################################"
echo "##########  STARTING OPENLAVA  ##############"
echo "#############################################"

echo -n "HOSTS: ${hosts[@]}"; echo; echo;
echo -n "Enter cluster password: "; read -r -s PASS; echo; 






# on the masterhosts
if [ "${config}" == "--config" ]; then
  # only the iah372, iah372backup, iah522, iah502    (they have their own home folders)
  # select only the first three elements.
  for (( i=0; i < 4; i++ ))
  do
  
    echo ""
    echo "#############################################"
    echo "copying configuration to node: ${hosts[i]}"
    echo "#############################################"  

    eval ping -c 3 ${ips[i]}
    # if pings are not returned/forbidden, then check for individual services (e.g. ssh --> port 22) through nmap
    #eval nmap $host -p 22 --max-retries 10 | grep -q open
    if [ "$?" == "0" ]; then
      echo ""
      echo "Transfer lsf.cluster.openlava file on ${hosts[i]}"
      ssh ${hosts[i]} "mkdir -p ~/lsf_config"
      scp ${CLST_DIR}/etc/openlava/lsf_config/* ${hosts[i]}:~/lsf_config/
    else 
      echo "---- COULD NOT CONNECT TO ${hosts[i]} ----"
      if [ "$i" == "0" ]; then
       echo "Connection to cluster master node failed. This script is terminated."
       exit 1
      fi      
    fi    
  done
fi


echo $hosts


for (( i=0; i < ${#hosts[@]}; i++ ))
do


    echo ""
    echo "#############################################"
    echo "starting openlava on node: ${hosts[i]}"
    echo "#############################################"

    eval ping -c 3 ${ips[i]}
    # if pings are not returned/forbidden, then check for individual services (e.g. ssh --> port 22) through nmap
    #eval nmap $host -p 22 --max-retries 10 | grep -q open
    if [ "$?" == "0" ]; then

      if [ "${config}" == "--config" ]; then
	echo ""
	echo "Transfer lsf.cluster.openlava file on ${hosts[i]}"
	ssh -t -t -t ${hosts[i]} "sudo -S cp ~/lsf_config/* ${install_path}/${openlava}/etc/ <<'EOF'
$PASS
EOF
"
      fi



      echo "Starting openlava service on ${hosts[i]}"
      ssh -t -t -t ${hosts[i]} "sudo -S sh /etc/profile.d/openlava stop <<'EOF'
$PASS
EOF
"  
      ssh -t -t -t ${hosts[i]} "sudo -S service openlava restart <<'EOF'
$PASS
EOF
"
 

    else
      echo "---- COULD NOT CONNECT TO ${hosts[i]} ----"
    fi
done
