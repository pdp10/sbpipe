% Piero Dalle Pezze (2013)
%
% This script combines the repositories multiple fits sequences in order to compact 
% the results of a parallel parameter estimation.


%  % the 'finalised' model
%  model='mtor_foxo_ros_model_v24_mixed_pop_pw3';
%  % model-data dataset
%  dataset='mtor_foxo_ros_dataset_mixed_pop_v24_combined2';
%  % the job folder
%  folder_pattern='fitseq';
%  % number of jobs executed
%  % THIS IS A LIMIT FOR MATLAB/PottersWheelToolbox . It is impossible to 
%  % save/load a pw-repository bigger than 40,000 fits.
%  njobs=40;            
%  
%  % the folder containing the merged repository
%  summary_folder=[model,'_all_fits'];
%  % the configuration file
%  configuration_file='pwConfigurationFile.mat';



PROJ_DIR=getenv('PROJ_DIR');


% PottersWheelToolbox path
path_pw='/opt/IAH_MATLAB_TOOLBOXES/';
%path_pw='~/Documents/MATLAB/';

% Add PottersWheelToolbox path
addpath([path_pw, 'PottersWheelToolbox']);
addpath([path_pw, 'PottersWheelToolbox/']);
addpath([path_pw, 'PottersWheelToolbox/PlugIns/MOTA']);
addpath([path_pw, 'PottersWheelToolbox/PlugIns/PLE']);
% Add sundials-2.4.0 path
addpath([path_pw, 'sundials-2.4.0/sundialsTB/sundialsTB']);
addpath([path_pw, 'sundials-2.4.0/sundialsTB/sundialsTB/cvodes']);
addpath([path_pw, 'sundials-2.4.0/sundialsTB/sundialsTB/cvodes/cvm']);
addpath([path_pw, 'sundials-2.4.0/sundialsTB/sundialsTB/cvodes/examples_ser']);
addpath([path_pw, 'sundials-2.4.0/sundialsTB/sundialsTB/cvodes/function_types']);
addpath([path_pw, 'sundials-2.4.0/sundialsTB/sundialsTB/nvector']);

pwClear;
warning('off', 'MATLAB:oldPfileVersion');
warning('off','all'); % turn all warnings off


[model_path,model_noext,model_ext]=fileparts(model);
[dataset_path,dataset_noext,dataset_ext]=fileparts(dataset);

mkdir([workdir, '/', summary_folder]);
% copy the association and configuration files 
copyfile([workdir, '/', dataset_noext, '*.mat'], [workdir, '/', summary_folder]);
copyfile([workdir, '/', configuration_file], [workdir, '/', summary_folder]);
delete([workdir, '/', summary_folder, '/', model, '_full_repository.mat']) 

% prevents Matlab from storing temp files in PROJ_DIR/bin/
cd(workdir);


% Load the complete repository from the first job folder. (first time)
if njobs > 1
  pwLoadRepository([workdir, '/', folder_pattern, '1/', model_noext, '_repository.mat'], false);
end
% Append fit history of repository (also used for merging repositories) (afterwards)
for jb = 2:njobs
  pwAppendFitHistoryOfRepository([workdir, '/', folder_pattern, num2str(jb), '/', model_noext, '_repository.mat']);
end


% Save the matlab repository inclusive of all the fits sequence groups.
pwSaveRepository([workdir, '/', summary_folder,'/', model_noext, '_full_repository.mat'],false);

