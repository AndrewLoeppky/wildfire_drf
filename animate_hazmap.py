import pandas as pd
import geopandas as gpd
import geoplot
import numpy as np
import shapely
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation



def main():
    # read in a .shp
    the_file = gpd.GeoDataFrame.from_file(
        "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180808.shp"
    )

    fig = plt.figure()
    ax = geoplot.polyplot(the_file)
    ax.show()

if __name__ == "__main__":
    main()