# install.packages("plyr")
# install.packages("esc")
# install.packages("EValue")

library(plyr)
library(esc)
library(EValue)

setwd("./data/proc")

# write output to file: comment out if printing to console
sink('evalues.txt', append=FALSE, split=FALSE)

# ----- BIOS1168 -----
df <- read.csv('bios1168_clean_.csv', header=TRUE, sep=',', na.strings=c('', '.', 'NA'))

# get summary stats
cdf <- ddply(df, c("group"), summarise,
             N = length(ese_100_percent),
             mean = mean(ese_100_percent, na.rm=TRUE),
             sd   = sd(ese_100_percent, na.rm=TRUE),
             se   = sd / sqrt(N))

# linear model
md <- lm(ese_100_percent ~ group, data=df)

# get Cohen's d standardised mean difference and SE for E value
# esc calculates difference as grp1m - grp2m
smd <- esc_mean_se(grp2m = cdf$mean[c(1)], grp2se = cdf$se[c(1)], grp2n = cdf$N[c(1)],
                   grp1m = cdf$mean[c(2)], grp1se = cdf$se[c(2)], grp1n = cdf$N[c(2)],
                   es.type = "d")

# compute evalue
eval <- evalues.MD(est=smd$es, se=smd$se)

cat("\n================================================================\n")
cat("BIOS1168 End-semester mark: Cohen's d")
cat("\n================================================================\n")
print(smd)

cat("\n================================================================\n")
cat("E value")
cat("\n================================================================\n")
print(eval)

# ----- BIOS5090 -----
df <- read.csv('bios5090_clean_.csv', header=TRUE, sep=',', na.strings=c('', '.', 'NA'))

# get summary stats
cdf <- ddply(df, c("group"), summarise,
             N = length(ese_100_percent),
             mean = mean(ese_100_percent, na.rm=TRUE),
             sd   = sd(ese_100_percent, na.rm=TRUE),
             se   = sd / sqrt(N))

# linear model
md <- lm(ese_100_percent ~ group, data=df)

# get Cohen's d standardised mean difference and SE for E value
# esc calculates difference as grp1m - grp2m
smd <- esc_mean_se(grp2m = cdf$mean[c(1)], grp2se = cdf$se[c(1)], grp2n = cdf$N[c(1)],
                   grp1m = cdf$mean[c(2)], grp1se = cdf$se[c(2)], grp1n = cdf$N[c(2)],
                   es.type = "d")

# compute evalue
eval <- evalues.MD(est=smd$es, se=smd$se)

cat("\n================================================================\n")
cat("BIOS5090 End-semester mark: Cohen's d")
cat("\n================================================================\n")
print(smd)

cat("\n================================================================\n")
cat("E value")
cat("\n================================================================\n")
print(eval)

# close file
sink()