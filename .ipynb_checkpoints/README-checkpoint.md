# Subset 2003 Analysis with Xarray

This Notebook provides an overview, as well as practical examples, to access and analyse a subset of NetCDF data from available campaigns collected in the year 2003. This subset of data has been prepared and uploaded on the Hyrax server (https://opendap.terradue.com/hyrax/data/subset_2003/), where it can be accessed directly.

The main steps for executing the Notebook are described below. 

## Set-up
The first step is to define the url of the server to use. Two options are provided, one for HYRAX and one for THREDDS:
* hyrax: https://opendap.terradue.com/hyrax/data/subset_2003/
* thredds: https://opendap.terradue.com/thredds/dodsC/subset_2003/

Subsequently, the *year* and the *platform codes* are defined. This information is needed, and needs to be known a priori, as it allows comleting the url to access each specific NetCDF file. The naming convention of the NetCDF files is:
```58<platform_code>_CTD_<year>.nc.nc4```
For example, for the platform 'GT' and year 2003, the name of the NetCDF file is: 58GT_CTD_2003.nc.nc4.

## Retrieval of DDS information

## Visual Analysis: Load and Plot Positions only

### Create Position Dataframe 

### Plot Positions 

### Filter Positions
* By bounding box (BBOX)
* By BBOX and Month of collection
* By BBOX and Time (eg hour) of collection

## Processing: Load and Plot all needed Data (Variables and their Attributes)

### Create Data Dictionary (*data_dict*) 

### Filter Data
* Filtered data by BBOX and One Variable
* Filtered data by BBOX (All Variables)
* Filtered data by BBOX and One Variable, within a DEPTH range
* Filtered data by BBOX (All Variables), within a DEPTH range

### Reference Plots
* Plotting individual Variables per individual Platform
* Plotting individual Variables across aggregated Platforms




