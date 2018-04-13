# Import libraries. Note: dependencies must be installed.

# library for least squares fit using levenberg-marquart algorithm
if(!require(reshape2)){
  install.packages('reshape2')
  library(reshape2)
}
# library for solving differential equations
if(!require(deSolve)){
  install.packages('deSolve')
  library(deSolve)
}
# library for least squares fit using levenberg-marquart algorithm
if(!require(minpack.lm)){
  install.packages('minpack.lm')
  library(minpack.lm)
}

# get the report file name
args <- commandArgs(trailingOnly=TRUE)
report_filename  <-  "insulin_receptor_param_estim.csv"
if(length(args) > 0) {
  report_filename <- args[1]
}

# retrieve the folder of this file to load the data set file name.
args <- commandArgs(trailingOnly=FALSE)
SBPIPE_R <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))

# load concentration data
df <- read.table(file.path(SBPIPE_R,'insulin_receptor_dataset.csv'), header=TRUE, sep=',')
colnames(df) <- c("time", "B")

# mathematical model
insulin_receptor <- function(t,x,parms){
  # t: time
  # x: initial concentrations
  # parms: kinetic rate constants and the insulin input
  insulin <- 1
  with(as.list(c(parms, x)), {
      dA <- -k1*A*insulin + k3*C
      dB <- k1*A*insulin - k2*B
      dC <- k2*B - k3*C   
      res <- c(dA, dB, dC)
      list(res)
  })
}


# residual function
rf <- function(parms){
  # inital concentration
  cinit <- c(A=16.5607,B=0,C=0)
  # time points
  t <- seq(0,120,1)
  # parameters from the parameter estimation routine
  k1 <- parms[1]
  k2 <- parms[2]
  k3 <- parms[3]
  # solve ODE for a given set of parameters
  out <- ode(y=cinit,times=t,func=insulin_receptor,
             parms=list(k1=k1,k2=k2,k3=k3),method="ode45")
  
  outdf <- data.frame(out)
  # filter the column we have data for
  outdf <- outdf[ , c("time", "B")]
  # Filter data that contains time points where data is available
  outdf <- outdf[outdf$time %in% df$time,]
  # Evaluate predicted vs experimental residual
  preddf <- melt(outdf,id.var="time",variable.name="species",value.name="conc")
  expdf <- melt(df,id.var="time",variable.name="species",value.name="conc")
  ssqres <- sqrt((expdf$conc-preddf$conc)^2)

  # return predicted vs experimental residual
  return(ssqres)
}

# parameter fitting using Levenberg-Marquardt nonlinear least squares algorithm
# initial guess for parameters
parms <- runif(3, 0.001, 1)
names(parms) <- c("k1", "k2", "k3")
tc <- textConnection("eval_functs","w")
sink(tc)
fitval <- nls.lm(par=parms,
                 lower=rep(0.001,3), upper=rep(1,3),
                 fn=rf,
                 control=nls.lm.control(nprint=1, maxiter=100))
sink()
close(tc)

# create the report containing the evaluated functions
report <- NULL;
for (eval_fun in eval_functs) {
  items <- strsplit(eval_fun, ",")[[1]]
  rss <- items[2]
  rss <- gsub("[[:space:]]", "", rss)
  rss <- strsplit(rss, "=")[[1]]
  rss <- rss[2]
  estim.parms <- items[3]
  estim.parms <- strsplit(estim.parms, "=")[[1]]
  estim.parms <- strsplit(trimws(estim.parms[[2]]), "\\s+")[[1]]
  rbind(report, c(rss, estim.parms)) -> report
}
report <- data.frame(report)
names(report) <- c("rss", names(parms))

# write the output
write.table(report, file=report_filename, sep="\t", row.names=FALSE, quote=FALSE)
