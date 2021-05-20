# =========================================================
#                     Process Hazmap
# =========================================================
# uses geopandas package to loop through each day and
# identify the level of smoke at the specified coordinates
# as well as animate the results

import pandas as pd
import geopandas as gpd
import numpy as np
import shapely
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

# read in a .shp
the_file = gpd.GeoDataFrame.from_file(
    "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/shapefile_smoke_polygons/smoke2018/smoke20180808.shp"
)


def gen_file(years, months, days):
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


def add_site(coords, smoke):
    """Generates a geodataframe describing a point at specified as tuple (lat, lon)
            joining the specified point to existing gdf "smoke"
    """
    df = pd.DataFrame({"lat": [coords[0]], "lon": [coords[1]]})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
    # add "Density" column to site for plotting purposes
    gdf["Density"] = "1"
    joined_gdf = gpd.GeoDataFrame(pd.concat([gdf, smoke], ignore_index=True))
    return joined_gdf


def join_site(site, smoke):
    """Joins the site shapefile to smoke and returns geodataframe
    adds "Density" column to site for plotting purposes
    """
    site["Density"] = "1"
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
        "  Waskesiu AERONET Site",
        verticalalignment="top",
        horizontalalignment="left",
        transform=ax.transAxes,
        fontsize=10,
    )
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    fig = plt.gcf()
    # fig.set_size_inches(10, 10)
    # fig.savefig("C:/Users/Owner/Wildfire_Smoke_Mckendry/data/plots/sample_plot.png")

    return fig, ax


def make_frame(file):
    """ iterate to the next day and redraw ax
    """
    curr_file = next(file)
    ax = curr_file.plot(column="Density")


"""
#class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, 
#    fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)
"""


#############################################################
#             this will become "__main__"
#############################################################

# initialize a file generator and get the first file
file_generator = gen_file(years, months, days)
the_file = next(file_generator)
# specify a site by lat/lon
waskesiu = (53.914, -106.070)

# add site to dile and generate the initial plot with which to animate
the_file = add_site(waskesiu, the_file)
fig, ax = make_plot(waskesiu, the_file)
fig.savefig("C:/Users/Owner/Wildfire_Smoke_Mckendry/data/plots/sample_plot.png")

# initialize a video writer
#Writer = animation.writers["ffmpeg"]
#writer = Writer(fps=15, metadata=dict(artist="Me"), bitrate=1800)

# make and save the animation
#anim = FuncAnimation(fig, make_frame, frames=100, interval=200)


# further code to plot AOD beside map (to be completed)
"""
wask = make_site(waskesiu)
joined = join_site(wask, curr_file)


light_smoke = the_file[the_file["Density"] == "5.000"]
med_smoke = the_file[the_file["Density"] == "16.000"]
heavy_smoke = the_file[the_file["Density"] == "27.000"]
smoke = (light_smoke, med_smoke, heavy_smoke)
"""
