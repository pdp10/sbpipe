
SB_PIPE
=

Authors
=== 
Piero Dalle Pezze



Introduction
===
This package offers a collection of pipelines for parameter estimation, single parameter perturbation, double parameter perturbation, and sensitivity analysis.



Environment Variables:
===
export SB_PIPE=/path/to/SB_pipe
export SB_PIPE_LIB=${SB_PIPE}/lib
export PATH=$PATH:${SB_PIPE}/bin



Requirements
===
Bash (script management)
R (plot generation), gplots, abind
Python (report generation)
Latex (for report generation)
Matlab with Potterswheel (for parameter estimation)
Copasi (model simulation) - remember to tick the execution check box on the task to run



TODO:
===
* Specify the x axis label in the configuration file.
* Add a pipeline for parameter estimation using another software (e.g. ABC-sysbio ?). If this is done using Copasi, a way to assess parameter non-identifiability must be implemented likely using Copasi->ParameterScan
* In the future, it would be nice to convert the full package written in Python / Latex and generate the plots with matplotlib. This would be easier to maintain.




Example of Configuration file (this might undergo some changes):
user=npdp
hosts=iah372.ncl.ac.uk
team=glyn                     <<---- this must be replaced with the x axis
project=p3__mtor_mito_ros     <<---- this must be replaced with the full path 
model=mtor_mito_ros_model_v3_4_pw3.m  <<---- start config for param estimation using pw 
dataset=mtor_mito_ros_model_v3_4_pw3_dataset_10times.xls
setup_file=setup_param_estim__pw_paral.m
configuration_file=pwConfigurationFile.mat
folder_pattern_suffix=_cluster
summary_folder_suffix=_all_fits
tarball_suffix=_fitseqs_paral_comput_round
work_folder=working_folder
remote_work_folder=working_folder
models_folder=Models
remote_models_folder=Models
data_folder=Data
remote_data_folder=Data               
optim_algo=2                             
nfits=500
noise=0.4
njobs=40
job_name=fitseq.job
analyses_diary_prefix=data_collection_
param_estim__pw_export_model=true
param_estim__pw_showode=true
param_estim__pw_showgraph=true
param_estim__pw_draw=true
param_estim__pw_info=true
param_estim__pw_fitseq_linear_analysis=true
param_estim__pw_mota=true
param_estim__pw_confidenceIntervals=false
param_estim__pw_ple=false
param_estim__pw_history__percentageBestFits=100
param_estim__pw_history__minimumPValue=0
param_estim__pw_history__percentageIncludedOutliers=100
param_estim__pw_filter__percentageBestFits=30
param_estim__pw_filter__minimumPValue=0
param_estim__pw_filter__percentageOutliers=100
param_estim__pw_mota__maxNumberOfParameters=5
param_estim__pw_mota__outputfile_prefix=mota_results_
param_estim__pw_confidenceIntervals__mode=2
param_estim__pw_confidenceInterval__nfits=30        <<---- end config for param estimation using pw
simulations_folder=simulations                      <<---- start config for sim using copasi
remote_simulations_folder=simulations
tmp_folder=tmp
remote_tmp_folder=tmp
dataset_parameter_scan_dir=dataset_parameter_scan
tc_parameter_scan_dir=tc_parameter_scan
dataset_simulation_dir=dataset
dataset_short_simulation_dir=dataset_short
double_perturb_dir=double_perturb
tc_dir=tc
tc_mean_dir=tc_mean
tc_mean_with_exp_dir=tc_mean_with_exp
simulate__copasi_model=mtor_mito_ros_model_v3_4_copasi.cps
simulate__model_simulations_number=5
simulate__duration=50
simulate__interval_size=0.01
simulate__prefix_results_filename=report_simulation__
simulate__prefix_stats_filename=stats_simulation__
simulate__prefix_exp_stats_filename=stats_experiments__
param_scan__single_perturb_copasi_models_list=mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_Akt_inhibitor.cps mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_JNK_inhibitor.cps mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_mTORC1_inhibitor.cps mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_mTOR_inhibitor.cps mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_DNA_damage_inhibitor.cps mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_CDKN1A_inhibitor.cps mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_Mito_mass_inhibitor.cps mtor_mito_ros_model_v3_4_copasi_scan_ext_interv_ROS_inhibitor.cps
param_scan__single_perturb_species_list=ext_interv_Akt_inhibitor ext_interv_JNK_inhibitor ext_interv_mTORC1_inhibitor ext_interv_mTOR_inhibitor ext_interv_DNA_damage_inhibitor ext_interv_CDKN1A_inhibitor ext_interv_Mito_mass_inhibitor ext_interv_ROS_inhibitor
param_scan__single_perturb_legend=param_scan__single_perturb_legend
param_scan__single_perturb_knock_down_only=true
param_scan__single_perturb_perturbation_in_percent_levels=false
param_scan__single_perturb_levels_number=10
param_scan__single_perturb_min_inhibition_level=10
param_scan__single_perturb_max_overexpression_level=250
param_scan__single_perturb_simulations_number=1
param_scan__single_perturb_prefix_results_filename=report_param_scan__single_perturb_