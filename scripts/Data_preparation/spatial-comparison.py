# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 11:27:34 2022

@author: gwee

remarks: spatial comparison between DFM and cmems
"""

import xarray as xr
import matplotlib.pyplot as plt
import os
plt.rcParams.update({'figure.max_open_warning': 0})

from sys import platform
if platform == 'linux':
    cms = xr.open_dataset(
        r"/p/11206887-012-sito-is-2021-so-et-es/Data/CMEMS_Satellite_100mx100m/merged_2015-2020/2015_2020_P1D_HROC_L3-transp_NWS_31_32ULE_100m-v01.nc")
    dfm = xr.open_dataset(
        r"/p/11206887-012-sito-is-2021-so-et-es/Data/DFM_DWSM-FM_100m/Postprocessing_maps/DWSM-FM_100m_0000_map_regular_500_400_allvars.nc")
    opath = r"/p/11206887-012-sito-is-2021-so-et-es/Analysis/Plots/Compare_CMEMS100m_Model100m/spatial-comparison"
else:
    cms = xr.open_dataset(
        r"p:\11206887-012-sito-is-2021-so-et-es\Data\CMEMS_Satellite_100mx100m\merged_2015-2020\2015_2020_P1D_HROC_L3-transp_NWS_31_32ULE_100m-v01.nc")
    dfm = xr.open_dataset(
        r"P:\11206887-012-sito-is-2021-so-et-es\Data\DFM_DWSM-FM_100m\Postprocessing_maps\DWSM-FM_100m_0000_map_regular_500_400_allvars.nc")
    opath = r"P:\11206887-012-sito-is-2021-so-et-es\Analysis\Plots\Compare_CMEMS100m_Model100m\spatial-comparison"

var = [i for i in list(dfm.variables) if 'mesh' in i]
units = [dfm[i].units for i in var]
naming = ['salinity', 'temperature', 'SPM',
          'depth', 'velocity', 'pressure', 'significant-wave-height']

#cut dfm to boundaries of cmems
dfm_cut = dfm.where(((dfm.lat <= cms.lat.max()) & (dfm.lat >= cms.lat.min()) \
                         & (dfm.lon <= cms.lon.max()) & (dfm.lon >= cms.lon.min())),drop=True)
#cut cmems to temporal boundaries of dfm
cms_cut = cms.sel(time=cms.time.dt.year == 2017)


# # monthly
for m in range(1,13):
    cms_m = cms_cut.sel(time=cms_cut.time.dt.month == m).mean(dim='time')
    dfm_m = dfm_cut.sel(time=dfm_cut.time.dt.month == m).mean(dim='time')
    
    for i, n in enumerate(var):
        
        #plot
        fig, axes = plt.subplots(nrows=2)
        if n == 'mesh2d_water_quality_output_9':
            dfm_m[n].plot(ax=axes[0], vmin=0, vmax=100, cbar_kwargs={"label": f'{naming[i]} [{units[i]}]'})
        else:
            dfm_m[n].plot(ax=axes[0], cbar_kwargs={"label": f'{naming[i]} [{units[i]}]'})
        
        cms_m.SPM.plot(ax=axes[1], vmax=100)
        
        plt.savefig(os.path.join(opath, 'monthly', f'cmems-dfm-spatial-comparison-month{m}-{naming[i]}.png'))
        print(f'figure generated for month {m} and {n}')
        plt.clf()
        

#year
y = 2017

cms_y = cms_cut.mean(dim='time')
dfm_y = dfm_cut.sel(time=dfm_cut.time.dt.year == y).mean(dim='time')

for i, n in enumerate(var):
    
    #plot
    fig, axes = plt.subplots(nrows=2)
    if n == 'mesh2d_water_quality_output_9':
        dfm_y[n].plot(ax=axes[0], vmin=0, vmax=100, cbar_kwargs={"label": f'{naming[i]} [{units[i]}]'})
    else:
        dfm_y[n].plot(ax=axes[0], cbar_kwargs={"label": f'{naming[i]} [{units[i]}]'})
    
    cms_y.SPM.plot(ax=axes[1], vmax=100)
    
    fig.subplots_adjust(hspace=0.4)
    plt.savefig(os.path.join(opath, 'yearly', f'cmems-dfm-spatial-comparison-year{y}-{naming[i]}.png'))
    print(f'figure generated for {y} {n}')
    plt.clf()


for e in cms_cut.time.values:
    cms_e = cms_cut.sel(time=cms_cut.time == e)
    dfm_e = dfm_cut.sel(time=dfm_cut.time == e)
    for i, n in enumerate(var):
        
        
        #plot
        fig, axes = plt.subplots(nrows=2)
        if n == 'mesh2d_water_quality_output_9':
            dfm_e[n].plot(ax=axes[0], vmin=0, vmax=100, cbar_kwargs={"label": f'{naming[i]} [{units[i]}]'})
        else:
            dfm_e[n].plot(ax=axes[0], cbar_kwargs={"label": f'{naming[i]} [{units[i]}]'})
        cms_e.SPM.plot(ax=axes[1], vmax=100)
            
        fig.subplots_adjust(hspace=0.4)
        plt.savefig(os.path.join(opath, 'matchup', f'''cmems-dfm-spatial-comparison-{e.astype(str)[:10].replace('-','')}-{naming[i]}.png'''))
        print(f'figure printed for {e.astype(str)[:10]} {n}')
        plt.clf()
        