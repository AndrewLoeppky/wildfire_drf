# =========================================================
#                     Process Hazmap
# =========================================================
# uses geopandas package to loop through each day and
# identify the level of smoke at the specified coordinates

import geopandas as gpd
import numpy as np
import shapely
from matplotlib import pyplot as plt

# read in a .shp
the_file = gpd.GeoDataFrame.from_file(
    "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180808.shp"
)

# choose some coords to compare it to (make this a function later)
waskesiu = (53.914, -106.070)

the_site = waskesiu
window_size = 10
ax = the_file.plot(column="Density")
ax.set_xlim([the_site[1] - (window_size // 2), the_site[1] + (window_size // 2)])
ax.set_ylim([the_site[0] - (window_size // 2), the_site[0] + (window_size // 2)])
ax.text(
    0.5,
    0.5,
    "x\n        Waskesiu",
    verticalalignment="top",
    horizontalalignment="left",
    transform=ax.transAxes,
    fontsize=15,
)
fig = plt.gcf()
fig.set_size_inches(10, 10)
fig.savefig("C:/Users/Owner/Wildfire_Smoke_Mckendry/data/plots/sample_plot.png")

"""
the_file.plot(column="Density")
plt.show()


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
