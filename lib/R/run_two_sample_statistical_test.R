# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $



# CASE 1
#a = c(175, 168, 168, 190, 156, 181, 182, 175, 174, 179)
#b = c(185, 169, 173, 173, 188, 186, 175, 174, 179, 180)
#n = 10

# CASE 2 (Raptor KD)
a = c(106, 92, 123)
b = c(100, 100, 100)
n = 3

# CASE 3 (Rictor KD)
a = c(50, 25, 24)
b = c(100, 100, 100)
n = 3



# To solve this problem we must use to a Student's t-test with two samples, assuming that the two samples are taken from populations that follow a Gaussian distribution (if we cannot assume that, we must solve this problem using the non-parametric test called Wilcoxon-Mann-Whitney test; we will see this test in a future post). Before proceeding with the t-test, it is necessary to evaluate the sample variances of the two groups, using a Fisher's F-test to verify the homoskedasticity (homogeneity of variances). In R you can do this in this way:

# CASE 1-2
var.test(a,b);



# We obtained p-value greater than 0.05, then we can assume that the two variances are homogeneous. Indeed we can compare the value of F obtained with the tabulated value of F for alpha = 0.05, degrees of freedom of numerator = 9, and degrees of freedom of denominator = 9, using the function qf(p, df.num, df.den):

# CASE 1
qf(0.95, n-1, n-1)



# Note that the value of F computed is less than the tabulated value of F, which leads us to accept the null hypothesis of homogeneity of variances.
# NOTE: The F distribution has only one tail, so with a confidence level of 95%, p = 0.95. Conversely, the t-distribution has two tails, and in the R's function qt(p, df) we insert a value p = 0.975 when you're testing a two-tailed alternative hypothesis.
# Then call the function t.test for homogeneous variances (var.equal = TRUE) and independent samples (paired = FALSE: you can omit this because the function works on independent samples by default) in this way:

# CASE 1
#t.test(a,b, var.equal=TRUE, paired=FALSE)

# CASE 2
t.test(a,b, var.equal=FALSE)


#We obtained p-value greater than 0.05, then we can conclude that the averages of two groups are significantly similar. Indeed the value of t-computed is less than the tabulated t-value for 18 degrees of freedom, which in R we can calculate:

# CASE 1
qt(0.975, (n-1)*2)


# This confirms that we can accept the null hypothesis H0 of equality of the means.



# Wilcoxon-Mann-Whitney test (non-parametric; paired groups) 

wilcox.test(a,b, paired=TRUE)



# Wilcoxon-Mann-Whitney test (non-parametric; unpaired groups) 

wilcox.test(a,b, correct=FALSE, paired=FALSE)


