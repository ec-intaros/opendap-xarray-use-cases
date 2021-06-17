# Notebooks for analysing NetCDF data 

In this repository there are two notebooks for accessing, querying, analysing and visualising NetCDF data. The notebooks are explained in this document as separate sections. 

* 1) **Reference Notebook - Subset 2003 Analysis with Xarray**: 
* 2) **DAP Notebook - Extraction with Queries**: 





## 1) Reference Notebook - Subset 2003 Analysis with Xarray

This Notebook provides an overview, as well as practical examples, to access and analyse a subset of NetCDF data from available campaigns collected in the year 2003. This subset of data has been prepared and uploaded on the Hyrax server (https://opendap.terradue.com/hyrax/data/subset_2003/), where it can be accessed directly.

The main steps for executing the Notebook are described below. 

### Set-up
The first step is to define the url of the server to use. Two options are provided, one for HYRAX and one for THREDDS:
* hyrax: https://opendap.terradue.com/hyrax/data/subset_2003/
* thredds: https://opendap.terradue.com/thredds/dodsC/subset_2003/

Subsequently, the *year* and the *platform codes* are defined. This information is needed, and needs to be known a priori, as it allows comleting the url to access each specific NetCDF file. The naming convention of the NetCDF files is:
```58<platform_code>_CTD_<year>.nc.nc4```.
For example, for the platform 'GT' and year 2003, the name of the NetCDF file is: ```58GT_CTD_2003.nc.nc4.```

### Retrieval of DDS information
After the set-up, the data dimensions can be accessed through the Data Distribution Service (DDS), to understand the size of the datasets in an efficient way, without downloading all data into local memory. The dimensions under consideration for this NetCDF files are: 'TIME', 'LATITUDE', 'LONGITUDE', 'DEPTH', 'POSITION'.

### Visual Analysis: Load and Plot Positions only
The objective of this section is to visualise the geograhical positions of the data for each platform, and to perform some filtering operations based on locations and time queries. This is possible using only the necessary information retrieved from the DDS. The key dimensions that are used for the position analysis are: 'TIME', 'LATITUDE', 'LONGITUDE'. 

#### Create Position Dictionary and Dataframe 
The *position_dict* is a dictionary that is generated by iteratively reading the url of each platform, selecting only with 'TIME', 'LATITUDE', 'LONGITUDE' dimensions. In the dictionary are saved:
* the actual data, loaded into an xarray for data handling, analysis and visualisation
* the campaign's main attributes: *platform code & name*, *data type*, *title*, *instrument*, *longitude* & *latitude*, and *vertical min & max*)

A position dataframe is then generated per each platform, to match and combine the three 'TIME', 'LATITUDE', 'LONGITUDE' dimensions for each measurement. Subsequently, the platform-specific dataframes are combined in a *position_df* dataframe. An overview of the structure of the *position_df* dataframe is given below (showing the first and last 5 element):

Merged dataframe with all platforms. Total of 3209 measurement locations.
![image](./images/position_df_table.png)

#### Plot Positions 
The positions of all measurements of the given platforms are visualised in different colours on an interactive plot. By hoovering on the coloured dots, information such as index, x&y, and platform can be easily retrieved and visualised. 

![image](./images/interactive_position_plot.png)

#### Filter Positions
This section shows a few examples of data filtering by using the 'LATITUDE', 'LONGITUDE' and 'TIME' dimensions. The following filters are included:

* By bounding box (BBOX)
* By BBOX and Month of collection
* By BBOX and Time (eg hour) of collection

### Processing: Load and Plot all needed Data (Variables and their Attributes)
This section goes deeper into the data analysis by accessing all data (variables and their attributes). This is therefore more computationally-demanding, especially if multiple datasets of many measurements are analysed at once. 

#### Create Data Dictionary (*data_dict*) 
All data (variables and their attributes) for each platform are read iteratively, and saved into a dictionary *data_dict* which contains:
* the actual data, loaded into an xarray for data handling, analysis and visualisation
* the campaign's main attributes: *platform code & name*, *data type*, *title*, *instrument*, *longitude* & *latitude*, and *vertical min & max*)

An overview dataframe *overview_df* is then generated to show the detailed information about each campaign at sea: *platform code & name*, *data type*, *title*, *instrument*, *longitude* & *latitude*, and *vertical min & max*).

The variables that are available for each platform are extracted and printed out, to allow the user to select only those variables of interest for the detailed analysis. In this case, the four variables of interest in this dataset are: 
* **PRES**: Sea Water Pressure
* **TEMP**: Sea Water Temperature
* **PSAL**: Sea Water Practical Salinity
* **CNDC**: Sea Water Electrical Conductivity

#### Filter Data
This section allows filtering one or more variables for each platform, and DEPTH range, to the data that was previously filtered in the Filtered Position section.

The following are the four types of filters that are given as examples: 
* Filtered data by BBOX and One Variable
* Filtered data by BBOX (All Variables)
* Filtered data by BBOX and One Variable, within a DEPTH range
* Filtered data by BBOX (All Variables), within a DEPTH range

The output of all filters is a *filtered_xarr* xarray dataset, containing one or all the variables within the specified DEPTH range, of those positions that have been previously filtered (eg by "BBOX", by "BBOX and Month", or by "BBOX and Hour"). 

#### Reference Plots
The reference plots are generated for the available variables of the filtered xarrays. On the y-axis is shown the TIME of the measurement (in float format, which needs to be converted to datetime format), and on the x-axis is the DEPTH of the measurement. 

This notebook shows how to generate two types of plots:
* Plotting individual Variables per individual Platform
* Plotting individual Variables across aggregated Platforms

The first plot is more straightforward, as it automatically generates plot(s) of the variable(s) that has(have) been generated in the Filtered Data section. The example plot below represents the Sea Water Practical Salinity (PSAL) between 50 and 100 meters below sea level, for the platform GT.
![image](./images/GT_PSAL.png)

The second plot is more complex, as it needs an additional operation before executing. This consists on generating and then aggregating all data for a specific variable, across all platforms. To do so, the dimensions of the DEPTH of the variables of all platforms must be the equal, otherwise it is not possible to combine them into a new, aggregated, xarray. Two options are provided to accomplish this:
* Aggregate with minimum DEPTH, i.e. use minimum common DEPTH across all platforms' DEPTHs
* Aggregate with maximum DEPTH, i.e. use maximum DEPTH across all platforms' DEPTHs, and fill empty values with nans

The example plots below represent the four variables aggregated among the available platforms, between 0 and 100 meters below sea level.
![image](./images/aggregated_platforms.png)


## 2) DAP Notebook - Extraction with Queries