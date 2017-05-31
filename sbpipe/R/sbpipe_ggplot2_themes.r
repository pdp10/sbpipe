# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Plotting of time courses columns wrt time. 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-7-6 12:14:32 $


library(ggplot2)


# A theme for time courses. It extends ggplot2 theme_classic.
#
# :param base_size: the font size
# :param base_family: the font family
tc_theme <- function (base_size=12, base_family="") {
  theme_classic(base_size=base_size, base_family=base_family) %+replace% 
  theme(aspect.ratio = 0.5,
        axis.line = element_line(colour="black", size=1.0),
        axis.text.x=element_text(angle=-45, hjust=0, vjust=0.8),
        panel.border = element_rect(colour = "black", fill=NA, size=1.5),
        legend.key = element_rect(fill = "transparent", colour = "transparent"),
        legend.background = element_rect(fill = "transparent", colour = "transparent"),
        plot.background = element_rect(fill = "transparent",colour = NA),
        plot.margin = unit(c(0.5,0.5,0.8,0.5), "in")
        )
}


# A generic basic theme for time courses. It extends ggplot2 theme_classic.
#
# :param base_size: the font size
# :param base_family: the font family
basic_theme <- function (base_size=12, base_family="") {
  theme_classic(base_size=base_size, base_family=base_family) %+replace% 
  theme(aspect.ratio = 1,
        axis.line = element_line(colour = "black", size=1.0),
        axis.text.x=element_text(angle=-45, hjust=0, vjust=0.8),
        panel.border = element_rect(colour = "black", fill=NA, size=1.5),
        legend.key = element_rect(fill = "transparent", colour = "transparent"),
        legend.background = element_rect(fill = "transparent", colour = "transparent"),
        plot.background = element_rect(fill = "transparent", colour = NA)
        )
}

