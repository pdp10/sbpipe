% License (GPLv3):
% This program is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation; either version 2 of the License, or (at
% your option) any later version.
%
% This program is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program; if not, write to the Free Software
% Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
%
%
% $Revision: 1.0 $
% $Author: Piero Dalle Pezze $
% $Date: 2013-04-20 12:14:32 $
%
%
%clear
%clc



% PottersWheelToolbox path
path_pw='/opt/IAH_MATLAB_TOOLBOXES/';
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



cd([workdir, '/', summary_folder]);

%pwLoadConfigFromMatFile('pwConfigurationFile.mat');
config = pwGetConfig;
config.general.showAdvancedItems = true;
config.analyses.linearFitSequenceAnalysis.nMaxSubplotsCorrelatedPars = 100;
config.analyses.linearFitSequenceAnalysis.nMaxFitsForDendogram = 100;
config.analyses.fitSequence.disturbanceStrength = noise;
config.integration.integrator = 14;
config.integration.calcJacobian = true;
config.integration.useJacobian = true;
config.optimization.method = optim_algo; %TR
config.optimization.fitInLogParameterSpace = true;
config.optimization.calcJacobian = true;
config.optimization.useJacobian = true;
%config.optimization.useJacobian = false;

config.integration.calcSensitivities = true;
%config.plotting.showA             = true;
config.plotting.showU             = true;
config.plotting.showX             = true;
config.plotting.showY             = true;
config.plotting.savePNG           = true;
config.plotting.savePNGsmall      = false;
config.plotting.saveFIG           = true;
config.analyses.PLE.thresholdMode = 3;  % 1 or 2  = separate CI
config.general.commandLineVerbosity = 1;
pwSetConfig(config);




[model_path,model_noext,model_ext]=fileparts(model);


% Load the full repository containing the merged session of parameter estimation
fprintf('Loading model repository:\n')
rep_loaded=pwLoadRepository([model_noext, '_full_repository.mat'], false)



% pwEqualizer;

% Close the windows: necessary, otherwise it locks the script at this point
pwCloseEqualizer
pwCloseMainGUI




if strcmp(param_estim__pw_export_model,'true')
  fprintf('Export fitted model:\n')
  pwSaveModel([], [model_noext, '_fitted_', timestamp, '.m'], [], 'true')
  pwSaveParametersIntoModelFile('false', 'false', [model_noext, '_fitted_', timestamp, '.m']);  
  fprintf('Export model in SBML format:\n')
  pwAddModel([model_noext, '_fitted_', timestamp, '.m'])
  pwExportCouplesToSBML([]);
end



if strcmp(param_estim__pw_showode,'true')
  fprintf('Listing model ODE:\n')
  pwShowODE
end



if strcmp(param_estim__pw_showgraph,'true')
  fprintf('Plotting model graph:\n')
  pwShowGraphAsPNG
end



if strcmp(param_estim__pw_draw,'true')
  fprintf('Plotting model fitting diagrams:\n')
  pwDraw
  pwSaveAllOpenFigures;
  pwCloseFigures;
end



if strcmp(param_estim__pw_info,'true')
  fprintf('Plotting model information:\n')
  pwInfo
  pwInfoPlotsFitting
  pwSaveAllOpenFigures;
  pwCloseFigures;
end



% Merges the fits sequences (necessary for linear sequence analysis and MOTA, since we have more than one fits sequence)
pwFitHistoryMergeFitSequences


if strcmp(param_estim__pw_fitseq_linear_analysis,'true')
  fprintf('Executing linear sequence analysis:\n')
  [fits] = pwFitHistoryGetFits([], [], [], param_estim__pw_history__percentageBestFits, param_estim__pw_history__minimumPValue, param_estim__pw_history__percentageIncludedOutliers);
  pwFitSequenceAnalysis(param_estim__pw_filter__percentageBestFits, param_estim__pw_filter__minimumPValue, false, fits, param_estim__pw_filter__percentageOutliers);  
  pwSaveAllOpenFigures;
  pwCloseFigures;  
end



if strcmp(param_estim__pw_mota,'true')
  fprintf('Executing MOTA non-linear analysis:\n')
  [fits] = pwFitHistoryGetFits([], [], [], param_estim__pw_filter__percentageBestFits, param_estim__pw_filter__minimumPValue, param_estim__pw_filter__percentageOutliers);
  pwMota(fits, [], true, param_estim__pw_mota__maxNumberOfParameters)
  pwPlugInMOTASaveResult(param_estim__pw_mota__outputfile)
  pwSaveAllOpenFigures;
  pwCloseFigures;
end



if strcmp(param_estim__pw_confidenceIntervals,'true')
  fprintf('Compute the confidence intervals:\n')
  pwConfidenceIntervals(param_estim__pw_confidenceIntervals__mode, [], param_estim__pw_confidenceInterval__nfits)
  pwSaveAllOpenFigures;
  pwCloseFigures;  
end



if strcmp(param_estim__pw_ple,'true')
  fprintf('Executing PLE analysis:\n')
  pwPleInit(false);
  
%   arguments to pwPleCalculate(i, a, b, c, d, e) are:
%   iPar                  i-th parameter, see pwInfo
%                         [if omitted, all free parameters are considered]
%   maxNumSteps           maximum number of steps to sample the profile likelihood
%                         Default: 100
%   relChi2StepIncrease:  percentage chi^2 increase of a step [0.1]
%   maxStepSize:          maximum step size as log10 change
%   minStepSize:          minimum step size as log10 change
%   breakOnParLimits:     stop if a parameter bound has been reached  [true]
%   showIterations        If true, the progress of the PL estimation is visualized
%                         Default as specified in config.analyses.PLE.showIterations, usually true
%   thresholdMode         1: Use relative chi-square threshold for simultaneous confidence level
%                         2: Use relative chi-square threshold for separate confidence levels
%                         3: Use absolute chi-square threshold based on chi-square test
%                         Default as specified in config.analyses.PLE.thresholdMode, usually 1
%   fitBeforePLE          Default given by config.analyses.PLE.fitBeforePLE
%   hSubplot              Handle to a subplot which will be used to plot
%                         the currently estimated profile likelihood.
%   showLegend            If true, a legend is shown. Default: true
  pwPleCalculate([], 100, 0.1, 0.1, 0.01, 'true', 3, 'false', [], 'true'); 
  
%    pwPle;
  pwPlePrint;
%  pwPlePlot(i)
  pwPlePlotMulti;
  %pwPlePlotRelations([2 4]);
  %pwSetPlottingState('x', true);
  pwPleTrajectories;
  %pwDraw
  pwSaveAllOpenFigures;
  pwCloseFigures;   
end












% rename the folder Plots adding a timestamp
movefile('Plots', ['Plots_', timestamp])


