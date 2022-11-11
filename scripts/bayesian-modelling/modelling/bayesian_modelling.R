library("bmstdr")
library("ncdf4")
library("spTimer")

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
f2 <- y8hrmax ~ xmaxtemp+xwdsp+xrh
f <- mwtl ~ time + spmmodel + spmsatellite

#Bsptime running 3.2, 3.4 -> example
M3 <- Bsptime(package="spTimer", formula=f2, data=nysptime, n.report=5, 
              coordtype="utm", coords=4:5)

#selecting validation points

#exploring the separable model according to 3.3

#plotting results /parameter estimations ect



