

# Model from https://cran.r-project.org/web/packages/sde/sde.pdf

# import sde package
# sde and its dependencies must be installed.
if(!require(sde)){
    install.packages('sde', repos='http://cran.r-project.org')
    library(sde)
}


# Retrieve the report file name (necessary for stochastic simulations)
args <- commandArgs(trailingOnly=TRUE)
report_filename = "sde_periodic_drift.csv"
if(length(args) > 0) {
    report_filename <- args[1]
}


# Model definition
# ---------------------------------------------
# set.seed()
d <- expression(sin(x))
d.x <- expression(cos(x))
A <- function(x) 1-cos(x)

X0 <- 0
delta <- 1/20
N <- 500
time <- seq(X0, N*delta, by=delta)

# EA = exact method
periodic_drift <- sde.sim(method="EA", delta=delta, X0=X0, N=N, drift=d, drift.x=d.x, A=A)

out <- data.frame(time, periodic_drift)
# ---------------------------------------------



# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row names must be discarded.
write.table(out, file=report_filename, sep="\t", row.names=FALSE)

