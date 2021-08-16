# Notebooks for analysing NetCDF data 

In this repository there are two Notebooks for accessing, querying, analysing and visualising NetCDF data, accessible online from OPeNDAP servers, with the specific purpose to help application developers to refine and validate optimised OPeNDAP queries. 
For the provided code examples in the Notebooks, a subset of NetCDF data has been chosen from available CTD data acquisition campaigns collected in the year 2003 (cf. descriptions from the [INTAROS Catalogue](https://catalog-intaros.nersc.no/organization/institute-of-marine-research-imr)). This data subset has been prepared and uploaded on both the OPeNDAP Hyrax and the OPeNDAP TDS servers hosted on the iAOS Cloud Platform’s Data Agency (see section "Set-up" below), from where it can be accessed online by authorised developer users. This type of developer support operation can be adapted to any registered developer needs, and garantees a stable work environment for the duration of an application tests. 
Once a query strategy is validated by the developer, operational OPeNDAP servers can then be configured by the developer, and the optimised Notebook code can be integrated into a target application for efficient data filtering and retrieval across a network connection.

The two Notebooks are presented in this document as separate sections, and can be executed in parallel to refine and validate optimised OPeNDAP queries. 

The two Notebooks are:
1) **Test1 REF - OPeNDAP Xarray use cases**: a reference notebook for the download of full data files (data bulks as they are encoded server side), and storing their content in memory for processing: the bulk data structure can be further filtered to extract data chunks related to an analysis goal (build a reference view from the original data), using Python functions, and with plotting for data visualisation;
2) **Test1 DAP - OPeNDAP Xarray use cases**: a Data Access Protocol (DAP) Notebook for the validation of OPeNDAP query filters, in order to download optimized data chunks related to an analysis goal. These optimised downloads can be validated against a reference view created within the REF Notebook. These data chunks are also plotted for data visualisation.

Both the REF and DAP Notebooks follow the same approach: 
* Set-up of the Server URL, Year and Platform Codes
* Load and Plot of CTD Positions only (from DDS information, the OPeNDAP Data Description Structure)
* Load and Plot all needed CTD Data (from Variables and Attributes)

In each Notebook, two examples of data filtering queries are pre-defined, describing how to visualise different data ranges: 
* extraction of data between the first elements of DEPTH, eg **0-20**;
* extraction of data between the last elements of DEPTH, eg **50-last**.

Application developers are supported with these two examples to compare the two ways to querying data (Bulk and Optimized) in order to learn how to exploit efficiently (and without mistake) all the OPeNDAP server-side capabilities for optimized data filtering and retrieval across a network connection.

# 1) **Test1 REF - OPeNDAP Xarray use cases**

This Notebook provides an overview, as well as practical examples, for online access and analysis of netCDF data files holding CTD data acquisitions.

The main steps for executing the Notebook are described below. 

## Exploratory Data Analysis

### Set-up
The first step is to specify the data source available on the iAOS Cloud Platform’s Data Agency. Two options are provided, one for HYRAX and one for THREDDS DATA SERVER:
* hyrax: https://opendap.terradue.com/hyrax/data/subset_2003/
* thredds: https://opendap.terradue.com/thredds/dodsC/subset_2003/

Subsequently, the *year* and the *platform codes* are defined. This information is needed, and has to be known a priori, as it allows completing the url to access each specific NetCDF file. The naming convention of the NetCDF files is:
```58<platform_code>_CTD_<year>.nc.nc4```. For example, for the platform 'GT' and year 2003, the name of the NetCDF file is: ```58GT_CTD_2003.nc.nc4.```. 

### Retrieval of DDS information
After the set-up, the DDS information (OpenDAP’s Dataset Descriptor Structure) is retrieved. The data dimensions can then be accessed through the DDS, to understand the size of the datasets in an efficient way, without downloading all data into local memory. The dimensions under consideration for this NetCDF files are: 'TIME', 'LATITUDE', 'LONGITUDE', 'DEPTH', 'POSITION'.

### Visual Analysis: Load and Plot Positions only
The objective of this section is to visualise the geograhical positions of the data for each platform, and to perform some filtering operations based on locations and time queries. This is possible using only the necessary information retrieved from the DDS. The key dimensions that are used for the position analysis are: 'TIME', 'LATITUDE', 'LONGITUDE'. 

#### Create Position Dictionary and Dataframe 
The *position_dict* is a dictionary that is generated by iteratively reading the URL of each platform, selecting only with 'TIME', 'LATITUDE', 'LONGITUDE' dimensions. In the dictionary are saved:
* the actual data, loaded into an xarray for data handling, analysis and visualisation
* the campaign's main attributes: *platform code & name*, *data type*, *title*, *instrument*, *longitude* & *latitude*, and *vertical min & max*

A position dataframe is then generated per each platform, to match and combine the three 'TIME', 'LATITUDE', 'LONGITUDE' dimensions for each measurement. Subsequently, the platform-specific dataframes are combined in a *position_df* dataframe. An overview of the structure of the *position_df* dataframe is given below (showing the first and last 5 element):

Merged dataframe with all platforms. Total of 3209 measurement locations.
![image](./images/position_df_table.png)

#### Plot all Positions 
The positions of all measurements of the given platforms are visualised in different colours on an interactive plot. By hoovering on the coloured dots, information such as index, x&y, and platform can be easily retrieved and visualised, as shown as an example in the figure. 

![image](./images/interactive_position_plot.png)

### Filter Positions
The following filters are included to filter positions. These filters can be modified or extended by an application developer:

* By bounding box (BBOX)
* By BBOX and Month of collection
* By BBOX and Time (eg hour) of collection
* By customised time range

## Data Processing: Load and Plot all Data (Variables and their Attributes)
Going deeper into the data analysis, the next step is accessing all data (variables and their attributes). This is therefore more computationally-demanding, especially if multiple datasets of many measurements are analysed at once. 

### Fetch Data 

#### Create Data Dictionary (*data_dict*) 
All data (variables and their attributes) for each platform are read iteratively, and saved into a dictionary *data_dict* which contains:
* the actual data, loaded into an xarray for data handling, analysis and visualisation
* the campaign's main attributes: *platform code & name*, *data type*, *title*, *instrument*, *longitude* & *latitude*, and *vertical min & max*)

#### Dataframe with overview of Platforms' attributes  
An overview dataframe *overview_df* is then generated to show the detailed information about each campaign at sea: *platform code & name*, *data type*, *title*, *instrument*, *longitude* & *latitude*, and *vertical min & max*).

#### Define Variables
The four variables that are available in this dataset are: 
* **PRES**: Sea Water Pressure
* **TEMP**: Sea Water Temperature
* **PSAL**: Sea Water Practical Salinity
* **CNDC**: Sea Water Electrical Conductivity

#### Define Filtered Data
Then, the filtered dataframe (eg *position_df_bbox*, *position_df_bbox_mm*, *position_df_bbox_hh*) to use for the analysis is assigned to the **df_toPlot** variable.

### Range 0-20 Test
The parameters to be defined are:
* Platform Code
* Selected Variables
* DEPTH range

#### Data Filtering
The filtering is done for all variables of the defined platform and DEPTH range, to the previously-filtered data (eg by "BBOX", by "BBOX and Month", or by "BBOX and Hour"). The following are the two types of filters that are given as examples: 
* Filtered data by BBOX and One Variable
* Filtered data by BBOX (All Variables)

The output of both filters is a *filtered_xarr* xarray dataset, containing one or all the variables within the specified DEPTH range.

#### Reference Plots
The reference plots are generated for the available variables of the filtered xarrays. On the y-axis is shown the TIME of the measurement (in float format, which needs to be converted to datetime format), and on the x-axis is the DEPTH of the measurement.

This Notebook shows how to generate two types of plots:
* Plotting individual Variables per individual Platform
* Plotting individual Variables across aggregated Platforms

The first plot is straightforward, as it automatically generates plot(s) of the variable(s) that has(have) been generated in the Data Filtering section. The example plots below represent the Sea Water Temperature and Pressure between 0-20 meters for the selected locations of the platform GT.
![image](./images/ref_0-20_individual.png)

The second plot is more complex, as it needs an additional operation before executing. This consists in generating and then aggregating all data across all platforms, for a specific variable. To do so, the dimensions of the DEPTH of the variables of all platforms must be equal, otherwise it is not possible to combine them into a new, aggregated, xarray. Two options are provided to accomplish this:
* Aggregate with minimum DEPTH elements, i.e. use minimum common DEPTH across all platforms' DEPTHs
* Aggregate with maximum DEPTH elements, i.e. use maximum DEPTH across all platforms' DEPTHs, and fill empty values with nans

The example plots below represent the four variables aggregated among the available platforms, between 0 and 20 meters below sea level.
![image](./images/ref_0-20_aggregated.png)

### Range 50-last Test
This section follows the same structure as the 0-20 range section, but focuses on data extracted from the 50 meters onwards of DEPTH.

* Plots for Sea Water Temperature and Pressure respectively, between 50-2956 meters for the selected locations of the platform GT.
![image](./images/ref_50-last_individual.png)
* Plots for Sea Water Temperature and Pressure respectively, between 50-2956 meters for the aggregated platforms.
![image](./images/ref_50-last_aggregated.png)


# 2) **Test1 DAP - OPeNDAP Xarray use cases** 
This Notebook provides an overview, as well as practical examples, for online access and analysis of NetCDF data files holding CTD data acquisition. It loads server-side filtered data structures in memory, into optimized Python xarray structures, and performs the plotting of the retrieved variables. 

The first steps are to specify the CTD data source with the same target as done in the REF Notebook, for example the HYRAX server or the THREDDS DATA SERVER available on the iAOS Cloud Platform’s Data Agency, or else directly an operational OPeNDAP server, and perform the retrieval of the DDS information (following the same approach described in the REF notebook).

## Exploratory Data Analysis
This is the same as the *Exploratory Data Analysis* section in the REF Notebook. 

## Data Processing: Load and Plot selected Data (Variables within DEPTH range)
This section enables accessing data of **only selected variables** and **within a specified DEPTH range**, to avoid fetching unnecessary data and minimise data volume over the network (and therefore the duration of transfer) and the footprint of the data in memory.

The selected variables of interest need to be specified in the *var_list*. The four variables that are available in this dataset are: 
* **PRES**: Sea Water Pressure
* **TEMP**: Sea Water Temperature
* **PSAL**: Sea Water Practical Salinity
* **CNDC**: Sea Water Electrical Conductivity 

The DEPTH range must also be defined in this case, as data is fetched with the specific DEPTH range directly from URL. Due to some limitations of the DAP syntax, at least one range boundary needs to correspond to one of the two extremes. For example, in a data array of 100 elements starting from 0 to 99, the following scenarios are possible:
* select the first 20 elements, corresponding to the values range 0 - 19 --> ```[first:1:intermediate] (eg [0:1:19])``` work
* select the last 20 elements, corresponding to the values range 80 - 99 --> ```[intermediate:1:last] (eg [80:1:99])``` work
* select the intermediate 60-80 elements, corresponding to the values range 60 - 79 --> ```[intermediate_1:1:intermediate_2] (eg [60:1:79])``` does NOT work

### Range 0-20 Test

#### Create Data Dictionary (*data_dict*) 
The next step is to create the Data Dictionary (data_dict). Define Selected Variables and then the DEPTH range, noting that:
* ***metadata[pc]['depth_m_v1']***: either this is equal to the lower bound (ie index=0)
* ***metadata[pc]['depth_m_v2']***: or is equal to the upper bound (ie index=-1)

Once variables and depth range are defined, the data and their attributes are read iteratively for each platform, and saved into a dictionary *data_dict*,  following the same approach described in the REF notebook. 

#### Define Filtered Data
Subsequently, the filtered dataframe (eg *position_df_bbox*, *position_df_bbox_mm*, *position_df_bbox_hh*) to use for the analysis is defined to the **df_toPlot** variable.

#### Data Filtering
This is the same as the *Data Filtering* section in the REF Notebook. 

#### Reference Plots
The reference plots are generated in the same way as decribed in the REF Notebook. 
* Plots for Sea Water Temperature and Pressure respectively, between 0-20 meters for the selected locations of the platform GT.
![image](./images/dap_0-20_individual.png)
* Plots for Sea Water Temperature and Pressure respectively, between 0-20 meters, for the selected locations of the aggregated platforms.
![image](./images/dap_0-20_aggregated.png)


### Range 50-last Test
This section follows the same structure and analysis as the DAP 0-20 range section, but focuses on data extracted from the 50 meters onwards of DEPTH.

* Plot for Sea Water Temperature and Pressure respectively, between 50-2956 meters for the selected locations of the platform GT.
![image](./images/dap_50-last_individual.png)

* Plot for Sea Water Temperature and Pressure respectively, between 50-2956 meters for the aggregated platforms.
![image](./images/dap_50-last_aggregated.png)
