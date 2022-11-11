# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:14:32 2022

@author: gwee
"""

import xarray as xr
import pandas as pd
import numpy as np
import os

indir = r'P:\11208031-007-ospar-validatie\data'
files = [os.path.join(indir, i) for i in os.listdir(indir) if 'CHL' in i]
files.sort()

def getValIndex(lat, lon, dslat, dslon):
    abslat = np.abs(dslat - lat)
    abslon = np.abs(dslon - lon)
    c = np.maximum(abslon, abslat)
    
    loc = np.where(c == np.min(c))
    
    return loc[0][0], loc[1][0]

#get mwtl station names
mn = pd.read_csv(r"P:\11208031-007-ospar-validatie\extractie\selstat.csv",
                   delimiter=';')

mwtl_loc = pd.read_csv(
    r"P:\11208031-007-ospar-validatie\extractie\mwtl_coords_noaeronet.txt",
    delimiter='\t')

mwtl = mwtl_loc[mwtl_loc.Name.isin(mn.satname)].reset_index(drop=True)

df = pd.DataFrame(columns = ['loc', 'year', 'month', 'day', 'chlfa'])

for f in files:
    
    ds = xr.open_dataset(f); ds.close()
    ds = ds.set_coords(['lat','lon'])

    basename = os.path.basename(f)
    date = f.split('_')[1].split('.')[0]
    
    yr = date[:4]
    mth = date[4:6]
    dy = date[6:]
    
    print(f'Extracting {yr}-{mth}-{dy}')
    lats, lons = mwtl.Lat.tolist(), mwtl.Lon.tolist()
    
    chl = []
    for (a, b) in zip(lats, lons):
        xi, yi = getValIndex(a, b, ds.lat, ds.lon)

        chl.append(ds.isel(x = xi, y = yi).CHL.values.tolist())
    
        
    ff = pd.DataFrame({'loc': mwtl.Name.tolist(),
                       'year': [int(yr)] * mwtl.shape[0],
                       'month': [int(mth)] * mwtl.shape[0],
                       'day': [int(dy)] * mwtl.shape[0],
                       'chlfa': chl})
    df = pd.concat([df, ff])
    
    del ds

df = df.reset_index(drop=True)

df.to_csv(r'P:\11208031-007-ospar-validatie\extractie\satelliet-rbins-2016-2019.csv',
          index = False)

# ### testing purpose
# ds = xr.open_dataset(r"P:\11208031-007-ospar-validatie\data\CHL_20160503.nc")

# ds = ds.set_coords(['lat','lon'])
# x, y = getValIndex(52.001, 2, ds.lat, ds.lon)

