clear
clc

pwClear;
config = pwGetConfig;
config.integration.integrator = 14;
config.integration.calcJacobian = true;
config.integration.useJacobian = true;
config.optimization.method = 2;
config.optimization.fitInLogParameterSpace = true;
config.optimization.calcJacobian = true;
config.optimization.useJacobian = true;
config.integration.calcSensitivities = true;
pwSetConfig(config);


all=false;


pwAddModel('../Models/insulin_receptor.m');

% Time-courses dataset
pwSelect([1]);
pwAddData('../Data/insulin_dataset_scaled.xls');

pwSelect('all');
pwCombine;
pwCloseFigures;
pwDraw;
pwCloseFigures
pwEqualizer;



%  Distributed parameter estimation (as required up to v.2): 
%  http://www.potterswheel.de/Pages/API/pwTutorial_Using_the_Parallel_Computing_Toolbox.html#Synopsis
%sched = findResource('scheduler','type','local')
%job = createJob(sched)
%  %%% pwF2(n, strength, backupMinutes, dataMode, tMax, job, nNodes, randnState)
%pwF2(1000, 1.0, [], [], [], job, 4)  

%pwDraw;
%pwSaveFigures;
%pwCloseFigures;

%pwInfo
%pwSaveFigures;
%pwCloseFigures;

% MOTA
%pwPlugInMOTASaveResult(filename)



%pwPLEInit(false);
%pwPLEInit;
%pwPLE;
%pwPLEPrint;
%pwPLEPlotMulti;
%pwPLEPlotRelations([2 4]);
%pwSetPlottingState('x', true);
%pwPLETrajectories(2);

