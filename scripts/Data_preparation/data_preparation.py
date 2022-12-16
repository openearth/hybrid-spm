# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 11:01:07 2022

@author: lorinc
"""
#import statements
import numpy as np
import os
import xarray as xr
import matplotlib 
import matplotlib.pyplot as plt
plt.close('all')
from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata
from dfm_tools.get_nc_helpers import get_ncvardimlist, get_timesfromnc, get_hisstationlist, get_ncvarproperties
import seaborn as sns
import glob
from sys import platform

#Path
if platform == 'linux':
    savepath=r'/p/11206887-012-sito-is-2021-so-et-es/Analysis/'
    fname = os.path.abspath(r'/p/11203669-004-kpp-morfwad-krw-slib/Waddenzee_KRWmodel_slib/WAQ27_new_newexecutable/DFM_OUTPUT_DWSM-FM_100m/DWSM-FM_100m_0000_map.nc')
    nc_path = os.path.abspath(r'/p/11206887-012-sito-is-2021-so-et-es/Scripts/DFM_postprocess/data/output/DWSM-FM_100m_0000_map_regular_2367_1583_TIM.nc')
    outfile = os.path.abspath(r'/p/11206887-012-sito-is-2021-so-et-es/Scripts/DFM_postprocess/data/output/DWSM-FM_100m_0000_map_regular_2367_1583_TIM_postproc.nc')
else:
    savepath=r'p:/11206887-012-sito-is-2021-so-et-es/Analysis/'
    fname = os.path.abspath(r'p:\11203669-004-kpp-morfwad-krw-slib\Waddenzee_KRWmodel_slib\WAQ27_new_newexecutable\DFM_OUTPUT_DWSM-FM_100m\DWSM-FM_100m_0000_map.nc')
    nc_path = os.path.abspath(r'p:\11206887-012-sito-is-2021-so-et-es\Scripts\DFM_postprocess\data\output\DWSM-FM_100m_0000_map_regular_2367_1583_TIM.nc')
    outfile = os.path.abspath(r'p:/11206887-012-sito-is-2021-so-et-es/Scripts/DFM_postprocess/data/output/DWSM-FM_100m_0000_map_regular_2367_1583_TIM_postproc.nc')

#%%INTERPOLATION CHECK=========================================================
#Visualise unstructured data using dfm_tools

# load map.nc data from all partitions
   
ugrid_all = get_netdata(file_nc=fname, multipart=True)

#get variables and dimensions
vars_pd = get_ncvarproperties(file_nc=fname)

# plot the model grid
fig, ax = plt.subplots()
pc = plot_netmapdata(ugrid_all.verts, values=None, ax=None, linewidth=0.5, color="crimson", facecolor="None")
ax.set_aspect('equal')

#resolution for interpolation
delta_x_n=(max(ugrid_all.mesh2d_node_x)-min(ugrid_all.mesh2d_node_x))*1111*np.cos(np.mean(ugrid_all.mesh2d_node_y)*np.pi/180)
delta_y_n=(max(ugrid_all.mesh2d_node_y)-min(ugrid_all.mesh2d_node_y))*1111

#plot raw model TIM (SPM) on map
model_time=get_timesfromnc(file_nc=fname, varname="time")
data_frommap_SPM = get_ncmodeldata(file_nc=fname, varname='mesh2d_water_quality_output_9', timestep=-1, layer=-1, multipart=True)

matplotlib.rcParams['figure.figsize'] = (20,10)
fig, ax = plt.subplots()
pc = plot_netmapdata(ugrid_all.verts, values=data_frommap_SPM[0,:], ax=None, linewidth=0.5, cmap="jet")
pc.set_clim([0,100])
fig.colorbar(pc, ax=ax)
#ax.set_title('%s (%s)'%(data_frommap_SPM.var_varname, data_frommap_SPM.var_ncattrs['units']))
ax.set_aspect('equal')

#Visualise structured data

#Data source: Processed DFM output (100mx100m)
ds = xr.open_dataset(nc_path)
ds=ds.sortby('time')
#Postprocess time
matplotlib.rcParams['figure.figsize'] = (20,10)
ds.mesh2d_water_quality_output_9.isel(layer=-1, time=-1).plot(cmap="jet", robust=True)

# #Combined plot
# for time in np.arange(0,365,14):
#     data_frommap_SPM = get_ncmodeldata(file_nc=fname, varname='mesh2d_water_quality_output_9', timestep=time, layer=-1, multipart=True)
    
#     matplotlib.rcParams['figure.figsize'] = (20,10)
#     fig, ax = plt.subplots(2)
#     pc = plot_netmapdata(ugrid_all.verts, values=data_frommap_SPM[0,:], ax=ax[0], linewidth=0.5, cmap="jet")
#     pc.set_clim([0,100])
#     fig.colorbar(pc, ax=ax[0])
#     ax[0].set_xlim(min(ugrid_all.mesh2d_node_x),max(ugrid_all.mesh2d_node_x))
#     ax[0].set_ylim(min(ugrid_all.mesh2d_node_y),max(ugrid_all.mesh2d_node_y))
#     ax[0].set_title('Raw model output')
#     #ax.set_title('%s (%s)'%(data_frommap_SPM.var_varname, data_frommap_SPM.var_ncattrs['units']))
#     ds.mesh2d_water_quality_output_9.isel(layer=-1, time=time).plot(cmap="jet", robust=True, ax=ax[1], vmin=0, vmax=100)
#     fig.savefig(savepath + 'Plots/DFM/Interp_check/DFM_raw_vs_DFM_interp' + '_' + str(ds.time.values[time])[:10] + '.png', format='png', bbox_inches='tight', dpi=300)
#     print(str(ds.time.values[time])[:10])
    
#%%Statistics==========================================================
#Variables
SPM=ds.mesh2d_water_quality_output_9

#histpolt
xr.plot.hist(SPM)
fig.savefig(savepath + 'Plots/DFM/Interp_check/DFM_interp_histplot_before' + '.png', format='png', bbox_inches='tight', dpi=300)

#min-max before
print('min: '+ str(SPM.min()))
print('max: '+ str(SPM.max()))

#Clean outliers
SPM_pos = SPM.where(SPM > 0)
ds['mesh2d_water_quality_output_9'] = SPM_pos

SPM_check=ds.mesh2d_water_quality_output_9.isel(layer=-1, time = -1)

#histpolt after
xr.plot.hist(SPM_check)
fig.savefig(savepath + 'Plots/DFM/Interp_check/DFM_interp_histplot_after' + '.png', format='png', bbox_inches='tight', dpi=300)

#min-max after
print('min: '+ str(SPM_check.min()))
print('max: '+ str(SPM_check.max()))

#Savefile
ds.to_netcdf(outfile)
print('Yearly datasets saved')