# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Plotting of time courses columns wrt time. 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-11-16 12:14:32 $
# $Id: param_scan__sim_parameter_scan.R,v 3.0 2010-11-16 19:45:32 Piero Dalle Pezze Exp $



# to use string replace
library(stringr)     
library(ggplot2)

# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(paste(SB_PIPE, "/sb_pipe/utils/R/matrices.R", sep=""))




tc_theme <- function (base_size=12, base_family="") {
  theme_bw(base_size=base_size, base_family=base_family) %+replace% 
  theme(aspect.ratio=0.5,
        axis.line = element_line(colour = "black", size=1.0),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(), 
        plot.background = element_rect(fill = "transparent",colour = NA))
}





plot_single_perturbation_data <- function(model_noext, species, inhibition_only, results_dir, dataset_parameter_scan_dir, tc_parameter_scan_dir, simulate__xaxis_label, param_scan__single_perturb_simulations_number, perturbation_in_percent_levels) {
    
    
    writeLines(paste("Model: ", model_noext, ".cps", sep=""))
    writeLines(paste("Perturbed species: ", species, sep=""))
    #writeLines(results_dir)
    # variables
    inputdir <- c ( paste(results_dir, "/", dataset_parameter_scan_dir, "/", sep="" ) )
    outputdir <- c ( paste(results_dir, "/", tc_parameter_scan_dir, "/", sep="" ) )
    #writeLines(inputdir)
    #writeLines(outputdir)
    

    theme_set(tc_theme(28))    
    
    for(k_sim in 1:param_scan__single_perturb_simulations_number) {    
    
	  
	  files <- list.files( path=inputdir, pattern=paste(model_noext, '__sim_', k_sim, sep=""))
	  levels <- c()
	  levels.index <- c()

	  # create the directory of output
	  if (!file.exists(outputdir)){ dir.create(outputdir) }
	  
	  
	  # the array files MUST be sorted. Required to convert the string into numeric.
	  # this is important because the legend must represent species's knockdown in order.
	  for(i in 1:length(files)) {
	      num_of_underscores <- length(gregexpr("_", files[i])[[1]])
	      levels <- c(levels, as.numeric(str_replace( strsplit( files[i], "_")[[1]][num_of_underscores + 1], ".csv", "")))
	  }
	  levels.temp <- c(levels)
	  newmax <- max(levels)+1
	  for(i in 1:length(levels)) {
	    min <- which.min(levels.temp)
	    #writeLines(min(levels.temp))
	    levels.index <- c(levels.index, min)
	    levels.temp[min] <- newmax
	  }
	  #writeLines(levels)
	  # sort by decreasing order
	  #writeLines(files)
	  #writeLines(levels)
	  #writeLines(levels.index)
	  levels <- sort(levels)

	  # Read species
	  timecourses <- read.table ( paste ( inputdir, files[1], sep="" ), header=TRUE, na.strings="NA", dec=".", sep="\t" )
	  column <- names ( timecourses )

	  #writeLines(levels)
	  #writeLines(levels.index)

	  # Load files in memory
	  dataset <- load_files_in_matrix_wlevels(inputdir, files, levels.index)

	  levels <- paste(species, levels, sep=" ")
	  writeLines(levels)

          

	  colors <- c()
	  linetype <- c()
	  
	  if(perturbation_in_percent_levels == "true") {
	    # The model is perturbed using a virtual species (A_percent_level) defining the percent level of its corresponding real species (A). 
	    # The perturbation is therefore done by percent levels and at the beginning.
	    # NOTE: A_percent_level=0  ==> A is knocked out (so 0%)
	    if(inhibition_only == "true") {
	      # THIS PALETTE OF COLOURS can be used for gradual inhibition only (blue [10,100])
	      # Including knockout (first number is knock out (bright blue), last number 24 is control (black))  (0%,10%,20%,..,100%)
	      # In linetype: 1 is a full line	    
	      #colors <- colors()[c(128,129,130,131,132,26,27,28,29,30,24)] 
	      #linetype <- c(1,6,4,3,2,1,6,4,3,2,1)
	      # Excluding knockout (10%,20%,..,100%)
	      colors <- colors()[c(129,130,131,132,26,27,28,29,30,24)]
	      linetype <- c(1,4,3,2,1,6,4,3,2,1)
	    } else {
	      # THIS PALETTE OF COLOURS can be used for gradual inhibition and overexpression (blue [10,250])	  
	      # Including knockout (first number is knock out (bright blue), last number 96 is control (overexpression))  (0%,25%,50%,..,100%,125%,150%,..250%)
	      # In linetype: 1 is a full line	    
	      #colors <- colors()[c(27,28,29,30,24,99,115,95,98,97,96)]
	      #linetype <- c(5,4,3,2,1,6,5,4,3,2,6)
	      # Excluding knockout (25%,50%,..,100%,125%,150%,..,250%)	    
	      colors <- colors()[c(28,29,30,24,99,115,95,98,97,96)]
	      linetype <- c(4,3,2,1,6,5,4,3,2,6)
	    }
	  } else {
	    # The model is perturbed using a virtual species (A_inhibitor) inhibiting its corresponding real species (A). 
	    # In this case, the perturbation is on the inhibitor or expressor, and NOT on the species. In this case, the perturbation is done all over the time course.
	    # NOTE 1: A_inhibitor=0  ==> A is not perturbed (so 100%)	    
	    # NOTE 2: This case requires a preliminary approximation of the percentage of inhibited/expressed protein, and assume that this percentage is linear to the inhibitor/expressor.
	    # NOTE 3: In this case, inhibition and overexpression are two separate perturbation. Although semantically incorrect, the second branch of the if-then-else clausole represents overexpression only.
	    if(inhibition_only == "true") {
	      # THIS PALETTE OF COLOURS can be used for gradual inhibition only (blue [10,100])
	      # First number is 24 is control (black), last number (bright blue))  (100%,90%,80%,..,10%)
	      # In linetype: 1 is a full line	    
	      colors <- colors()[c(24,30,29,28,27,26,132,131,130,129)]
	      linetype <- c(1,2,3,4,6,1,2,3,4,1)
	    } else {
	      # THIS PALETTE OF COLOURS can be used for gradual overexpression (magenta [100,250])	  
	      # First number is control (black), last number 96 is overexpression (magenta) (100%,115%,130%,..250%)
	      # In linetype: 1 is a full line
	      colors <- colors()[c(24,99,115,95,98,97,96,464,463,510)]
	      linetype <- c(1,2,3,4,1,2,3,4,6,1)
	    }
	  }
	  
	  # let's plot now! :)
	  # NOTE: a legend is not added. To create one, the color (and linetype) must be inside aes. 
	  # For each line they need to receive 
	  for(j in 2:length(column)) {
   	    g <- ggplot()
	    for(m in 1:length(files)) {
		df <- data.frame(a=dataset[,1,1], b=dataset[,j,m])
		g <- g + geom_line(data=df, 
				   aes(x=a, y=b), color=colors[m], linetype=linetype[m], size=1.0)
	    }	    
	    
	    g <- g + xlab(simulate__xaxis_label) + ylab(paste(column[j], " level [a.u.]", sep="")) 	    
      	    ggsave(paste(outputdir, model_noext, "__eval_", column[j], "__sim_", k_sim, ".png", sep="" ), 
		   dpi=300,  width=8, height=6, bg = "transparent") 
   
	  }
	  
  }
  
}
