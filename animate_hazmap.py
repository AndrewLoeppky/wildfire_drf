import pandas as pd
import geopandas as gpd
import numpy as np
import shapely
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation


def gen_file():
    """ loop through all dates in the dataset
    """
    years = range(2009, 2021)
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    days = ["01", "02", "03", "04", "05", "06", "07", "08", "09"] + list(range(10, 32))

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
                yield the_file


def add_site(coords, smoke_gdf):
    """Generates a geodataframe describing a point at specified as tuple (lat, lon)
            joining the specified point to existing gdf "smoke"
    """
    df = pd.DataFrame({"lat": [coords[0]], "lon": [coords[1]]})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
    # add "Density" column to site for plotting purposes
    gdf["Density"] = "1"
    joined_gdf = gpd.GeoDataFrame(pd.concat([gdf, smoke_gdf], ignore_index=True))
    return joined_gdf




def init(the_site):
    '''takes in a site tuple (lat, lon) and initializes the plot around the_site
    '''
    the_gen = gen_file()
    init_file = add_site(the_site, next(the_gen))


def main():
    waskesiu = (53.914, -106.070)
    init(waskesiu)
   

if __name__ == "__main__":
    main()

