/** PottersWheel ODE for model insulin_receptor
 *  Automatically generated on 2012-08-02 16:49:43
 *  www.PottersWheel.de
 **/


/* Global variables */
double *aGlobal;
double *kGlobal;
double *sGlobal;
double  tGlobal;
double *uGlobal;
double *xGlobal;
double *y0Global;
double *uTimes1, *uValues1, *u2Values1;
int uType1, nValues1;


/* Help functions and constants*/
double nthroot(double a, double b){return pow(a, 1.0/b);}
bool lt(double a, double b){ return a < b; }
bool gt(double a, double b){ return a > b; }
bool eq(double a, double b){ return a == b; }
bool ge(double a, double b){ return a >= b; }
bool le(double a, double b){ return a <= b; }
bool and(bool a, bool b) {if (a == true && b == true) return true; else return false;}
bool or(bool a, bool b) {if (a == true || b == true) return true; else return false;}
#ifndef min
double max(double a, double b) {if (a < b) return b; else return a;}
double min(double a, double b) {if (a > b) return b; else return a;}
#endif

double piecewise(int n, ...)
{
    va_list args;
    int i = 0;
    double result;
    int condition;
    va_start (args, n);
    for (i = 0; i < n/2; i++)
    {
       result = va_arg(args, double);
       condition = va_arg(args, int);
       if (condition == 1)
       {
           va_end (args);
           return result;
       }
    }
    result = va_arg (args, double);
    va_end (args);
    return result;
}

double pi = 3.14159265358979;


void getdxdt2(double t, double x[], double dxdt[], double v[])
{

/**************************************************************
/* Local and global variables */
double a[1];
double c[2];
double u[2];
double* k;
double* s;
double* y;
aGlobal = a;
tGlobal = t;
uGlobal = u;
xGlobal = x;
k = kGlobal;
s = sGlobal;
y = y0Global;

/**************************************************************
/* Identifiers

Dynamic variables
x[ 1]: IR_beta
x[ 2]: IR_beta_pY1146
x[ 3]: IR_beta_refractory
x[ 4]: unknown_species
x[ 5]: unknown_species_p

Algebraic equations
Compartments
c[ 1]: Cell

Scaling factors (only of default observation as specified in the model definition file)
s[ 1]: scale_IR_beta_pY1146_obs

Observables (only of default observation as specified in the model definition file)
y[ 1]: IR_beta_pY1146_obs

Dynamic parameters
k[ 1]: IR_beta_phosphorylation_by_Insulin
k[ 2]: IR_beta_pY1146_dephosphorylation
k[ 3]: IR_beta_ready
k[ 4]: unknown_species_phosphorylation
k[ 5]: unknown_species_dephosphorylation

Driving input functions
u[ 1]: Insulin

**/
/* Driving input */
u[1]     = interpolate(uTimes1, uValues1, u2Values1, nValues1, t, uType1);


/* Compartments */
c[1]=1.0;

/* Rates */
v[ 1]    = k[1]*x[1]*u[1];
v[ 2]    = k[2]*x[2];
v[ 3]    = k[3]*x[3];
v[ 4]    = k[4]*x[4]*x[2];
v[ 5]    = k[5]*x[5];


/* ODE */
dxdt[ 1] =  - v[1] + v[3];
dxdt[ 2] = v[1] - v[2];
dxdt[ 3] = v[2] - v[3];
dxdt[ 4] =  - v[4] + v[5];
dxdt[ 5] = v[4] - v[5];


}


/* Calculation of derivatives */
void getdxdt(double t, double x[], double dxdt[])
{

/**************************************************************
/* Local and global variables */
double a[1];
double c[2];
double u[2];
double v[6];
double* k;
double* s;
double* y;
aGlobal = a;
tGlobal = t;
uGlobal = u;
xGlobal = x;
k = kGlobal;
s = sGlobal;
y = y0Global;

/**************************************************************
/* Identifiers

Dynamic variables
x[ 1]: IR_beta
x[ 2]: IR_beta_pY1146
x[ 3]: IR_beta_refractory
x[ 4]: unknown_species
x[ 5]: unknown_species_p

Algebraic equations
Compartments
c[ 1]: Cell

Scaling factors (only of default observation as specified in the model definition file)
s[ 1]: scale_IR_beta_pY1146_obs

Observables (only of default observation as specified in the model definition file)
y[ 1]: IR_beta_pY1146_obs

Dynamic parameters
k[ 1]: IR_beta_phosphorylation_by_Insulin
k[ 2]: IR_beta_pY1146_dephosphorylation
k[ 3]: IR_beta_ready
k[ 4]: unknown_species_phosphorylation
k[ 5]: unknown_species_dephosphorylation

Driving input functions
u[ 1]: Insulin

**/
/* Driving input */
u[1]     = interpolate(uTimes1, uValues1, u2Values1, nValues1, t, uType1);


/* Compartments */
c[1]=1.0;

/* Rates */
v[ 1]    = k[1]*x[1]*u[1];
v[ 2]    = k[2]*x[2];
v[ 3]    = k[3]*x[3];
v[ 4]    = k[4]*x[4]*x[2];
v[ 5]    = k[5]*x[5];


/* ODE */
dxdt[ 1] =  - v[1] + v[3];
dxdt[ 2] = v[1] - v[2];
dxdt[ 3] = v[2] - v[3];
dxdt[ 4] =  - v[4] + v[5];
dxdt[ 5] = v[4] - v[5];


}


