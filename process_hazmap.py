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
# **make sure coordinate systems match!**

from matplotlib import pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os
# %matplotlib inline

# +
###########################################################################
############## generate a geodataframe of field site(s) ###################
###########################################################################

# lat/lon of field site (just wask for now)
site_lat, site_lon = 53.91439, -106.06958  # waskesiu

# convert site to shapely point
polygon_geom = Point((site_lon, site_lat))
crs = {"init": "EPSG:4326"}
the_site = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])
the_site = the_site.to_crs(epsg=4326)

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

# change projection attribute to newer syntax
plot_bbox = plot_bbox.to_crs(epsg=4326)
# -


# get the smoke data
path_to_file = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180802.shp"

# +
the_file = gpd.read_file(path_to_file)

# complicated way to assign the data a projection
the_file.crs = {'init' :'epsg:4326'}
the_file = the_file.to_crs(epsg=4326)
the_file = gpd.clip(the_file, plot_bbox)
the_file.reset_index(inplace=True, drop=True)

# get the light smoke
light_smoke = the_file[the_file["Density"] == 5.0]

# get the med smoke
med_smoke = the_file[the_file["Density"] == 16.0]

# get the heavy smoke
heavy_smoke = the_file[the_file["Density"] == 27.0]
# -

# get a basemap
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = gpd.clip(world, plot_bbox)

# +
fig, ax = plt.subplots(figsize=(10,5))

#ax.set_aspect("equal")
world.plot(ax=ax, color='grey')
light_smoke.plot(ax=ax, color="yellow", alpha=0.5)
med_smoke.plot(ax=ax, color="orange", alpha=0.5)
heavy_smoke.plot(ax=ax, color="red", alpha=0.5)
the_site.plot(ax=ax, marker='*')

plt.show()
# -

# which of the smokey shapes intersect the site?
ign, locs = the_file.sindex.query_bulk(the_site["geometry"], predicate="intersects")
the_file['intersects'] = np.isin(np.arange(0, len(the_file)), locs)

# get the highest smoke level at the specified site
try:
    max_smoke = max(the_file[the_file['intersects'] == True]["Density"])
except:
    max_smoke = 0

max_smoke

######################################################################################
############## loop through all smoke data and extract level at site #################
######################################################################################
os.getcwd()

os.chdir("../data/shapefile_smoke_polygons")
base_path = os.getcwd()

dataset_years = os.listdir()

for year in dataset_years:
    the_path = base_path + "\\" + year
    print(f'Processing data in {the_path}')
    os.chdir(the_path)
    [print(the_path + '\\' + file) for file in os.listdir() if file[-3:] == "shp"]

