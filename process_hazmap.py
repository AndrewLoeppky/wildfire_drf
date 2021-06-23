# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Process Hazmap
#
# - retrieve a shp file from harddrive (later add functionality to scrape a single file from online archive)
#
# - initialize a site by lat/lon
#
# - determine smoke level at that site
#
# - output a timeseries as a dataframe/saved as .csv of pd.to_datetime(dataset[["year", "month", "day", "hour", "minute", second"]]) and smoke level at that site
#
# - save a plot of the site and smoke level as a png
#
#
# **make sure coordinate systems match! (they do, epsg4326)**

# +
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os

# %matplotlib inline
# display all of a df
pd.set_option("display.max_rows", None, "display.max_columns", None)

# +
###########################################################################
############## generate a geodataframe of field site(s) ###################
###########################################################################

# lat/lon of field site (just wask for now)
site_lat, site_lon = 53.91439, -106.06958
site_name = "Waskesiu"

# convert site to shapely point
polygon_geom = Point((site_lon, site_lat))
crs = {"init": "EPSG:4326"}
the_site = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])
the_site = the_site.to_crs(epsg=4326)


# +
####################################################################
########## extract data from HMS smoke shapefiles ##################
####################################################################

path_to_file = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180803.shp"
#path_to_file = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2015/smoke20150727.shp"


the_file = gpd.read_file(path_to_file)

# set size limits for plot
disp_width = 50  # degrees
disp_height = 30  # degrees
disp_width /= 2
disp_height /= 2

# create the boundary box of specified size
lat_point_list = [
    site_lat + disp_height,
    site_lat + disp_height,
    site_lat - disp_height,
    site_lat - disp_height,
]
lon_point_list = [
    site_lon - disp_width,
    site_lon + disp_width,
    site_lon + disp_width,
    site_lon - disp_width,
]

polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
crs = {"init": "EPSG:4326"}
plot_bbox = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])
plot_bbox = plot_bbox.to_crs(epsg=4326)

# complicated way to assign the data a projection
the_file.crs = {'init' :'epsg:4326'}
the_file = the_file.to_crs(epsg=4326)
the_file = gpd.clip(the_file, plot_bbox)
the_file.reset_index(inplace=True, drop=True)

# +
###########################################################
################ plot smoke polygons ######################
###########################################################

# divide light, med, heavy smoke shapes
try:
    light_smoke = the_file[the_file["Density"] == 5.0]
    med_smoke = the_file[the_file["Density"] == 16.0]
    heavy_smoke = the_file[the_file["Density"] == 27.0]
    
except KeyError:
    the_file["Density"] = 1.0 # assign a code for un-ordered smoke polygons
    ambg_smoke = the_file[the_file["Density"] == 1.0]
    light_smoke = the_file[the_file["Density"] == 5.0]
    med_smoke = the_file[the_file["Density"] == 16.0]
    heavy_smoke = the_file[the_file["Density"] == 27.0]

# get a basemap
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = gpd.clip(world, plot_bbox)

# do the plot
fig, ax = plt.subplots(figsize=(10,10))
world.plot(ax=ax, color="grey")
light_smoke.plot(ax=ax, color="yellow", alpha=0.5)
med_smoke.plot(ax=ax, color="orange", alpha=0.5)
heavy_smoke.plot(ax=ax, color="red", alpha=0.5)
try:
    ambg_smoke.plot(ax=ax, color="lightblue", alpha=0.5)
except NameError:
    pass
sitemarker = the_site.plot(ax=ax, marker="*", color="k")
ax.text(site_lon + 0.5, site_lat + 0.5, site_name)
ax.set_title(f"HMS Smoke Polygons")
ax.set_xlabel("Lon (deg)")
ax.set_ylabel("Lat (deg)")
ax.text(site_lon-25, site_lat+15.5, "the date")

plt.show()

# +
######################################################################################
############## loop through all smoke data and extract level at site #################
######################################################################################


def reset_path():
    """
    changes directory to where this notebook is stored (dont overthink it)
    """
    os.chdir("C:\\Users\\Owner\\Wildfire_Smoke_Mckendry\\code")


def get_max(arg):
    """
    returns the maximum of a sequence, or 0 if the sequence is empty or None
    """
    try:
        the_max = max(arg)
    except ValueError:  # in case it is empty
        the_max = 0
    except TypeError:
        the_max = 0
    if the_max == None:
        return 0
    else:
        return the_max


def parse_file(filepath, filename):
    # get file and date
    the_file = gpd.read_file(filepath)
    year, month, day = filename[5:9], filename[9:11], filename[11:13]
    
    # filter for polygons that intersect site
    ign, locs = the_file.sindex.query_bulk(the_site["geometry"], predicate="intersects")
    the_file["intersects"] = np.isin(np.arange(0, len(the_file)), locs)
    the_file = the_file[the_file["intersects"] == True]

    # add a density column if necessary (pre 2008 files lack them)
    if "Density" not in the_file.columns.values:
        the_file["Density"] = 1.000  # code for ambiguous smoke level
        
    # convert datetime format -- ##this needs to handle more alternative dt formats##
    try:       
        the_file["Start"] = pd.to_datetime(year + month + day + the_file["Start"])
        the_file["End"] = pd.to_datetime(year + month + day + the_file["End"])
    except:
        # handle alternate (bad) time formatting
        the_file["Start"] = pd.to_datetime(year + month + day + the_file["Start"][:-4])
        the_file["End"] = pd.to_datetime(year + month + day + the_file["End"][:-4])

        
    # loop through each hour of the day of the file
    def do_hourloop(hour, file=the_file):
        """
        takes in an int "hour" from 0 to 23 and geodataframe "file",
        generates a datetime object with the year month day hour,
        calculates the smoke level at the hour specified 
        """
        # get the "current" datetime
        try:
            curr_datetime = pd.to_datetime(
                year + month + day + "0" + str(hour) + "0000"
            )
        except OverflowError:
            curr_datetime = pd.to_datetime(year + month + day + str(hour) + "0000")

        # filter the df by hour
        hourly_file = the_file[the_file["Start"] < curr_datetime]
        hourly_file = hourly_file[curr_datetime < hourly_file["End"]]

        # save data to the pandas df
        dt, smk = curr_datetime, get_max(hourly_file["Density"].values)
        print(dt, smk)
        #df = pd.DataFrame({dt, smk)
        return dt, smk

    # execute the loop in a LC
    hours = range(24)
    for hour in hours:
        do_hourloop(hour) 
# +
## the main event ##
reset_path()
os.chdir("../data/shapefile_smoke_polygons")
base_path = os.getcwd()
dataset_years = os.listdir()
dataset_years = os.listdir()[-3:-2] ########################## testing only ################3

# some days contain errors
glitch_days = {"smoke20140326.shp", # CPLE_OpenFailedError 
               "smoke20150120.shp", # CPLE
               "smoke20150125.shp", # KeyError
               "smoke20170715.shp", # ParserError
               "smoke20170720.shp", 
               "smoke20170817.shp", 
               "smoke20170824.shp",
               "smoke20170831.shp",
               "smoke20170909.shp",
               "smoke20180303.shp", # KeyError
               "smoke20180512.shp", # ParserError
               "smoke20180520.shp", # ParserError
               "smoke20180724.shp",
               "smoke20180725.shp",
               "smoke20180727.shp",
               "smoke20180801.shp",
               "smoke20180805.shp",
               "smoke20180808.shp",
               "smoke20180809.shp",
               "smoke20180810.shp",
               "smoke20180811.shp",
               "smoke20180812.shp",
               "smoke20180815.shp",
               "smoke20180816.shp",
               "smoke20180817.shp",
               "smoke20180821.shp",
               "smoke20180822.shp",
               "smoke20180823.shp",
               "smoke20190529.shp",  # ParserError (a new one..)
               "smoke20190530.shp",
               "smoke20190601.shp"
              }

# create a new dataframe to store the timeseries
smoke_lvl = pd.DataFrame(columns=("datetime", "smoke_lvl"))

for year in dataset_years:
    the_path = base_path + "\\" + year
    print(f"Processing data in {the_path}")
    os.chdir(the_path)
    # do the big loop
    [parse_file((the_path + "\\" + file), file) for file in os.listdir()
                                                if file[-3:] == "shp" 
                                                if file not in glitch_days]


# +
## Testing zone
smoke_lvl = pd.DataFrame(columns=("datetime", "smoke_lvl"))

path_to_file = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2019/smoke20190602.shp"
file = path_to_file[-17:]

parse_file(path_to_file, file)
# -

smoke_lvl['date']= [1,2,3]
smoke_lvl['smokelvl'] = ['a','b',2]

smoke_lvl = smoke_lvl.append({'date':1, "smokelvl":2}, ignore_index=True)
smoke_lvl

# ## how to make this loop
#
# * [x] get the file for day x
#
# - [x] filter for polygons that intersect site
#
# - [x] change dates to my new format
#
# - [x] for hour in day
#     
#     3) [x] filter by hour, find max smoke level for that hour
#     
#     4) [ ] add to the dataframe year,day,hour:maxsmoke
#
# - [ ] save the whole deal as a csv

reset_path()
os.chdir("../data/shapefile_smoke_polygons")
base_path = os.getcwd()
os.listdir()[-3:]

"201706252017177 0130"[-4:]


