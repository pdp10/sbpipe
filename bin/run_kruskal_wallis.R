
# To use the test of Kruskal-Wallis simply enter the data, and then organize them into a list:

#test 1
#a = c(1, 5, 8, 17, 16)
#b = c(2, 16, 5, 7, 4)
#c = c(1, 1, 3, 7, 9)
#d = c(2, 15, 2, 9, 7)
#data = list(g1=a, g2=b, g3=c, g4=d)

#test 2
#a = c(100, 100, 100)
#b = c(31, 63, 16)
#c = c(42, 21, 33)
#d = c(98, 57, 119)
#data = list(g1=a, g2=b, g3=c, g4=d)

#test 3
factors <- c("ctrl", "ctrl", "ctrl",
	   "pp242", "pp242", "pp242",
	   "wmn", "wmn", "wmn", 
	   "raptorKD", "raptorKD", "raptorKD")
values <- c(1, 1, 1, 0.02, 0.59, 0.14, 0.26, 0.16, 0.71, 1.05, 1.32, 1.60)
data <- data.frame(factors=factors, values=values)

print(data)


# kruskal-wallis test: three or more unmatched (unpaired) groups. Non-parametric test.
# Now we can apply the kruskal.test() function:

# test 1
#kw <- kruskal.test(data)
#print(kw)
boxplot(data)
# The value of the test statistic is 1.9217. This value already contains the fix when there are ties (repetitions). The p-value is greater than 0.05; also the value of the test statistic is lower than the chi-square-tabulation:
# test 1
#qchisq(0.950, 3)
# The conclusion is therefore that I accept the null hypothesis H0: the means of the 4 groups are statistically equal.


# test 3
kw <- kruskal.test(values~factors, data=data)
print(kw)

#pwt <- pairwise.wilcox.test(values, factors, #p.adj="bonferroni", exact=)
#print(pwt)

my.tukeyhsd <- TukeyHSD(kw)
print(my.tukeyhsd)








