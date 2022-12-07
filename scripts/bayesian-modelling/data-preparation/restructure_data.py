import pandas as pd
from pyproj import Proj
from pyproj import CRS
from pyproj import Transformer

df = pd.read_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_bayesian_mwtl_dfm_cms_finermodelgrid.csv')

def label_station (row):
   if row['station'] == 'ROTTMPT3' :
      return 1
   if row['station'] == 'HUIBGOT' :
      return 2
   if row['station'] == 'GROOTGND' :
      return 3

df['s.index'] = df.apply(lambda row: label_station(row), axis=1)

df['year'] = pd.to_datetime(df['Time']).dt.year
df['month'] = pd.to_datetime(df['Time']).dt.month
df['day'] = pd.to_datetime(df['Time']).dt.day

df=df.drop(columns=['Unnamed: 0', 'station', 'Time'])

myProj = Proj("+proj=utm +zone=32 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

to_crs = CRS.from_proj4("+proj=utm +zone=32 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
from_crs = CRS.from_epsg(4326)

proj = Transformer.from_crs(from_crs, to_crs, always_xy=True)
UTM = proj.transform(df.lat, df.lon)
df['UTMx']=pd.Series(UTM[0])
df['UTMy']=pd.Series(UTM[1])

cols=['s.index', 'UTMx', 'UTMy' ,'lon', 'lat','year',
       'month', 'day', 'sat_SPM', 'dfm_SPM', 'mwtl_SPM']

df = df[cols]

df.to_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_bayesian_mwtl_dfm_cms_finemodelgrid_restructured.csv', index=False)