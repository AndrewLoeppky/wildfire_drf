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

import fiona
from shapely.geometry import Polygon, mapping 
from matplotlib import pyplot as plt
from descartes import PolygonPatch

# field site coordinates
site_lat, site_lon =  53.91439, 106.06958 # Waskisiu aerocan site

# +
# import a test shapefile. use august 1/18 when we know it was definitely smokey
my_shp = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180801.shp"
my_smoke = fiona.open(my_shp)

# how to extract smoke density
my_smoke[0]['properties']['Density']

# +
# loop through this whole process by date..
# -

# turn all separate shapes into Polygon objects
polylist = []
polyproperties = []
for shape in my_smoke:
    polygeom = Polygon(shape['geometry']['coordinates'][0])
    polylist.append(polygeom)
    polyproperties.append(shape['properties'])

# +
# create a small circle around field site coordinates
# -




