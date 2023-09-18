library("bmstdr")
library("ncdf4")
library("spTimer")
library('tidyverse')
library('ggsn')
library('ggmap')
library('akima')
library('ggplot2')
library('tidyr')

#map <- map_data("netherlands")
# basic set up hybrid spm
# input needed for Bsptime (package in bmstdr): 
#   Data structure: 
#     two columns giving the coordinates of the locations
#     Data with n sites and T times within each site should be organised in the order (s1,t1),(s1,t2)
#   using either the spTimer or sptDyn packages OR following the linear equation given in example 2.4
#
train <-read_delim(file = "P://11206887-012-sito-is-2021-so-et-es/Data/input_bayesian/input_bayesian.csv")
dummy <-read_delim(file="P://11206887-012-sito-is-2021-so-et-es/Data/input_bayesian/input_bayesian_mwtl_dfm_cms_finemodelgrid_restructured.csv")
f <- mwtl_SPM ~ sat_SPM + dfm_SPM

# Sort the dataframe based on the 'Age' column
sorted_data <- train %>%
  arrange(s.index)

#reading datasets 
# formula definition -> now taken from example
# input is space -> gridcel number for example, time, coordinates

subset<-head(train,20)
M1 <- Bsptime(model="lm", formula=f, data=sorted_data, scale.transform = "SQRT")

M2 <- Bspatial(model="separable", formula=f, data=sorted_data, 
             coordtype="lonlat", coords=4:5, phi=0.4)

M3 <- Bsptime(package="separable", formula=f, data=sorted_data, coords=,c("UTMx","UTMy"), scale.transform="SQRT",
              coordtype="utm",n.report=5, time.data=sorted_data[,6])



sitemeans <- function(a, sn, tn=62) { 
  u <- matrix(a, nrow=sn, ncol=tn, byrow=T)
  b <- apply(u, 1, mean)
  as.vector(b)
}

post <- M1$fit

gpred <- predict(model, newdata=train, newcoords=~Longitude+Latitude)

#selecting validation points
gpred <- predict(post, newdata=grid_sat_dfm, newcoords=~Longitude+Latitude)
u <- gpred$pred.samples
v <- apply(u, 2, sitemeans, sn=100)
a <- get_parameter_estimates(t(v)) 
b <- data.frame(grid_sat_dfm[, 1:5], a) 
meanmat <- post$op
sig2eps <-  post$sig2ep
sige <- sqrt(sig2eps)
itmax <- ncol(meanmat)
nT <- nrow(train)
sigemat <- matrix(rep(sige, each=nT), byrow=F, ncol=itmax)
a <- matrix(rnorm(nT*itmax), nrow=nT, ncol=itmax)
ypreds <- meanmat + a * sigemat
ypreds <-  (ypreds)^2
v <- apply(ypreds, 2, sitemeans, sn=28)
a <- get_parameter_estimates(t(v)) 
fits <- data.frame(train[, 1:5], a)
b <- rbind(b, fits)
coord <- nyspatial[, c("Longitude","Latitude")]

xo <- seq(from=min(coord$Longitude)-0.5, to = max(coord$Longitude)+0.8, length=200)
yo <- seq(from=min(coord$Latitude)-0.25, to = max(coord$Latitude)+0.8, length=200)
surf <- interp(b$Longitude, b$Latitude, b$mean,  xo=xo, yo=yo)
v <- fnc.delete.map.XYZ(xyz=surf)

interp1 <- data.frame(long = v$x, v$z )
names(interp1)[1:length(v$y)+1] <- v$y

interp1 <- gather(interp1,key = lat,value =Predicted,-long,convert = TRUE)

nymap <- map_data(database="state",regions="new york")

zr <- range(interp1$Predicted, na.rm=T)
P <- ggplot() +  
  geom_raster(data=interp1, aes(x = long, y = lat,fill = Predicted)) +
  geom_polygon(data=nymap, aes(x=long, y=lat, group=group), color="black", size = 0.6, fill=NA) + 
  geom_point(data=coord, aes(x=Longitude,y=Latitude))  +
  stat_contour(data=na.omit(interp1), aes(x = long, y = lat,z = Predicted), colour = "black", binwidth =2) +
  scale_fill_gradientn(colours=colpalette, na.value="gray95", limits=zr) +
  theme(axis.text = element_blank(), axis.ticks = element_blank()) +
  ggsn::scalebar(data =interp1, dist = 100, location = "bottomleft", transform=T, dist_unit = "km", st.dist = .05, st.size = 5, height = .06, st.bottom=T, model="WGS84") +
  ggsn::north(data=interp1, location="topleft", symbol=12) +
  labs(x="Longitude", y = "Latitude", size=2.5) 
P

#exploring the separable model according to 3.3




