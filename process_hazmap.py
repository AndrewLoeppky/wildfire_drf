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
import geopandas as gpd
from shapely.geometry import Point, Polygon
# %matplotlib inline

# +
## generate a geodataframe of field site(s)

# lat/lon of field site (just wask for now)
site_lat, site_lon =  53.91439, -106.06958

# display the site as a point
polygon_geom = Point((site_lon, site_lat))
crs = {'init': 'EPSG:4326'}
the_site = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom]);

# how big to display a plot
disp_size = 50 # degrees
sizeparam = disp_size / 2

# create the boundary box of specified size
lat_point_list = [site_lat + sizeparam, site_lat + sizeparam, site_lat - sizeparam, site_lat - sizeparam]
lon_point_list = [site_lon - sizeparam, site_lon + sizeparam, site_lon + sizeparam, site_lon - sizeparam]

polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
crs = {'init': 'EPSG:4326'}
plot_bbox = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom]);

# projection to newer syntax
plot_bbox = plot_bbox.to_crs(epsg=4326) 
# -


# get the smoke data
path_to_file = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180802.shp"

# +
the_file = gpd.read_file(path_to_file)
the_file.crs = {'init' :'epsg:4326'}
the_file = the_file.to_crs(epsg=4326)
the_file = gpd.clip(the_file, plot_bbox)

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
fig, ax = plt.subplots(figsize=(15,7))

ax.set_aspect("equal")
world.plot(ax=ax, color='grey')
light_smoke.plot(ax=ax, color="yellow", alpha=0.5)
med_smoke.plot(ax=ax, color="orange", alpha=0.5)
heavy_smoke.plot(ax=ax, color="red", alpha=0.5)
the_site.plot(ax=ax, marker='*')

plt.show()

# +
# useful methods
covered_by(other[, align]) # for figuring out the smokey plot part


# -
















