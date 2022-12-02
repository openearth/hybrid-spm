library("bmstdr")
library("ncdf4")
library("spTimer")
library('tidyverse')
# basic set up hybrid spm
# input needed for Bsptime (package in bmstdr): 
#   Data structure: 
#     two columns giving the coordinates of the locations
#     Data with n sites and T times within each site should be organised in the order (s1,t1),(s1,t2)
#   using either the spTimer or sptDyn packages OR following the linear equation given in example 2.4
#


#reading datasets 
#

# formula definition -> now taken from example
# input is space -> gridcel number for example
# time
# coordinates
d <- read_delim(file = "P://11206887-012-sito-is-2021-so-et-es/Data/input_bayesian/input_bayesian_mwtl_dfm_cms.csv")
#f2 <- y8hrmax ~ xmaxtemp+xwdsp+xrh
d[1] <- NULL
data <-d
head(data)
f <- mwtl_SPM ~ sat_SPM + dfm_SPM

#Bsptime running 3.2, 3.4 -> example
M3 <- Bsptime(package="spTimer", formula=f, data=data, n.report=5, time.data=1,
              coordtype="lonlat", coords=5:6)
Bsptime()
#selecting validation points

#exploring the separable model according to 3.3

#plotting results /parameter estimations ect



