
% Piero Dalle Pezze (2013)
% executes the matlab script 'param_estim__pw_combine_fitseqs_proc.m' after 
% a parallel parameter estimation


% The file containing the model configuration, usually in working_folder (e.g. model.conf)



% import the model configuration data (project, model-name, association-pattern)
%# read the whole file to a temporary cell array
fid = fopen(model_configuration,'rt');
values = textscan(fid,'%s%s','Delimiter','=');
fclose(fid);




% the project of reference
project='';
% the 'finalised' model
model='';
% model-data dataset
dataset='';
% Matlab configuration file (e.g. pwConfigurationFile.mat)
configuration_file='';
% The number of jobs to be executed
% THIS IS A LIMIT FOR MATLAB/PottersWheelToolbox . It is impossible to 
% save/load a pw-repository bigger than 40,000 fits. (e.g. 40)
njobs=0;
% Job name (e.g. fitseq)
job_name='';
% The folder cluster suffix (e.g. _cluster)
folder_pattern_suffix='';
% The summary folder suffix (e.g. _all_fits)
summary_folder_suffix='';
% The work folder (e.g. working_folder)
work_folder='';



fprintf(['Reading file ', model_configuration, ':\n']);
nRows = size(values{1},1);

for rowIdx = 1:nRows;
  switch values{1}{rowIdx}
    case 'project'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);
        project=values{2}{rowIdx};
    case 'model'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        model=values{2}{rowIdx};
    case 'dataset'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        dataset=values{2}{rowIdx};
    case 'configuration_file'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        configuration_file=values{2}{rowIdx};
    case 'njobs'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);
        njobs=str2num(values{2}{rowIdx});
    case 'job_name'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        job_name=values{2}{rowIdx}; 
    case 'folder_pattern_suffix'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        folder_pattern_suffix=values{2}{rowIdx};  
    case 'summary_folder_suffix'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        summary_folder_suffix=values{2}{rowIdx}; 
    case 'work_folder'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        work_folder=values{2}{rowIdx};    
  end    
end
fprintf('\n\n');



PROJ_DIR=getenv('PROJ_DIR');

% the local working directory
% the dir containing the parameter estimation output
workdir=[PROJ_DIR,'/',project,'/',work_folder];


[model_path,model_noext,model_ext]=fileparts(model);
[job_path,job_noext,job_ext]=fileparts(job_name);


% the folder pattern
folder_pattern=[model_noext, folder_pattern_suffix, '/', job_noext];
% the folder containing the merged repository
summary_folder=[model_noext, summary_folder_suffix];



run([PROJ_DIR, '/bin/param_estim__pw_combine_fitseqs_proc.m']);



