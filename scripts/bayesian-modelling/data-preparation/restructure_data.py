# %%
import pandas as pd
from pyproj import Proj
from pyproj import CRS
from pyproj import Transformer
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt, dates as mdates

df = pd.read_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_bayesian_mwtl_dfm_cms_finermodelgrid.csv')

def label_station (row):
   if row['station'] == 'ROTTMPT3' :
      return 1
   if row['station'] == 'HUIBGOT' :
      return 2
   if row['station'] == 'GROOTGND' :
      return 3

df['s.index'] = df.apply(lambda row: label_station(row), axis=1)

df.sort_values(['s.index', 'Time'], ascending=[True, True])
myProj = Proj("+proj=utm +zone=32 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

to_crs = CRS.from_proj4("+proj=utm +zone=32 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
from_crs = CRS.from_epsg(4326)

proj = Transformer.from_crs(from_crs, to_crs, always_xy=True)
UTM = proj.transform(df.lat, df.lon)
df['UTMx']=pd.Series(UTM[0])
df['UTMy']=pd.Series(UTM[1])

start=pd.to_datetime('2017-01-01')
end=pd.to_datetime('2017-12-31')

df['year'] = pd.to_datetime(df['Time']).dt.year
df['month'] = pd.to_datetime(df['Time']).dt.month
df['day'] = pd.to_datetime(df['Time']).dt.day

#df=df.drop(columns=['Time'])
dti=pd.DataFrame()
df['Time']=pd.to_datetime(df['Time'])
dti['time'] = pd.date_range(start, end, freq="D")
dti['time'] = dti['time'].dt.date
df['time'] = df['Time'].dt.date

s1= df.loc[df['s.index'] == 1]
s2= df.loc[df['s.index'] == 2]
s3= df.loc[df['s.index'] == 3]

df=df.sort_values(['s.index', 'time'], ascending=[True, True])
#df=df.drop(columns=['time'])

cols=['s.index', 'UTMx', 'UTMy' ,'lon', 'lat','time', 'year','month', 'day', 'sat_SPM', 'dfm_SPM', 'mwtl_SPM']
df=df[cols]

#df.to_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_bayesian.csv', index=False)

# %%
ax = plt.gca()
plt.rcParams["figure.figsize"] = [12, 4]
plt.rcParams["figure.autolayout"] = True
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.scatter(df['time'], df['mwtl_SPM'], label='MWTL')
ax.scatter(df['time'], df['sat_SPM'], label='Satellite')
ax.scatter(df['time'], df['dfm_SPM'], label='Model')
ax.set_ylabel('SPM concentration')
ax.set_xlabel('Time')

plt.legend(loc="upper left")
plt.title('SPM concentrations of MWTL, satellite and model at HUIBGOT, GROOTGND and ROTTMPT3')
plt.show()
# %%
d=pd.merge(df,dti,on='time',how='outer')
# %% prepping input data
d=d.sort_values(by='Time')
cols=['Time', 's.index', 'UTMx', 'UTMy' ,'lon', 'lat','time','year', 'month','day', 'sat_SPM', 'dfm_SPM', 'mwtl_SPM']
d['year'] = pd.to_datetime(d['time']).dt.year
d['month'] = pd.to_datetime(d['time']).dt.month
d['day'] = pd.to_datetime(d['time']).dt.day


d = d[cols]
d.to_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_restructuredAll.csv', index=False)

 #%% DOWN BELOW IS TESTING STUFF
"""
df['year'] = pd.to_datetime(df['Time']).dt.year
df['month'] = pd.to_datetime(df['Time']).dt.month
df['day'] = pd.to_datetime(df['Time']).dt.day
"""
s1 = s1[cols]

ds2=pd.DataFrame()
df['Time']=pd.to_datetime(df['Time'])
ds2['time'] = pd.date_range(start, end, freq="D")
ds2['time'] = ds2['time'].dt.date

dti['lon']=s1['lon'][0]
dti['lat']=s1['lat'][0]
dti['s.index']=s1['s.index'][0]
dti['UTMx']=s1['UTMx'][0]
dti['UTMy']=s1['UTMy'][0]

dti['sat_SPM']=np.random.randint(1, 6, dti.shape[0])
dti['dfm_SPM']=np.random.randint(1, 6, dti.shape[0])
dti['mwtl_SPM']=np.random.randint(1, 6, dti.shape[0])

dti['year'] = pd.to_datetime(dti['time']).dt.year
dti['month'] = pd.to_datetime(dti['time']).dt.month
dti['day'] = pd.to_datetime(dti['time']).dt.day

#dd=pd.concat([dti,ds2])

dti=dti.sort_values(['s.index', 'time'], ascending=[True, True])
dti=dti.drop(columns=['time'])

cols=['s.index', 'UTMx', 'UTMy' ,'lon', 'lat', 'sat_SPM', 'dfm_SPM', 'mwtl_SPM']
dti=dti[cols]
dti.to_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_restructured_dummy.csv', index=False)

# %% TESTING STUFFF
dti=pd.DataFrame()

df['time'] = pd.to_datetime(df['Time'])
dti['time'] = pd.date_range(start, end, freq="D")
dti['time'] = dti['time'].dt.date
df['time'] = df['time'].dt.date

      # %%
df=df.drop(columns=['Unnamed: 0', 'station'])

# %%
d=pd.merge(df,dti,on='time',how='outer')

d['year'] = pd.to_datetime(d['Time']).dt.year
d['month'] = pd.to_datetime(d['Time']).dt.month
d['day'] = pd.to_datetime(d['Time']).dt.day

d=d.sort_values(by='time')
d=d.drop(columns=['Time'])

cols=['s.index', 'UTMx', 'UTMy' ,'lon', 'lat','year', 'month','day', 'sat_SPM', 'dfm_SPM', 'mwtl_SPM','time']

d = d[cols]

# %%
d.to_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_restructured_time.csv', index=False)
# %%
