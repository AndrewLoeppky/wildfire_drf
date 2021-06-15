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

path_to_file = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180802.shp"
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

print(the_file["Density"])

# +
###########################################################
################ plot smoke polygons ######################
###########################################################

# divide light, med, heavy smoke shapes
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
sitemarker = the_site.plot(ax=ax, marker="*", color="k")
ax.text(site_lon + 0.5, site_lat + 0.5, site_name)
ax.set_title(f"HMS Smoke Polygons for {date}")
ax.set_xlabel("Lon (deg)")
ax.set_ylabel("Lat (deg)")

plt.show()

# +
# which of the smokey shapes intersect the site?
#ign, locs = the_file.sindex.query_bulk(the_site["geometry"], predicate="intersects")
#the_file['intersects'] = np.isin(np.arange(0, len(the_file)), locs)

# +
# get the highest smoke level at the specified site
#try:
#    max_smoke = max(the_file[the_file['intersects'] == True]["Density"])
#    the_date = max(the_file[the_file['intersects'] == True])
#except:
#    max_smoke = 0

# +
######################################################################################
############## loop through all smoke data and extract level at site #################
######################################################################################

# create a new dataframe to store the timeseries
smoke_lvl = pd.DataFrame(columns=("date", "smokelvl"))


def convert_datetime(file, col):
    """
    takes in a HMS smoke polygon (or geodataframe full of them) and returns the date
    as a datetime object. col takes either "Start" or "End"
    """
    year = file[col].str[0:4]
    day = file[col].str[4:7]
    hour = file[col].str[8:10]
    mnt = file[col].str[10:12]
    return pd.to_datetime(year + day + hour + mnt, format="%Y%j%H%M")


def reset_path():
    """
    changes directory to where this notebook is stored (dont overthink it)
    """
    os.chdir("C:\\Users\\Owner\\Wildfire_Smoke_Mckendry\\code")


# def save_smoke_level_in_the_csv(path_to_file, df=smoke_lvl):
#    df = df.append({'date':1, "smokelvl":2}, ignore_index=True)


def parse_file(filepath, filename):
    # get file and date
    the_file = gpd.read_file(filepath)
    print(the_file["Density"])
    year, month, day = filename[5:9], filename[9:11], filename[11:13]

    """
    # convert to datetime format
    the_file["Start"] = pd.to_datetime(year + month + day + the_file["Start"])
    the_file["End"] = pd.to_datetime(year + month + day + the_file["End"])

    # loop through each hour of the day of the file
    hours = range(24)
    for hour in hours:
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
        print(curr_datetime,"---------------------------------------------------------------------------------")
        print(hourly_file)
    """

reset_path()
os.chdir("../data/shapefile_smoke_polygons")
base_path = os.getcwd()
dataset_years = os.listdir()
for year in dataset_years:
    the_path = base_path + "\\" + year
    print(f"Processing data in {the_path}")
    os.chdir(the_path)
    # do the big loop
    [parse_file((the_path + "\\" + file), file) for file in os.listdir() if file[-3:] == "shp"]
# -
smoke_lvl

smoke_lvl['date']= [1,2,3]
smoke_lvl['smokelvl'] = ['a','b',2]

smoke_lvl.append({'date':1, "smokelvl":2}, ignore_index=True)


# ## how to make this loop
#
# * [x] get the file for day x
#
# - [ ] change dates to my new format
#
# - [ ] for hour in day
#     
#     3) [ ] filter by hour, find max smoke level for that hour
#     
#     4) [ ] add to the dataframe year,day,hour:maxsmoke
#
# - [ ] save the whole deal as a csv

# +
def add_smokelevel(file):
    # open the file
    # code to open file
    
    # loop through each hour of the day of the file
    year, month, day = file[5:9], file[9:11], file[11:13]
    hours = range(24)
    for hour in hours:
        try:
            curr_datetime = pd.to_datetime(year+month+day+"0"+str(hour)+"0000")
        except OverflowError:
            curr_datetime = pd.to_datetime(year+month+day+str(hour)+"0000")
        #hourly_smoke = the_file[]
        print(curr_datetime)

add_smokelevel("smoke20180802.shp")

# +
path_to_file = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180802.shp"
file = "smoke20180802.shp"
# for file in files, where files are named smokeyyyymmdd.shp, and we have the variable path_to_file defined

the_file = gpd.read_file(path_to_file)
the_file['dtstart'] =  convert_datetime(the_file, "Start")
the_file['dtend'] = convert_datetime(the_file, "End")

curr_datetime = pd.Timestamp("20180802 220000")

hourly_file = the_file[the_file['dtstart'] < curr_datetime]# < the_file['dtend']] # doesnt work for some reason
hourly_file = hourly_file[curr_datetime < hourly_file['dtend']]
    
hourly_file

# +
the_file['dtstart'] =  convert_datetime(the_file, "Start")
the_file['dtend'] = convert_datetime(the_file, "End")

time1 = the_file['dtstart'][0]
time2 = the_file['dtend'][0]

time3 = pd.Timestamp('2018-08-02 16:00:01')

time1 < time3 < time2
