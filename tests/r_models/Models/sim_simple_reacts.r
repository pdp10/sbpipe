# Example edited from:
#
# Computational Appendix of Book
# Chemical Reactor Analysis and Design Fundamentals - Rawlings and Ekerdt
#
# Example A.5: Estimating rate constants for A->B->C from concentration vs time data


# Model from https://cran.r-project.org/web/packages/deSolve/deSolve.pdf

# import deSolve package
# deSolve and its dependencies must be installed.
if(!require(deSolve)){
    install.packages('deSolve', repos='http://cran.r-project.org')
    library(deSolve)
}


# Retrieve the report file name
args <- commandArgs(trailingOnly=TRUE)
report_filename = "sim_simple_reacts.csv"
if(length(args) > 0) {
    report_filename <- args[1]
}



# Mathematical model
my_model <- function(t,x,parms){
  # t: time
  # x: initial concentrations
  # parms: kinetic rate constant
  with(as.list(c(parms, x)), {
      dA <- -k1*A
      dB <- k1*A - k2*B
      dC <- k2*B
      res <- c(dA, dB, dC)
      list(res)
  })
}



## Parameters
parms <- c(k1=0.92292, k2=0.448036)
## vector of timesteps
times <- seq(0,5,0.1)
## Start values
xstart <- c(A=1,B=0,C=0)
## Solving
out <- lsoda(xstart, times, my_model, parms)
# ---------------------------------------------



# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row names must be discarded.
write.table(out, file=report_filename, sep="\t", row.names=FALSE)

