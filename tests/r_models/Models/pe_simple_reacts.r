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
# library for plotting
if(!require(ggplot2)){
  install.packages('ggplot2')
  library(ggplot2)
}



# Retrieve the report file name
args <- commandArgs(trailingOnly=TRUE)
report_filename = "pe_simple_reacts.csv"
if(length(args) > 0) {
  report_filename <- args[1]
}



# Load concentration data
df=read.table("pe_simple_reacts_dataset.csv", header=TRUE, sep=",")


# Mathematical model
my_model=function(t,c,parms){
  # t: time
  # c: initial concentrations  
  # parms: kinetic rate constant
  
  k1=parms$k1
  k2=parms$k2
  
  r=rep(0,length(c))
  r[1]=-k1*c["A"]  #dcA/dt
  r[2]=k1*c["A"]-k2*c["B"] #dcB/dt
  r[3]=k2*c["B"] #dcC/dt

  return(list(r))
}


# Calculate the residual sum of squares (RSS)
ssq=function(parms){
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
  out=ode(y=cinit,times=t,func=my_model,parms=list(k1=k1,k2=k2))
  
  # Filter data that contains time points where data is available
  outdf=data.frame(out)
  outdf=outdf[outdf$time %in% df$time,]
  # Evaluate predicted vs experimental residual
  preddf=melt(outdf,id.var="time",variable.name="species",value.name="conc")
  expdf=melt(df,id.var="time",variable.name="species",value.name="conc")
  ssqres=expdf$conc-preddf$conc

  # return predicted vs experimental residual
  return(ssqres)
}



# Parameter fitting using levenberg marquart algorithm

# initial guess for parameters
parms <- runif(2, 0.001, 10.0)
names(parms) <- c("k1", "k2")
# parms <- c(k1=0.5, k2=0.5)
#print(parms)

# fitting
# Is there a better way to retrieve nls.lm.control ?? 
# So far I have to capture the print lines, and then parse them...
#----------
tc <- textConnection("eval_functs_text","w")
sink(tc)

fitval=nls.lm(par=parms,fn=ssq,control=nls.lm.control(nprint=1))

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
  # print(rss)
  
  params <- items[3]
  params <- strsplit(params, "=")[[1]]
  params <- sub("^\\s+", "", params[[2]])
  params <- sub("\\s+", " ", params)
  params <- strsplit(params, " ")[[1]]
  # print(params)

  rbind(report, c(rss, params)) -> report
}

report <- data.frame(report)
names(report) <- c("rss", names(parms))
# print(report)

# Write the output. The output file must be the model name with csv or txt extension.
# Fields must be separated by TAB, and row names must be discarded.
write.table(report, file=report_filename, sep="\t", row.names=FALSE, quote=FALSE)





# # Extract interesting parameters

# print(fitval)
# print(summary(fitval))

# # residual sum-of-square (objective value)
# print(deviance(fitval))

# # Estimated parameter
# parest=as.list(coef(fitval))
# print(parest)



# # Plot predicted vs experimental data (for testing)
# 
# # simulated predicted profile at estimated parameter values
# cinit=c(A=1,B=0,C=0)
# t=seq(0,5,0.2)
# out=ode(y=cinit,times=t,func=my_model,parms=as.list(parest))
# outdf=data.frame(out)
# names(outdf)=c("time","a_pred","b_pred","c_pred")
# 
# # Overlay predicted profile with experimental data
# tmppred=melt(outdf,id.var=c("time"),variable.name="species",value.name="conc")
# tmpexp=melt(df,id.var=c("time"),variable.name="species",value.name="conc")
# p=ggplot(data=tmppred,aes(x=time,y=conc,color=species,linetype=species))+geom_line()
# p=p+geom_line(data=tmpexp,aes(x=time,y=conc,color=species,linetype=species))
# p=p+geom_point(data=tmpexp,aes(x=time,y=conc,color=species))
# p=p+scale_linetype_manual(values=c(0,1,0,1,0,1))
# p=p+scale_color_manual(values=rep(c("red","blue","green"),each=2))+theme_bw()
# print(p)
