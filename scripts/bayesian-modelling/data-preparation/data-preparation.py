# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 16:23:05 2022

@author: gwee, dees

Bayesian modelling
* To create a table ready for modelling, first reproject satellite data to dfm model grid
* Then, extract pixel values for all MWTL coordinates across the satellite and model data
* then, create a table of ID, time, lat, lon, MWTL_spm, dfm_spm, sat_spm
"""

import xarray as xr
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime

#loading data
from sys import platform
if platform == 'linux':
    cms = xr.open_dataset(
        r"/p/11206887-012-sito-is-2021-so-et-es/Data/CMEMS_Satellite_100mx100m/merged_2015-2020/2015_2020_P1D_HROC_L3-transp_NWS_31_32ULE_100m-v01.nc")
    dfm = xr.open_dataset(
        r"/p/11206887-012-sito-is-2021-so-et-es/Data/DFM_DWSM-FM_100m/Postprocessing_maps/DWSM-FM_100m_0000_map_regular_500_400_allvars.nc")
    opath = r"/p/11206887-012-sito-is-2021-so-et-es/Data/interpolated_CMS/CMS_interpolated_to_DFMgrid.nc"
    mwtl_loc=pd.read_csv(r'/p/11206887-012-sito-is-2021-so-et-es/Data/MWTL/MWTL_stations_all.csv')
    mwtl_dir=r'/p/11206887-012-sito-is-2021-so-et-es/Data/MWTL/csv_per_station'
else:
    cms = xr.open_dataset(
        r"p:\11206887-012-sito-is-2021-so-et-es\Data\CMEMS_Satellite_100mx100m\merged_2015-2020\2015_2020_P1D_HROC_L3-transp_NWS_31_32ULE_100m-v01.nc")
    dfm = xr.open_dataset(
        r"P:\11206887-012-sito-is-2021-so-et-es\Data\DFM_DWSM-FM_100m\Postprocessing_maps\DWSM-FM_100m_0000_map_regular_500_400_allvars.nc")
    opath = r"P:\11206887-012-sito-is-2021-so-et-es\Data\interpolated_CMS\CMS_interpolated_to_DFMgrid.nc"
    mwtl_loc=pd.read_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\MWTL\MWTL_stations_all.csv')
    mwtl_dir=r'P:\11206887-012-sito-is-2021-so-et-es\Data\MWTL\csv_per_station'


#combining mwtl locations and mwtl SPM to one tabel
mwtl_loc=mwtl_loc.rename(columns={'geometriepunt.x':'lon', 'geometriepunt.y':'lat'})
mwtl=[]

for fname in os.listdir(mwtl_dir):
    f = os.path.join(mwtl_dir, fname)
    name=os.path.splitext(fname)[0]
    station=list(mwtl_loc.loc[mwtl_loc['locatie.code'] == name, 'locatie.code'])
    coords=mwtl_loc.loc[mwtl_loc['locatie.code'] == station[0]]
    spm=pd.read_csv(f)
    spm=spm.rename(columns={name :'mwtl_SPM'})
    spm['Time'] = pd.to_datetime(spm['Time'],format='%Y-%m-%d %H:%M:%S')
    spm['station'] = coords['locatie.code'].iloc[0]
    spm['lon'] = coords['lon'].iloc[0]
    spm['lat'] = coords['lat'].iloc[0]
    mwtl.append(spm)

mwtl = pd.concat(mwtl)

#grid reprojection
dfmspm = dfm.isel(time=0,layer=0).drop(['time','layer'])
#dfmspm = dfm.drop(['layer']).mesh2d_water_quality_output_9

# cutting to only 2017 # cutting out januari as well as it has a lot of nan data 
cms_cut   = cms.sel(time=slice('2017-01-01','2017-12-31'))

#some tests on slice of the data. can be done on all when this works. 
#cms1=cms_cut.sel(time=slice('2017-3-01','2017-4-01'))

#interpolating satellite data onto the model data, specifying the type of method
cms_newgrid = cms_cut.interp(lat = dfmspm.lat, lon = dfmspm.lon, method='nearest')

#plotting an example of the interpolated gridconda 
#cms_newgrid.isel(time=5).SPM.plot(vmin=0, vmax=100)

#saving data
#when saving, add data encoding as explained in merge-cmems.py 
# [cms.SPM.encoding.pop(b) for b in ['szip', 'zstd', 'bzip2', 'blosc']]
# [cms.lon.encoding.pop(b) for b in ['szip', 'zstd', 'bzip2', 'blosc']]
# [cms.lat.encoding.pop(b) for b in ['szip', 'zstd', 'bzip2', 'blosc']]
# [cms.time.encoding.pop(b) for b in ['szip', 'zstd', 'bzip2', 'blosc']]
cms_newgrid.to_netcdf(
    opath, 
    # encoding={
    #     'lat': cms.lat.encoding, 'lon': cms.lon.encoding, 
    #     'time': cms.time.encoding, 'SPM': cms.SPM.encoding
    #     }
    )

sel = cms_newgrid.isel(time=51).where(
    ((cms_newgrid.lat <= cms.lat.max()) & (cms_newgrid.lat >= cms.lat.min()) \
    & (cms_newgrid.lon <= cms.lon.max()) & (cms_newgrid.lon >= cms.lon.min())),drop=True)



# #checking which mwtl data is taken as the same time as the satellite data. #TODO
# mwtl = mwtl[mwtl['Time'].dt.year == 2017]
# #mwtl=mwtl[mwtl['Time'].dt.hour.between(9,12)]
# mwtl = mwtl.sort_values(by='Time', ascending=True)
# #mwtl_date=mwtl['Time'].dt.date

# def satspm(ee):
#     mth = pd.Series(ee.Time).dt.month.values[0]
#     time = ee.Time
#     lat = ee.lat
#     lon = ee.lon
#     varspm = cms_newgrid.sel(time = cms_newgrid.time.dt.month == mth).mean(dim='time')

#     spm = varspm.sel(lat=lat, lon=lon,method='nearest').SPM.values.flatten()[0]
    
#     ee['sat_SPM'] = spm
#     # ee['sat_time'] = cms.sel(time=time, lat=lat, lon=lon,method='nearest').time.values
#     # ee['sat_lon'] = cms.sel(time=time, lat=lat, lon=lon,method='nearest').lon.values
#     #ee['sat_lat'] = cms.sel(time=time, lat=lat, lon=lon,method='nearest').lat.values

#     return ee

# def dfmspm_func(ee):
#     time = ee.Time
#     lat = ee.lat
#     lon = ee.lon

#     spm = dfmt.sel(time=time, lat=lat, lon=lon,method='nearest').mesh2d_water_quality_output_9.values.flatten()[0]
    
#     ee['dfm_SPM'] = spm
#     # ee['sat_time'] = cms.sel(time=time, lat=lat, lon=lon,method='nearest').time.values
#     # ee['sat_lon'] = cms.sel(time=time, lat=lat, lon=lon,method='nearest').lon.values
#     #ee['sat_lat'] = cms.sel(time=time, lat=lat, lon=lon,method='nearest').lat.values

#     return ee

# #create monthly aggregated
# for m in range(1,13):
#     cms_m = cms_newgrid.sel(time=cms_newgrid.time.dt.month == m).mean(dim='time')
    
# dfmt = dfm.isel(layer=0).drop(['layer'])

# dd = mwtl.apply(satspm,axis=1)
# tt = dd[~dd.sat_SPM.isna()]
# tt=tt[~tt.mwtl_SPM.isna()]

# df = tt.apply(dfmspm_func,axis=1)
# df.reset_index(drop=True,inplace=True)

# #df.to_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_bayesian_mwtl_dfm_cms.csv')


# #merge['time_diff'] = abs((merge.Date_time - merge.datetimeUTC).astype('timedelta64[m]')).values
