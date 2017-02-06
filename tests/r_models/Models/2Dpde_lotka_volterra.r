

# Model from https://cran.r-project.org/web/packages/deSolve/deSolve.pdf

# import deSolve package
# deSolve and its dependencies must be installed.
if(!require(deSolve)){
    install.packages('deSolve')
    library(deSolve)
}


# Retrieve the report file name (necessary for stochastic simulations)
args <- commandArgs(trailingOnly=TRUE)
report_filename = "2Dpde_lotka_volterra.csv"
if(length(args) > 0) {
    report_filename <- args[1]
}


# Model definition
# ---------------------------------------------
## =======================================================================
## A Lotka-Volterra predator-prey model with predator and prey
## dispersing in 2 dimensions
## =======================================================================
## ==================
## Model definitions
## ==================
lvmod2D <- function (time, state, pars, N, Da, dx) {
    NN <- N*N
    Prey <- matrix(nrow = N, ncol = N,state[1:NN])
    Pred <- matrix(nrow = N, ncol = N,state[(NN+1):(2*NN)])
    with (as.list(pars), {
        ## Biology
        dPrey <- rGrow * Prey * (1- Prey/K) - rIng * Prey * Pred
        dPred <- rIng * Prey * Pred*assEff - rMort * Pred
        zero <- rep(0, N)
        ## 1. Fluxes in x-direction; zero fluxes near boundaries
        FluxPrey <- -Da * rbind(zero,(Prey[2:N,] - Prey[1:(N-1),]), zero)/dx
        FluxPred <- -Da * rbind(zero,(Pred[2:N,] - Pred[1:(N-1),]), zero)/dx
        ## Add flux gradient to rate of change
        dPrey <- dPrey - (FluxPrey[2:(N+1),] - FluxPrey[1:N,])/dx
        dPred <- dPred - (FluxPred[2:(N+1),] - FluxPred[1:N,])/dx
        ## 2. Fluxes in y-direction; zero fluxes near boundaries
        FluxPrey <- -Da * cbind(zero,(Prey[,2:N] - Prey[,1:(N-1)]), zero)/dx
        FluxPred <- -Da * cbind(zero,(Pred[,2:N] - Pred[,1:(N-1)]), zero)/dx
        ## Add flux gradient to rate of change
        dPrey <- dPrey - (FluxPrey[,2:(N+1)] - FluxPrey[,1:N])/dx
        dPred <- dPred - (FluxPred[,2:(N+1)] - FluxPred[,1:N])/dx
        return(list(c(as.vector(dPrey), as.vector(dPred))))
    })
}
## ===================
## Model applications
## ===================
pars <- c(rIng = 0.2, # /day, rate of ingestion
          rGrow = 1.0, # /day, growth rate of prey
          rMort = 0.2 , # /day, mortality rate of predator
          assEff = 0.5, # -, assimilation efficiency
          K = 5 ) # mmol/m3, carrying capacity
R <- 10 # total length of surface, m
N <- 4 # number of boxes in one direction
dx <- R/N # thickness of each layer
Da <- 0.05 # m2/d, dispersion coefficient
NN <- N*N # total number of boxes
## initial conditions
yini <- rep(0, 2*N*N)
cc <- c((NN/2):(NN/2+1)+N/2, (NN/2):(NN/2+1)-N/2)
yini[cc] <- yini[NN+cc] <- 1
## solve model using Cash-Karp Runge-Kutta method
times <- seq(0, 20, by = 1)
out <- ode.2D(y = yini, times = times, func = lvmod2D, parms = pars,
              dimens = c(N, N), names = c("Prey", "Pred"),
              N = N, dx = dx, Da = Da, method = rkMethod("rk45ck"))
# ---------------------------------------------



# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row names must be discarded.
write.table(out, file=report_filename, sep="\t", row.names=FALSE)

