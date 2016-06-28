# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $

# This script is a bash wrapper executing a matlab script as declared below


# The file containing the model configuration, usually in working_folder (e.g. model.conf)
model_configuration=$1



printf "\nReading file ${model_configuration} : \n"
# import the model configuration data (project, model-name, association-pattern)
old_IFS=$IFS
IFS=$'\n'
lines=($(cat ${model_configuration}))  # array
IFS=$old_IFS
printf "\n\n"


# The project name (e.g. "p3__mtor_foxo_ros")
project=""
# The work folder (e.g. working_folder)
work_folder=""

# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("project") 		echo "$line"; project="${array[1]}" ;; 
    ("work_folder") 		echo "$line"; work_folder="${array[1]}" ;;
  esac  
done
IFS=$old_IFS






# remove the path in case this was specified.
model_configuration=$(basename ${model_configuration})

model_configuration_with_path="${SB_PIPE}/${project}/${work_folder}/${model_configuration}"

model_configuration_with_path__matlab="'${model_configuration_with_path}'"




# Run command
# "-desktop" opens a matlab GUI ; "-r" passes a command to matlab (by command line).
matlab -desktop -r "try; SB_PIPE=getenv('SB_PIPE'); model_configuration=${model_configuration_with_path__matlab}; run([SB_PIPE,'/bin/sb_param_estim__pw/param_estim__pw_analyses_full_repository.m']); catch; end; "


