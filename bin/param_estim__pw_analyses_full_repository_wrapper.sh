
# Piero Dalle Pezze (2013)

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
matlab -desktop -r "try; SB_PIPE=getenv('SB_PIPE'); model_configuration=${model_configuration_with_path__matlab}; run([SB_PIPE,'/bin/param_estim__pw_analyses_full_repository.m']); catch; end; "


