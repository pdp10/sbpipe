

# Model from https://cran.r-project.org/web/packages/sde/sde.pdf

# import sde package
# sde and its dependencies must be installed.
if(!require(sde)){
    install.packages('sde')
    library(sde)
}


# Retrieve the report file name (necessary for stochastic simulations)
args <- commandArgs(trailingOnly=TRUE)
report_filename = "sde_cox_ingersoll_ross_process.csv"
if(length(args) > 0) {
    report_filename <- args[1]
}


# Model definition
# ---------------------------------------------
# set.seed()
# Cox-Ingersoll-Ross process
# dXt = (6-3*Xt)*dt + 2*sqrt(Xt)*dWt

d <- expression( 6-3*x )
s <- expression( 2*sqrt(x) )
X0 <- 10

delta <- 1/50
N <- 500
time <- seq(0, N*delta, by=delta)

Cox_Ingersoll_Ross <- sde.sim(delta=delta, X0=X0, N=N, drift=d, sigma=s)

out <- data.frame(time, Cox_Ingersoll_Ross)
# ---------------------------------------------



# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row names must be discarded.
write.table(out, file=report_filename, sep="\t", row.names=FALSE)

