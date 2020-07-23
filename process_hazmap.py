# =========================================================
#                     Process Hazmap
# =========================================================
# uses geopandas package to loop through each day and
# identify the level of smoke at the specified coordinates

import pandas as pd
import geopandas as gpd
import numpy as np
import shapely
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# read in a .shp
the_file = gpd.GeoDataFrame.from_file(
    "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180808.shp"
)

def get_file(years, months, days):
    """ loop through all dates in the dataset
    """
    for year in years:
        year = str(year)
        for month in months:
            month = str(month)
            for day in days:
                day = str(day)

                filename = (
                    "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke"
                    + year
                    + "/"
                    + "smoke"
                    + year
                    + month
                    + day
                    + ".shp"
                )
                the_file = gpd.GeoDataFrame.from_file(filename)
                print(filename)
                yield the_file


years = range(2009, 2021)
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09"] + list(range(10, 32))

def make_site(coords):
    """Generates a geodataframe describing a point at specified as tuple (lat, lon)
    """
    df = pd.DataFrame({"lat": [coords[0]], "lon": [coords[1]]})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
    return gdf

def join_site(site, smoke):
    """Joins the site shapefile to smoke and returns geodataframe
    adds "Density" column to site for plotting purposes
    """
    site['Density'] = '1'
    joined_gdf = gpd.GeoDataFrame(pd.concat([site, smoke], ignore_index=True))
    return joined_gdf

def make_plot(site, file):
    """ Plot smoke shapefiles from file within 5degrees of
        coordinates specified in site

        IN: file (geodataframe), site (lat/lon tuple)
        OUT: returns a matplotlib plot object
    """
    window_size = 10
    ax = file.plot(column="Density")
    ax.set_xlim([site[1] - (window_size // 2), site[1] + (window_size // 2)])
    ax.set_ylim([site[0] - (window_size // 2), site[0] + (window_size // 2)])
    ax.text(
        0.5,
        0.5,
        "   Waskesiu AERONET Site",
        verticalalignment="top",
        horizontalalignment="left",
        transform=ax.transAxes,
        fontsize=10,
    )
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    # fig.savefig("C:/Users/Owner/Wildfire_Smoke_Mckendry/data/plots/sample_plot.png")

    return fig,

def make_frame(site, file):
    
    # this iterates to the next day
    curr_file = next(file)
    # output the plot 
    frame = make_plot(site, file)
"""
#class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, 
#    fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)
"""
animation = FuncAnimation(fig, make_frame)

# the_file = get_file(years[8:], months[7:], days)
the_file = get_file(years, months, days)
curr_file = next(the_file)
waskesiu = (53.914, -106.070)
wask = make_site(waskesiu)

joined = join_site(wask, curr_file)
the_fig = make_plot(waskesiu, joined)
the_fig.show()




"""
light_smoke = the_file[the_file["Density"] == "5.000"]
med_smoke = the_file[the_file["Density"] == "16.000"]
heavy_smoke = the_file[the_file["Density"] == "27.000"]
smoke = (light_smoke, med_smoke, heavy_smoke)
"""
