# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 16:23:05 2022

@author: gwee

Bayesian modelling
* To create a table ready for modelling, first reproject satellite data to dfm model grid
* Then, extract pixel values for all MWTL coordinates across the satellite and model data
* then, create a table of ID, time, lat, lon, MWTL_spm, dfm_spm, sat_spm
"""

import xarray as xr
import pandas as pd
import os
import matplotlib.pyplot as plt

#loading data
cms = xr.open_dataset(
    r"p:\11206887-012-sito-is-2021-so-et-es\Data\CMEMS_Satellite_100mx100m\merged_2015-2020\2015_2020_P1D_HROC_L3-transp_NWS_31_32ULE_100m-v01.nc")
dfm = xr.open_dataset(
    r"p:\11206887-012-sito-is-2021-so-et-es\Scripts\DFM_postprocess\data\input\DWSM-FM_100m_0000_map_regular_2367_1583_allvars_2timesteps.nc")

#combining mwtl locations and mwtl SPM to one tabel
mwtl_loc=pd.read_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\MWTL\MWTL_stations_all.csv')
mwtl_dir=r'P:\11206887-012-sito-is-2021-so-et-es\Data\MWTL\csv_per_station'

mwtl_loc=mwtl_loc.rename(columns={'geometriepunt.x':'lon', 'geometriepunt.y':'lat'})
mwtl=[]

for fname in os.listdir(mwtl_dir):
    f = os.path.join(mwtl_dir, fname)
    name=os.path.splitext(fname)[0]
    station=list(mwtl_loc.loc[mwtl_loc['locatie.code'] == name, 'locatie.code'])
    coords=mwtl_loc.loc[mwtl_loc['locatie.code'] == station[0]]
    spm=pd.read_csv(f)
    spm=spm.rename(columns={name :'SPM'})
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
cms_cut   = cms.sel(time=slice('2017-02-01','2017-12-31'))

#some tests on slice of the data. can be done on all when this works. 
cms1=cms_cut.sel(time=slice('2017-3-01','2017-4-01'))

#interpolating satellite data onto the model data, specifying the type of method
cms_newgrid = cms1.interp(lat = dfmspm.lat, lon = dfmspm.lon, method='nearest')

#plotting
#cms_newgrid.isel(time=5).SPM.plot(vmin=0, vmax=100)

#when saving, add data encoding as explained in merge-cmems.py 

#checking which mwtl data is taken as the same time as the satellite data. #TODO
merge['time_diff'] = abs((merge.Date_time - merge.datetimeUTC).astype('timedelta64[m]')).values
