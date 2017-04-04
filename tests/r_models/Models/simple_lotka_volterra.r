

# Model from https://cran.r-project.org/web/packages/deSolve/deSolve.pdf

# import deSolve package
# deSolve and its dependencies must be installed.
if(!require(deSolve)){
    install.packages('deSolve', repos='http://cran.r-project.org')
    library(deSolve)
}


# Retrieve the report file name (necessary for stochastic simulations)
args <- commandArgs(trailingOnly=TRUE)
report_filename = "simple_lotka_volterra.csv"
if(length(args) > 0) {
    report_filename <- args[1]
}



# Model definition
# ---------------------------------------------
## =======================================================================
## Example 1:
## A simple resource limited Lotka-Volterra-Model
##
## Note:
## 1. parameter and state variable names made
## accessible via "with" function
## 2. function sigimp accessible through lexical scoping
## (see also ode and rk examples)
## =======================================================================
SPCmod <- function(t, x, parms) {
    with(as.list(c(parms, x)), {
        import <- sigimp(t)
        dS <- import - b*S*P + g*C #substrate
        dP <- c*S*P - d*C*P #producer
        dC <- e*P*C - f*C #consumer
        res <- c(dS, dP, dC)
        list(res)
    })
}
## Parameters
parms <- c(b = 0.0, c = 0.1, d = 0.1, e = 0.1, f = 0.1, g = 0.0)
## vector of timesteps
times <- seq(0, 100, length = 101)
## external signal with rectangle impulse
signal <- as.data.frame(list(times = times,
import = rep(0,length(times))))
signal$import[signal$times >= 10 & signal$times <= 11] <- 0.2
sigimp <- approxfun(signal$times, signal$import, rule = 2)
## Start values for steady state
y <- xstart <- c(S = 1, P = 1, C = 1)
## Solving
out <- lsoda(xstart, times, SPCmod, parms)
# ---------------------------------------------



# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row names must be discarded.
write.table(out, file=report_filename, sep="\t", row.names=FALSE)

