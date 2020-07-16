# =========================================================
#                     Process Hazmap
# =========================================================
# uses geopandas package to loop through each day and
# identify the level of smoke at the specified coordinates

import geopandas as gpd
import numpy as np
from matplotlib import pyplot as plt


the_file = gpd.read_file(
    "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2012/smoke20120703.shp"
)

the_plot = plt.plot(the_file)
plt.show(the_plot)
