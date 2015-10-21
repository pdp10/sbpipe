
% Piero Dalle Pezze (2013)
% executes the matlab script 'param_estim__pw_analyses_full_repository_proc.m' after 
% combining a list of fits sequences of parallel parameter estimation


% The file containing the model configuration, usually in working_folder (e.g. model.conf)
% model_configuration


% import the model configuration data (project, model-name, association-pattern)
%# read the whole file to a temporary cell array
fid = fopen(model_configuration,'rt');
values = textscan(fid,'%s%s','Delimiter','=');
fclose(fid);



% the project of reference
project='';
% the 'finalised' model
model='';
% The folder cluster suffix (e.g. _cluster)
folder_pattern_suffix='';
% The summary folder suffix (e.g. _all_fits)      
summary_folder_suffix='';
% The work folder (e.g. working_folder)
work_folder='';
% The optimisation algorithm (e.g. 2  -- TrustRegion)
optim_algo=0;
% The number of fits in a sequence (e.g. 500)
nfits=0;
% The noise to be applied for each fit in the fits sequence (e.g. 0.4)
noise=0.1;
% The prefix of the file containing the diary of the analyses (e.g. data_collection_)
analyses_diary_prefix='';
% Export the fitted model in pw and SBML (e.g. false)
param_estim__pw_export_model='false';
% Execute the task pw Info (e.g. false)
param_estim__pw_info='false';
% shows the odes (e.g. false)
param_estim__pw_showode='false';
% shows the graph (e.g. false)
param_estim__pw_showgraph='false';
% shows the fitting plots (e.g. false)
param_estim__pw_draw='false';
% Execute linear fits sequence analysis (e.g. false)
param_estim__pw_fitseq_linear_analysis='false';

% configure the percentage of the best fits for history retrieval (e.g. 100)
param_estim__pw_history__percentageBestFits=100;
% configure the minimum pvalue for this filter (e.g. 0)
param_estim__pw_history__minimumPValue=0;
% configure the percentage of outliers for this filter (e.g. 100)
param_estim__pw_history__percentageIncludedOutliers=100;

% configure the percentage of the best fits for this filter (e.g. 50)
param_estim__pw_filter__percentageBestFits=10;
% configure the minimum pvalue for this filter (e.g. 0)
param_estim__pw_filter__minimumPValue=0;
% configure the percentage of outliers for this filter (e.g. 100)
param_estim__pw_filter__percentageOutliers=100;
% Execute the task pw MOTA (e.g. false)
param_estim__pw_mota='false';
% Set the parameter for pw MOTA (e.g. 5)
param_estim__pw_mota__maxNumberOfParameters=5;
% The output file for MOTA analysis (e.g. mota.txt)
param_estim__pw_mota__outputfile_prefix='';
% Compute the confidence intervals (e.g. false)
param_estim__pw_confidenceIntervals='false';
% Method used for computing the confidence intervals (e.g. 2 (Monte-Carlo))
param_estim__pw_confidenceIntervals__mode=2;
% Number of fits used by the method to compute the confidence intervals (e.g. 100)
param_estim__pw_confidenceInterval__nfits=100;
% Execute the task pw PLE (e.g. false)
param_estim__pw_ple='false';



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
    case 'folder_pattern_suffix'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        folder_pattern_suffix=values{2}{rowIdx};          
    case 'summary_folder_suffix'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        summary_folder_suffix=values{2}{rowIdx}; 
    case 'work_folder'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        work_folder=values{2}{rowIdx};
    case 'optim_algo'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        optim_algo=str2num(values{2}{rowIdx}); 
    case 'nfits'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        nfits=str2num(values{2}{rowIdx});  
    case 'noise'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);
        noise=str2num(values{2}{rowIdx}); 
    case 'analyses_diary_prefix'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        analyses_diary_prefix=values{2}{rowIdx}; 
    case 'param_estim__pw_export_model'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_export_model=values{2}{rowIdx}; 
    case 'param_estim__pw_info'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_info=values{2}{rowIdx};        
    case 'param_estim__pw_showode'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_showode=values{2}{rowIdx};
    case 'param_estim__pw_showgraph'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_showgraph=values{2}{rowIdx};       
    case 'param_estim__pw_draw'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_draw=values{2}{rowIdx};  
    case 'param_estim__pw_fitseq_linear_analysis'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_fitseq_linear_analysis=values{2}{rowIdx};         
    case 'param_estim__pw_history__percentageBestFits'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_history__percentageBestFits=str2num(values{2}{rowIdx});
    case 'param_estim__pw_history__minimumPValue'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_history__minimumPValue=str2num(values{2}{rowIdx});                   
    case 'param_estim__pw_history__percentageIncludedOutliers'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_history__percentageIncludedOutliers=str2num(values{2}{rowIdx}); 
    case 'param_estim__pw_filter__percentageBestFits'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_filter__percentageBestFits=str2num(values{2}{rowIdx}); 
    case 'param_estim__pw_filter__minimumPValue'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_filter__minimumPValue=str2num(values{2}{rowIdx}); 
    case 'param_estim__pw_filter__percentageOutliers'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_filter__percentageOutliers=str2num(values{2}{rowIdx}); 
    case 'param_estim__pw_mota'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_mota=values{2}{rowIdx};
    case 'param_estim__pw_mota__maxNumberOfParameters'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_mota__maxNumberOfParameters=str2num(values{2}{rowIdx});
    case 'param_estim__pw_mota__outputfile_prefix'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_mota__outputfile_prefix=values{2}{rowIdx};   
    case 'param_estim__pw_confidenceIntervals'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_confidenceIntervals=values{2}{rowIdx};  
    case 'param_estim__pw_confidenceIntervals__mode'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_confidenceIntervals__mode=str2num(values{2}{rowIdx}); 
    case 'param_estim__pw_confidenceInterval__nfits'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_confidenceInterval__nfits=str2num(values{2}{rowIdx});
    case 'param_estim__pw_ple'
        fprintf([values{1}{rowIdx},'=',values{2}{rowIdx},'\n']);    
        param_estim__pw_ple=values{2}{rowIdx};   
  end    
end
fprintf('\n\n');






PROJ_DIR=getenv('PROJ_DIR');

% Generate a timestamp
format shortg;
now=fix(clock);
timestamp=[num2str(now(1)),num2str(now(2)),num2str(now(3)),'_',num2str(now(4)),num2str(now(5))];

% the local working directory
% the dir containing the parameter estimation output
workdir=[PROJ_DIR,'/',project,'/',work_folder];


[model_path,model_noext,model_ext]=fileparts(model);
% the folder containing the merged repository
summary_folder=[model_noext, summary_folder_suffix]
% The file containing the diary of the analyses
analyses_diary=[analyses_diary_prefix, model_noext, '_', timestamp, '.txt']
% Mota output file
param_estim__pw_mota__outputfile=[param_estim__pw_mota__outputfile_prefix, model_noext, '.txt']




% Switch the diary on
diary([workdir, '/', summary_folder, '/', analyses_diary]);
run([PROJ_DIR, '/bin/param_estim__pw_analyses_full_repository_proc.m'])
fprintf('\nEnd script (diary closed)\n')
% Switch the diary off
diary off;

