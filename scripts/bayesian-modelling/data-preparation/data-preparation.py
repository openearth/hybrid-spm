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

# cutting to only 2017 
cms_cut   = cms.sel(time=cms.time.dt.year == 2017)

#some tests #TODO for next time take out first part of the 2017 data as they contain a lot of nans. Investigate and then interpolate over another month (March or so) 
cms1=cms_cut.isel(time=1)

#interpolating satellite data onto the model data
cms_newgrid1 = cms1.interp(lat = dfmspm.lat, lon = dfmspm.lon)

#checking which mwtl data is taken as the same time as the satellite data. #TODO
merge['time_diff'] = abs((merge.Date_time - merge.datetimeUTC).astype('timedelta64[m]')).values
