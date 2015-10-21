/* PottersWheel loadData function for model insulin_receptor */
/* Automatically generated on 2012-08-02 17:41:21 */
/* www.PottersWheel.de */

void loadData()
{
    mxArray const *pwGlobals;
    mxArray *mxCouples, *mxStimuli, *mxDrivingFunctions;
    int currentCouple, currentStimulus;

	/* Get information from global variable: */
	pwGlobals = mexGetVariablePtr("global", "pwGlobals");

	/* Which couple and stimulus do we need? */
	currentCouple   = (int) mxGetPr(mxGetField(pwGlobals, 0, "currentCouple"))[0];
	currentStimulus = (int) mxGetPr(mxGetField(pwGlobals, 0, "currentStimulus"))[0];

	/* Get current couple, stimulus and driving functions */
	mxCouples = mxGetField(pwGlobals, 0, "couples");
	mxStimuli = mxGetField(mxCouples, currentCouple - 1, "stimuli");
	mxDrivingFunctions = mxGetField(mxStimuli, currentStimulus - 1, "drivingFunctions");

	/* Get parameter vector k of current couple and stimulus */
	kGlobal = mxGetPr(mxGetField(mxCouples, currentCouple -1 , "k")) - 1; /* We need k to be one-based */
	uType1    = (int) mxGetPr(mxGetField(mxDrivingFunctions, 0, "uType"))[0];
	uTimes1   = mxGetPr(mxGetField(mxDrivingFunctions, 0, "uTimes"));
	uValues1  = mxGetPr(mxGetField(mxDrivingFunctions, 0, "uValues"));
	u2Values1 = mxGetPr(mxGetField(mxDrivingFunctions, 0, "u2Values"));
	nValues1  = mxGetNumberOfElements(mxGetField(mxDrivingFunctions, 0, "uValues"));
}
