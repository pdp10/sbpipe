#!/bin/bash

# update cluster of computers specified in clst_list.txt
# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013



#note that 
# <<EOF
#$PASS
#EOF
#"
# MUST NOT HAVE ANY CHARACTER at the end of EACH STRING. NEWLINE IS MANDATORY



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



# iah-huygens was intentionally discarded due to issue related to the previosu ATI graphic card
# which were solved after taking and installing iah372 nvidia graphic card.
#declare -a hosts=( ${hosts[@]/"${admin}@iah-huygens.ncl.ac.uk"/} )




echo ""
echo "#############################################"
echo "##############  UPDATE CLUSTER  #############"
echo "#############################################"

echo -n "HOSTS: ${hosts[@]}"; echo; echo;
echo -n "Enter cluster password: "; read -r -s PASS; echo; 


for (( i=0; i < ${#hosts[@]}; i++ ))
do

    echo "#############################################"
    echo "...processing node: ${hosts[i]}"
    echo "#############################################"

    eval ping -c 3 ${ips[i]}
    # if pings are not returned/forbidden, then check for individual services (e.g. ssh --> port 22) through nmap
    #eval nmap ${hosts[i]} -p 22 --max-retries 10 | grep -q open
    if [ "$?" == "0" ]; then

      ssh -t -t -t ${hosts[i]} "sudo -S apt-get update << 'EOF'
$PASS
EOF
"
      ssh -t -t -t ${hosts[i]} "sudo -S apt-get -y upgrade << 'EOF'
$PASS
EOF
"

    else
      echo "---- COULD NOT CONNECT TO ${hosts[i]} ----"
    fi
done