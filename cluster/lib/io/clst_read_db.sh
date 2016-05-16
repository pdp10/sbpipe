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



# It returns a specified component (hostnames,ips,macs) of a database string.
# Input: database string in the format: hostnames,ips,macs 
#        component name
function get_comp()
{
  declare -a database=("${!1}")
  local list=$2 # accepts "hosts", "ips", "mac"
  local array=()
  OIFS="$IFS"
  # NOTE: IFS wants a single char. It does not work with '/?/'
  IFS=$','
  array=(${database[@]})
  IFS="$OIFS"
  case "${list}" in
    ("hosts") 	echo "${array[0]}" ;; 
    ("ips") 	echo "${array[1]}" ;; 
    ("mac") 	echo "${array[2]}" ;; 
    (*) echo "WARNING: found unknown entry!" ;;
  esac
}
 


# It retrieves the administrator name.
# Input: A file containing the administrator name
function get_admin()
{
  local filename=$1
  local admin=""
  while read -r line
  do
     admin="$line"
  done < ${filename}
  echo "$admin"
}



# It retrieves the full list of hosts in a database string in the format hostnames, ips, macs
# Input: A file in the format hostname, ip, mac EOL
function get_list_hosts()
{
  local filename=$1  
  local hosts=()
  local ips=()
  local mac=()
  local line=""
  local array=()
  OIFS="$IFS"
  IFS=$',' 
  while read -r line
  do
    array=($line)
    hosts+=(${array[0]})
    ips+=(${array[1]})
    mac+=(${array[2]})
  done < ${filename}
  IFS="$OIFS"
  # return with a comma delimiter
  echo "${hosts[@]},${ips[@]},${mac[@]}"
}



# It retrieves a list of hosts in a database string in the format hostnames, ips, macs
# without excluded hosts.
# Input: A file in the format hostname, ip, mac EOL
#        An array of hostnames
#        An array of ip addresses
#        An array of mac addresses
function exclude_hosts()
{ 
  local filename=$1  
  declare -a hosts=("${!2}")
  declare -a ips=("${!3}")
  declare -a mac=("${!4}")
  local line=""
  local array=()
  local exclude_hosts=()
  local exclude_ips=()
  local exclude_mac=()
  OIFS="$IFS"
  IFS=$','   
  # it retrieves the excluded hosts
  while read -r line
  do
    array=($line)
    exclude_hosts+=(${array[0]})
    exclude_ips+=(${array[1]})
    exclude_mac+=(${array[2]})
  done < ${filename}
  IFS="$OIFS"

  for (( i=0; i < ${#exclude_hosts[@]}; i++ ))
  do
    declare -a hosts=( ${hosts[@]/${exclude_hosts[i]}/} )
    declare -a ips=( ${ips[@]/${exclude_ips[i]}/} )
    declare -a mac=( ${mac[@]/${exclude_mac[i]}/} )
  done
  # it returns new host after exclusion
  echo "${hosts[@]},${ips[@]},${mac[@]}"
}



# It attaches the admin name to the hosts and returns 
# an array in the format user@host(s). 
# Input: A user name
#        An array of hostnames
function bind_user_host()
{
  local user=${1}
  declare -a hosts=("${!2}")
  for (( i=0; $i < ${#hosts[@]}; i++ ))
  do
    hosts[$i]=${user}@${hosts[$i]}
  done
  echo "${hosts[@]}"
}



# It exports the following functions (is this really required?? TO CHECK)
export -f get_comp
export -f get_admin
export -f get_list_hosts
export -f exclude_hosts
export -f bind_user_host
