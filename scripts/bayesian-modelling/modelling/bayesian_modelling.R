library("bmstdr")
library("ncdf4")
library("spTimer")
library('tidyverse')
library('ggsn')
library('ggmap')

#map <- map_data("netherlands")
# basic set up hybrid spm
# input needed for Bsptime (package in bmstdr): 
#   Data structure: 
#     two columns giving the coordinates of the locations
#     Data with n sites and T times within each site should be organised in the order (s1,t1),(s1,t2)
#   using either the spTimer or sptDyn packages OR following the linear equation given in example 2.4
#


#reading datasets 
# formula definition -> now taken from example
# input is space -> gridcel number for example, time, coordinates
#d <- read_delim(file = "P://11206887-012-sito-is-2021-so-et-es/Data/input_bayesian/input_bayesian_mwtl_dfm_cms_finemodelgrid_restructured.csv")

#df <- read_delim(file = "P://11206887-012-sito-is-2021-so-et-es/Data/input_bayesian/input_restructured.csv")

#dt <- read_delim(file = "P://11206887-012-sito-is-2021-so-et-es/Data/input_bayesian/input_restructured_space_time.csv")

dummy <-read_delim(file = "P://11206887-012-sito-is-2021-so-et-es/Data/input_bayesian/input_restructured_dummy.csv")
f <- mwtl_SPM ~ sat_SPM + dfm_SPM

#Bsptime running 3.2, 3.4 -> example
M1 <- Bsptime(model="lm", formula=f, data=dummy, scale.transform = "SQRT")
a <- residuals(M1)

M2 <- Bspatial(model="spat", formula=f, data=dummy, 
               coordtype="lonlat", coords=4:5, phi=0.4)

M3 <- Bsptime(package="spTimer", formula=f, data=dummy, coords=,c("UTMx","UTMy"), scale.transform="SQRT",
              coordtype="utm",n.reports=5)

#selecting validation points

#exploring the separable model according to 3.3

fx<-nyspatial
#plotting results /parameter estimations ect



