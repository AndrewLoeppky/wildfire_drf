# =========================================================
#                     Process Hazmap
# =========================================================
# uses geopandas package to loop through each day and
# identify the level of smoke at the specified coordinates

import geopandas as gpd
import numpy as np
from matplotlib import pyplot as plt


the_file = gpd.read_file(
    "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2012/smoke20120703.shx"
)

the_file.plot(column="Density")
plt.show()

"""
light_smoke = the_file[the_file["Density"] == "5.000"]
med_smoke = the_file[the_file["Density"] == "16.000"]
heavy_smoke = the_file[the_file["Density"] == "27.000"]
smoke = (light_smoke, med_smoke, heavy_smoke)


fig, ax = plt.subplots()

light_smoke.plot()

plt.plot()
ax = med_smoke.plot()
ax = heavy_smoke.plot()


plt.show()
"""
