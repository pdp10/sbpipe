#!/bin/bash

# start openlava on the cluster of computers specified in clst_list.txt
# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013


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
