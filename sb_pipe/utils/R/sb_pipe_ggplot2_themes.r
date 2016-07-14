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
# $Date: 2016-7-6 12:14:32 $


library(ggplot2)


# A theme for time courses
tc_theme <- function (base_size=12, base_family="") {
  theme_bw(base_size=base_size, base_family=base_family) %+replace% 
  theme(aspect.ratio=0.5,
        axis.line = element_line(colour = "black", size=1.0),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
	panel.border = element_rect(colour = "black", fill=NA, size=1.5),
        panel.background = element_blank(),
	legend.key = element_rect(fill = "transparent", colour = "transparent"),        
        legend.background = element_rect(fill = "transparent", colour = "transparent"),
        plot.background = element_rect(fill = "transparent",colour = NA)
        )
}


# A basic theme
basic_theme <- function (base_size=12, base_family="") {
  theme_bw(base_size=base_size, base_family=base_family) %+replace% 
  theme(aspect.ratio=1,
        axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
	panel.border = element_rect(colour = "black", fill=NA, size=1.5),
        panel.background = element_blank(),
	legend.key = element_rect(fill = "transparent", colour = "transparent"),        
        legend.background = element_rect(fill = "transparent", colour = "transparent"),
        plot.background = element_rect(fill = "transparent", colour = NA)        
        )
}