import numpy as np
from scipy.integrate import odeint
import pandas as pd
import sys

# Retrieve the report file name (necessary for stochastic simulations)
report_filename = "insulin_receptor.csv"
if len(sys.argv) > 1:
    report_filename = sys.argv[1]



# Model definition
# ---------------------------------------------
def insulin_receptor(y, t, inp, p):
    dy0 = - p[0] * y[0] * inp[0] + p[2] * y[2]
    dy1 = + p[0] * y[0] * inp[0] - p[1] * y[1]
    dy2 = + p[1] * y[1] - p[2] * y[2]
    return [dy0, dy1, dy2]

# input
inp = [1]
# Parameters
p = [0.475519, 0.471947, 0.0578119]
# a tuple for the arguments (see odeint syntax)
config = (inp, p)

# initial value
y0 = np.array([16.5607, 0, 0])

# vector of time steps
time = np.linspace(0.0, 20.0, 100)

# simulate the model
y = odeint(insulin_receptor, y0=y0, t=time, args=config)
# ---------------------------------------------


# Make the data frame
# d = {'time': pd.Series(time),
#      'IR_beta': pd.Series(y[:, 0]),
#      'IR_beta_pY1146': pd.Series(y[:, 1]),
#      'IR_beta_refractory': pd.Series(y[:, 2])}

# we generate as little as possible to speed up testing.
d = {'time': pd.Series(time),
     'IR_beta_pY1146': pd.Series(y[:, 1])}
df = pd.DataFrame(d)

# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row indexes must be discarded.
df.to_csv(report_filename, sep='\t', index=False, encoding='utf-8')
