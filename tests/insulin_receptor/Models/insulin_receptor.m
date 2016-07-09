% PottersWheel model definition file

function m = insulin_receptor()

m = pwGetEmptyModel();

%% Meta information

m.ID          = 'insulin_receptor';
m.name        = 'insulin_receptor';
m.description = 'insulin_receptor';
m.authors     = {'Piero Dalle Pezze'};
m.dates       = {'2012'};
m.type        = 'PW-2-1-13';

% FEBS model with michelis-menten kinetic rates



%% X: Dynamic variables
% m = pwAddX(m, ID, startValue, type, minValue, maxValue, unit, compartment, name, description, typeOfStartValue)
m = pwAddX(m, 'IR_beta'           , 16.5607078175, 'fix', 0, 50,   [], 'Cell');
m = pwAddX(m, 'IR_beta_pY1146'    ,             0, 'fix', 0, 50,   [], 'Cell');
m = pwAddX(m, 'IR_beta_refractory',             0, 'fix', 0, 50,   [], 'Cell');
m = pwAddX(m, 'unknown_species',               10, 'fix', 0, 50,   [], 'Cell');
m = pwAddX(m, 'unknown_species_p',              0, 'fix', 0, 50,   [], 'Cell');

%% R: Reactions
% m = pwAddR(m, reactants, products, modifiers, type, options, rateSignature, parameters, description, ID, name, fast, compartments, parameterTrunks, designerPropsR, stoichiometry, reversible)

% Michaelis-Menten 
%m = pwAddR(m, {'IR_beta'                 }, {'IR_beta_pY1146'          }, {'Insulin'	          	}, 'MM', [], ['r1_k1 * r1 * m1 / (r1_k2 + r1)'], {'r1_k1','r1_k2'		           }, 'IR_beta_phosphorylation_by_Insulin'		  	, 'r1', [], [], {}, {}, {});
%m = pwAddR(m, {'IR_beta_pY1146'          }, {'IR_beta_refractory'      }, {       	          	}, 'MM2', [], ['r2_k1 * r1 / (r2_k2 + r1)'], {'r2_k1','r2_k2'  		           }, 'IR_beta_pY1146_dephosphorylation'  		  	, 'r2', [], [], {}, {}, {});
%m = pwAddR(m, {'IR_beta_refractory'      }, {'IR_beta'                 }, {         	          	}, 'A', [], [], {'r3_k1'                     		           }, 'IR_beta_ready'                     		  	, 'r3', [], [], {}, {}, {});
% Mass-actions
m = pwAddR(m, {'IR_beta'                 }, {'IR_beta_pY1146'          }, {'Insulin'	          	}, 'A', [], [], {'IR_beta_phosphorylation_by_Insulin'       }, 'IR_beta_phosphorylation_by_Insulin'		  	, 'r1', [], [], {}, {}, {});
m = pwAddR(m, {'IR_beta_pY1146'          }, {'IR_beta_refractory'      }, {       	          	}, 'A', [], [], {'IR_beta_pY1146_dephosphorylation'         }, 'IR_beta_pY1146_dephosphorylation'  		  	, 'r2', [], [], {}, {}, {});
m = pwAddR(m, {'IR_beta_refractory'      }, {'IR_beta'                 }, {         	          	}, 'A', [], [], {'IR_beta_ready'   		           }, 'IR_beta_ready'                     		  	, 'r3', [], [], {}, {}, {});
m = pwAddR(m, {'unknown_species'      }, {'unknown_species_p'          }, {'IR_beta_pY1146'       	}, 'A', [], [], {'unknown_species_phosphorylation'  }, 'unknown_species_phosphorylation'                     		  	, 'r4', [], [], {}, {}, {});
m = pwAddR(m, {'unknown_species_p'      }, {'unknown_species'          }, {       	}, 'A', [], [], {'unknown_species_dephosphorylation'  }, 'unknown_species_dephosphorylation'                     		  	, 'r5', [], [], {}, {}, {});


 


%% C: Compartments
% m = pwAddC(m, ID, size,  outside, spatialDimensions, name, unit, constant)

m = pwAddC(m, 'Cell', 1, [], 3, 'Cell', [], 1);


%% K: Dynamical parameters
% m = pwAddK(m, ID, value, type, minValue, maxValue, unit, name, description)
% Michaelis-Menten 
%m = pwAddK(m, 'r1_k1'                     , 0.0589212197442898  , 'global', 1e-06, 1e+04);
%m = pwAddK(m, 'r1_k2'                     , 0.0589212197442898  , 'global', 1e-06, 1e+04);
%m = pwAddK(m, 'r2_k1'                     , 0.504134783892512   , 'global', 1e-06, 1e+04);
%m = pwAddK(m, 'r2_k2'                     , 0.504134783892512   , 'global', 1e-06, 1e+04);
%m = pwAddK(m, 'r3_k1'                     , 0.0553343473568815  , 'global', 1e-06, 1e+04);
% Mass-actions
m = pwAddK(m, 'IR_beta_phosphorylation_by_Insulin'                     , 0.0589212197442898  , 'global', 1e-06, 1e+04);
m = pwAddK(m, 'IR_beta_pY1146_dephosphorylation'                     , 0.0589212197442898  , 'global', 1e-06, 1e+04);
m = pwAddK(m, 'IR_beta_ready'                     , 0.504134783892512   , 'global', 1e-06, 1e+04);
m = pwAddK(m, 'unknown_species_phosphorylation'                     , 0.504134783892512   , 'global', 1e-06, 1e+04);
m = pwAddK(m, 'unknown_species_dephosphorylation'                     , 0.504134783892512   , 'global', 1e-06, 1e+04);


%% U: Driving input
% m = pwAddU(m, ID, uType, uTimes, uValues, compartment, name, description, u2Values, alternativeIDs, designerProps)

m = pwAddU(m, 'Insulin',     'steps', [-1 0]  , [0 1]  , 'Cell', [], [], [0 0]);

%% Default sampling time points
m.t = 0:1:120;


%% Y: Observables
% m = pwAddY(m, rhs, ID, scalingParameter, errorModel, noiseType, unit, name, description, alternativeIDs, designerProps)

m = pwAddY(m, 'IR_beta_pY1146' 		, 'IR_beta_pY1146_obs'    , 'scale_IR_beta_pY1146_obs'   , 'y * 0.10 + max(y) * 0.10', 'Gaussian', [], [], []);


%% S: Scaling parameters
% m = pwAddS(m, ID, value, type, minValue, maxValue, unit, name, description)

m = pwAddS(m, 'scale_IR_beta_pY1146_obs'  , 1, 'fix', 0.01, 50);


%% Rules
% m = pwAddRule(m, lhs, reactants, parameters, ruleSignature, type, description, ID)


%% Derived variables
% m = pwAddZ(m, rhs, ID, unit, name, description)


%% Derived parameters
% m = pwAddP(m, rhs, ID, unit, name, description)


%% Constraints
% m = pwAddConstraint(m, lhs, operator, rhs, reactants, parameters, lambda)


%% Designer properties (do not modify)
m.designerPropsM = [1 1 1 0 0 0 400 250 600 400 1 1 1 0 0 0 1 0 0];
