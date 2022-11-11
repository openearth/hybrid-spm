# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 10:32:28 2022

@author: lorinc
"""
#import statements
import os
import xarray as xr
import glob
from sys import platform

#%%Combine monthly DFM files
#Merge monthly files
if platform == 'linux':
    subdir = os.path.abspath(r'/p/11206887-012-sito-is-2021-so-et-es/Scripts/DFM_postprocess/data/output/')
    outfile = os.path.abspath(r'/p/11206887-012-sito-is-2021-so-et-es/Scripts/DFM_postprocess/data/output/DWSM-FM_100m_0000_map_regular_2367_1583_TIM.nc')
else:
    subdir = os.path.abspath(r'p:\11206887-012-sito-is-2021-so-et-es\Scripts\DFM_postprocess\data\output')
    outfile = os.path.abspath(r'p:\11206887-012-sito-is-2021-so-et-es\Scripts\DFM_postprocess\data\output\DWSM-FM_100m_0000_map_regular_2367_1583_TIM.nc')

fn_monthly=glob.glob(os.path.join(subdir, '*.nc'))
DFM_combined = xr.open_mfdataset(fn_monthly, combine = 'nested', concat_dim=["time"])

#Savefile
DFM_combined.to_netcdf(outfile)
print('Yearly datasets saved')