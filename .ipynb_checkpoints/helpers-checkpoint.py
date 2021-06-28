# Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
import xarray as xr
import requests
import re

# Function to retrieve DDS info (sizes of 'TIME', 'LATITUDE', 'LONGITUDE', 'DEPTH', 'POSITION')
def retrieveDDSinfo(dds):
    
    # Function to extract the dimension of a specific keyword
    def findDim(txt, key):
        sel = [elem for elem in txt if key in elem]
        assert len(sel)==1

        dim = int(sel[0].split(' = ')[-1].strip(']'))-1
        return dim    
    
    r = requests.get(dds)
    
    unique_list = set(re.findall(r'\[.*?\]',r.text))
#     print('Unique elements:', unique_list)
    
    keys = ['TIME', 'LATITUDE', 'LONGITUDE', 'DEPTH', 'POSITION']

    dim_dict = {}

    for k in keys:
        dim_dict[k] = findDim(txt=unique_list, key=k)

    return dim_dict


# Function to build a string for query on URL
def getQueryString(mydict, keylist):
#     print('Retriving Query string for keywords:', keylist)
    
    que_str = ','.join([f'{key}[0:1:{mydict[key]}]' for key in mydict.keys() if key in keylist])
#     print('Query string:', que_str)
    return que_str


def fetch_data(url):
    remote_data = xr.open_dataset(
        url,
        decode_times=False,
    )   
    
    lon_min = float(remote_data.attrs['geospatial_lon_min'])
    lon_max = float(remote_data.attrs['geospatial_lon_max'])
    lat_min = float(remote_data.attrs['geospatial_lat_min'])
    lat_max = float(remote_data.attrs['geospatial_lat_max'])

    plat_code = remote_data.attrs['platform_code']
    plat_name = remote_data.attrs['platform_name']
    year = url.split('subset_')[1][:4]
    dtype = remote_data.attrs['data_type']
    title = remote_data.attrs['title']
    inst = remote_data.attrs['instrument']
    v_min = remote_data.attrs['geospatial_vertical_min']
    v_max = remote_data.attrs['geospatial_vertical_max']

    data_attr = np.array([plat_code, plat_name, year, dtype, title, inst, 
                         v_min, v_max, lon_min, lon_max, lat_min, lat_max])   
    
    return remote_data, data_attr


# Function to filter XARRAY based on platform, Var and DEPTH
def filter_xarr(df_toPlot, data_dict, platform, var, depth_range):
    
    # find indices for each platform for the selected data
    index = df_toPlot[df_toPlot['Platform']==platform].index.tolist()
    
    # Filer data using the indexes of the filtered elements
    xarr_sel = data_dict[platform]['data'][var].isel(TIME=index,
                                                     DEPTH=slice(depth_range[0], depth_range[1]+1))
    return xarr_sel


# Function to adjust data array with Vertical Min
def adjust_with_vmin(xarr_var, value):
    
    xarr_var = np.insert(xarr_var, obj=0, values=value, axis=1)
    #print('Adjusted shape:', xarr_var.shape)
    #display(xarr_var)

    # Remove last element (ie same dimension as original)
    xarr_var_trimmed = xarr_var[:,:-1]
    #print('Trimmed shape:', xarr_var_trimmed.shape)
    #display(xarr_var_trimmed)
    
    # return the trimmed array, to re-assign it to the original element
    return xarr_var_trimmed

# Function to check whether data should be aligned if vmin = 1, and align if so if has not been done already
def check_alignment(data_dict, pc, var, align_and_nan, vmin_dict):
    
    xarr = data_dict[pc]['data']
    xarr_var = xarr[var].data
    
    vmin = float(xarr.attrs['geospatial_vertical_min'])

    if vmin == 0:
        print(f'Platform: {pc} - Vertical min = {vmin}')
        
    elif vmin==1 and vmin_dict[pc][var]==False and align_and_nan: 
        # shift to the right and add nan in first position 
        print(f'Platform: {pc} - Vertical min = {vmin} --> aligning and add nan')
        data_dict[pc]['data'][var].data = adjust_with_vmin(xarr_var, value=np.nan)
        vmin_dict[pc][var] = True # to avoid doing hte vmin adjustment for this pc/var more than once
        print('this is a test')
        
    elif vmin==1 and vmin_dict[pc][var]==False and not align_and_nan: 
        # No need to shift, this occurred already in the data extraction
        print(f'Platform: {pc} - Vertical min = {vmin} --> data has been aligned already')
        vmin_dict[pc][var] = True # to avoid doing hte vmin adjustment for this pc/var more than once
        
        
# Function to plot a specific variable
def plotFilteredVar(data_xarr_var, title):
    plt.figure()
    # display(data_xarr)
    data_xarr_var.plot()
    plt.title(title)
    
    
# Function to plot a specific variable across the merged platforms
def plotVar_MergedPlatforms(merged_arr_var, var, title):
    plt.figure()
    merged_arr_var[var].plot() 
    plt.title(title)
    
    
# Function to create a new xarray. DataArray
def newXDA(oldarr, newarr_data, var):
    da = xr.DataArray(
        data=newarr_data, # this is the actual numpy array with the new desired shape
        dims=oldarr.dims, # copy dimensions names from the old array (eg TIME, DEPTH)
        coords=oldarr.coords, # copy coords
        attrs=oldarr.attrs, # copy attrs
        name=var # define var name
    )
    
    return da


# Function to define queries
def getQuery(pc, start, stop):
    dims = f'[{start}:1:{stop}]' # in the format [start,step,stop]
    return dims

# # function call for TIME
# dim_name = 'TIME'
# time_dims = getQuery(pc='AA', start=0, stop=pc_dim_dict[pc][dim_name])
# print(dim_name, time_dims)

# # function call for DEPTH
# dim_name = 'DEPTH'
# depth_dims = getQuery(pc='AA', start=0, stop=pc_dim_dict[pc][dim_name])
# print(dim_name, depth_dims)

# # join TIME and DEPTH for ONE Variables
# var = 'TEMP'
# queries_ONEvar = f'{var}{time_dims}{depth_dims}'
# print(queries_ONEvar)

# # join TIME and DEPTH for ALL Variables
# var_str_ALL = []

# for var in all_vars:
#     var_str = f'{var}{time_dims}{depth_dims}'
#     var_str_ALL = np.append(var_str_ALL, var_str)
# queries_ALLvars = ','.join(var_str_ALL)
# print(queries_ALLvars)

# Combine positional queries and variable queries:
# - Positional: queries_pos_str
# - Variable: queries_ONEvar OR queries_ALLvars

# # Combine Positions and Variables Queries
# queries_all = ','.join([queries_pos_str,queries_ONEvar])
# queries_all


# Function to save Attributes to a database
def getAttributes(my_df, my_dict):
    
    for key in my_dict.keys():

        my_df.loc[key,'Platform_code'] = [my_dict[key]['data_attr'][0].astype(str)]
        my_df.loc[key,'Platform_name'] = [my_dict[key]['data_attr'][1].astype(str)]
        my_df.loc[key,'Year'] = [my_dict[key]['data_attr'][2].astype(int)]
        my_df.loc[key,'Data_type'] = [my_dict[key]['data_attr'][3].astype(str)]
        my_df.loc[key,'Title'] = [my_dict[key]['data_attr'][4].astype(str)]
        my_df.loc[key,'Instrument'] = [my_dict[key]['data_attr'][5].astype(str)]
        my_df.loc[key,'Vertical_min'] = [my_dict[key]['data_attr'][6].astype(float)]
        my_df.loc[key,'Vertical_max'] = [my_dict[key]['data_attr'][7].astype(float)]
        my_df.loc[key,'Lon_min'] = [my_dict[key]['data_attr'][8].astype(float)]
        my_df.loc[key,'Lon_max'] = [my_dict[key]['data_attr'][9].astype(float)]
        my_df.loc[key,'Lat_min'] = [my_dict[key]['data_attr'][10].astype(float)]
        my_df.loc[key,'Lat_max'] = [my_dict[key]['data_attr'][11].astype(float)]

    return my_df    
    