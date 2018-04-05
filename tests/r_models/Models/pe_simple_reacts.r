# Example edited from:
#
# Computational Appendix of Book
# Chemical Reactor Analysis and Design Fundamentals - Rawlings and Ekerdt
#
# Example A.5: Estimating rate constants for A->B->C from concentration vs time data
#


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


# Retrieve the report file name

args <- commandArgs(trailingOnly=TRUE)
report_filename = "pe_simple_reacts.csv"
if(length(args) > 0) {
  report_filename <- args[1]
}


# we retrieve the folder of this file to load the data set file name.
args <- commandArgs(trailingOnly = FALSE)
SBPIPE_R <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))

# Load concentration data
df <- read.table(file.path(SBPIPE_R,'pe_simple_reacts_dataset.csv'), header=TRUE, sep="\t")
#df <- read.table("pe_simple_reacts_dataset.csv", header=TRUE, sep=",")


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


# residual function
rf=function(parms){
  # parms: the model parameters to estimate
  
  # inital concentration
  cinit=c(A=1,B=0,C=0)
  # time points for which conc is reported
  # include the points where data is available
  t=c(seq(0,5,0.1),df$time)
  t=sort(unique(t))
  # parameters from the parameter estimation routine
  k1=parms[1]
  k2=parms[2]
  # solve ODE for a given set of parameters
  out=ode(y=cinit,times=t,func=my_model,
          parms=list(k1=k1,k2=k2),method="ode23")
  
  # Filter data that contains time points where data is available
  outdf=data.frame(out)
  outdf=outdf[outdf$time %in% df$time,]
  # Evaluate predicted vs experimental residual
  preddf=melt(outdf,id.var="time",variable.name="species",value.name="conc")
  expdf=melt(df,id.var="time",variable.name="species",value.name="conc")
  ssqres=sqrt((expdf$conc-preddf$conc)^2)

  # return predicted vs experimental residual
  return(ssqres)
}



# Parameter fitting using levenberg marquart algorithm

# initial guess for parameters
parms <- runif(2, 0.0001, 10.0)
names(parms) <- c("k1", "k2")
# parms <- c(k1=0.5, k2=0.5)
#print(parms)

# fitting
# Is there a better way to retrieve nls.lm.control ?? 
# So far I have to capture the print lines, and then parse them...
#----------
tc <- textConnection("eval_functs_text","w")
sink(tc)

fitval=nls.lm(par=parms,fn=rf,control=nls.lm.control(nprint=1))

sink()
close(tc)
#----------


# Create the report containing the evaluated functions

report <- NULL;
for (eval_fun in eval_functs_text) {
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
# print(report)

# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row names must be discarded.
write.table(report, file=report_filename, sep="\t", row.names=FALSE, quote=FALSE)
