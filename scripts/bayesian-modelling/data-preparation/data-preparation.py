# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 16:23:05 2022

@author: gwee
"""

import xarray as xr


cms = xr.open_dataset(
    r"p:\11206887-012-sito-is-2021-so-et-es\Data\CMEMS_Satellite_100mx100m\merged_2015-2020\2015_2020_P1D_HROC_L3-transp_NWS_31_32ULE_100m-v01.nc")
dfm = xr.open_dataset(
    r"p:\11206887-012-sito-is-2021-so-et-es\Scripts\DFM_postprocess\data\input\DWSM-FM_100m_0000_map_regular_2367_1583_allvars_2timesteps.nc")

dfmspm = dfm.drop(['layer']).mesh2d_water_quality_output_9
cms = cms.where(((cms.time >= dfmspm.time.min()) & (cms.time <= dfmspm.time.max())), drop=True)

cms_newgrid = cms.interp(lat = dfmspm.lat, lon = dfmspm.lon)
