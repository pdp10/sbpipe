#!/usr/bin/octave -qf

# Prevent Octave from thinking that this
# is a function file:
#1;

# Retrieve the report file name (necessary for stochastic simulations)
report_filename = "nonlinear_octave_model.csv";
arg_list = argv ();
if length(arg_list) > 0
  report_filename = arg_list{1};
endif


# Model definition
# example from : GNU Octave
# A high-level interactive language for numerical computations
# Edition 3 for Octave version 3.2.4
# July 2007
# ---------------------------------------------
function xdot = f (x,t)
  r = 0.25;
  k = 1.4;
  a = 1.5;
  b = 0.16;
  c = 0.9;
  d = 0.8;
  xdot(1) = r*x(1)*(1 - x(1)/k) - a*x(1)*x(2)/(1 +b*x(1));
  xdot(2) = c*a*x(1)*x(2)/(1 + b*x(1)) - d*x(2);
endfunction

x0 = [1;2];
t = linspace (0,50,200)';
x = lsode ("f",x0,t);
# ---------------------------------------------


# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row indexes must be discarded.
fid = fopen (report_filename, "w");
fputs (fid, "Time\tX1\tX2\n");
for i = 1:length(t)
  fputs (fid, [num2str(t(i)) "\t" num2str(x(i,1)) "\t" num2str(x(i,2)) "\n"]);
endfor
fclose (fid);

