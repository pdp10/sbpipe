

xi = 0:1:120;

xT1 = [0,1,3,5,10,15,20,30,45,60,120];

mTOR_pS2448_obs	  = [0,	1.94,	  2.52,	     4.115,	   6.09,	  6.28,	5.875,	6.38,	7.675,	6.955,		8.38];
mTOR_pS2481_obs	  = [0,	1.545,	   2.37375,	 3.27,	   4.395,	   5.14125,	6.28125,	8.10375,	7.2675,	6.53625,		8.625];
PRAS40_pS183_obs  = [0,	0.58575,	3.71625, 4.7085,	4.41075,	5.19825,	6.27225,	6.9285,	8.079,	7.97775,		6.966];
PRAS40_pT246_obs  = [0,	3.445875,	6.95925, 8.48475,	5.842125,	7.03575,	6.03,	6.708375,	6.395625,	5.83875,		5.518125];
p70S6K_pT389_obs  = [0,	0.0818,	   0.137,	 0.2742,	0.9238,	  1.669,	2.823,	3.2152,	5.339,	5.8492,		7.8946];
Akt_pT308_obs     = [0,	6.135,	   12.282,	 11.2905,	5.5275,	  5.9715,	9.7455,	10.749,	12.327,	7.6395,		6.843];
Akt_pS473_obs     = [0,	3.269025,  7.62705,	 7.754625,	4.1691,	  5.4153,	7.1244,	6.2397,	6.808725,	4.157775,		3.65895];
IR_beta_pY1146_obs= [0,	8.158,	   7.386,	 4.952,	   2.494,	  2.27,	1.904,	1.786,	1.578,	1.694,		1.776];
IRS1_pS636_obs    = [ 0, 2.94,	  2.1525,	 2.555,	   4.3925,    4.8475,	3.2375,	6.0725,	5.7225,	5.5475,		8.54];

mTOR_pS2448_obs_i    = interp1(xT1, mTOR_pS2448_obs, xi, 'linear');
mTOR_pS2481_obs_i    = interp1(xT1, mTOR_pS2481_obs, xi, 'linear');
PRAS40_pS183_obs_i   = interp1(xT1, PRAS40_pS183_obs, xi, 'linear');
PRAS40_pT246_obs_i   = interp1(xT1, PRAS40_pT246_obs, xi, 'linear');
p70S6K_pT389_obs_i   = interp1(xT1, p70S6K_pT389_obs, xi, 'linear');
Akt_pT308_obs_i      = interp1(xT1, Akt_pT308_obs, xi, 'linear');
Akt_pS473_obs_i      = interp1(xT1, Akt_pS473_obs, xi, 'linear');
IR_beta_pY1146_obs_i = interp1(xT1, IR_beta_pY1146_obs, xi, 'linear');
IRS1_pS636_obs_i     = interp1(xT1, IRS1_pS636_obs, xi, 'linear');

% NOTE: vectors start from 1 
fprintf('\nmTOR_pS2448_obs_i at Min 100 is %d \n'   , mTOR_pS2448_obs_i(101));
fprintf('mTOR_pS2481_obs_i at Min 100 is %d \n'   , mTOR_pS2481_obs_i(101));
fprintf('PRAS40_pS183_obs_i at Min 100 is %d \n'  , PRAS40_pS183_obs_i(101));
fprintf('PRAS40_pT246_obs_i at Min 100 is %d \n'  , PRAS40_pT246_obs_i(101));
fprintf('p70S6K_pT389_obs_i at Min 100 is %d \n'  , p70S6K_pT389_obs_i(101));
fprintf('Akt_pT308_obs_i at Min 100 is %d \n'     , Akt_pT308_obs_i(101));
fprintf('Akt_pS473_obs_i at Min 100 is %d \n'     , Akt_pS473_obs_i(101));
fprintf('IR_beta_pY1146_obs_i at Min 100 is %d \n', IR_beta_pY1146_obs_i(101));
fprintf('IRS1_pS636_obs_i at Min 100 is %d \n\n'    , IRS1_pS636_obs_i(101));




xT2 = [0,3,20,45,100];
AMPK_pT172_obs=       [0,   10.531448362,	10.2548603195,	8.0805,	    4.0059430832];
TSC1_TSC2_pS1347_obs= [0,	7.8131403452,	9.6628314487,	10.8905,	8.0118861664];

AMPK_pT172_obs_i = interp1(xT2, AMPK_pT172_obs, xi, 'cubic');
TSC1_TSC2_pS1347_obs_i = interp1(xT2, TSC1_TSC2_pS1347_obs, xi, 'cubic');

fprintf('AMPK_pT172_obs_i at Min 1 is %d \n'     , AMPK_pT172_obs_i(2));
fprintf('AMPK_pT172_obs_i at Min 5 is %d \n'     , AMPK_pT172_obs_i(6));
fprintf('AMPK_pT172_obs_i at Min 10 is %d \n'    , AMPK_pT172_obs_i(11));
fprintf('AMPK_pT172_obs_i at Min 15 is %d \n'    , AMPK_pT172_obs_i(16));
fprintf('AMPK_pT172_obs_i at Min 30 is %d \n'    , AMPK_pT172_obs_i(31));
fprintf('AMPK_pT172_obs_i at Min 60 is %d \n'    , AMPK_pT172_obs_i(61));
fprintf('AMPK_pT172_obs_i at Min 120 is %d \n\n'   , AMPK_pT172_obs_i(121));


fprintf('TSC1_TSC2_pS1347_obs at Min 1 is %d \n'   , TSC1_TSC2_pS1347_obs_i(2));
fprintf('TSC1_TSC2_pS1347_obs at Min 5 is %d \n'   , TSC1_TSC2_pS1347_obs_i(6));
fprintf('TSC1_TSC2_pS1347_obs at Min 10 is %d \n'  , TSC1_TSC2_pS1347_obs_i(11));
fprintf('TSC1_TSC2_pS1347_obs at Min 15 is %d \n'  , TSC1_TSC2_pS1347_obs_i(16));
fprintf('TSC1_TSC2_pS1347_obs at Min 30 is %d \n'  , TSC1_TSC2_pS1347_obs_i(31));
fprintf('TSC1_TSC2_pS1347_obs at Min 60 is %d \n'  , TSC1_TSC2_pS1347_obs_i(61));
fprintf('TSC1_TSC2_pS1347_obs at Min 120 is %d \n' , TSC1_TSC2_pS1347_obs_i(121));




