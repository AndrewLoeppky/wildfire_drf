# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Data Scraping From NOAA / NESDIS Wildfire Smoke Mapping
# Code Author: Andrew Loeppky <br>
# Supervisor: Dr. Ian Mckendry <br>
# Project:  Effects of Wildfire Smoke on Forest Productivity in Central Canada <br>
# Date: June 2020
#
# Data Source: ```https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/```
#

# %%
import requests
import urllib
import time
from os import system, name

# %%
# test run for a single case (august 1 2018)
"""
url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/2018/08/smoke20180801.kml"
filename = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/kml_smoke_polygons/smoke2018/smoke20180801.kml"  # or specify the whole path

# get the file from url and save to to filename
r = requests.get(url)
with open(filename, "wb") as code:
    code.write(r.content)
"""

# %%
# clear the screen between download messages
def clear():
    """
    clear screen while executing in terminal
    https://www.geeksforgeeks.org/clear-screen-python/
    """
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


# %%
# get all the .kml files and save them in a folder called smoke_kml, sorted by month
base_url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/"

years = range(2009, 2021)
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09"] + list(range(10, 32))

counter = 0
# limit to 5 file loops for now
for year in years:
    year = str(year)
    for month in months:
        month = str(month)
        for day in days:
            if counter <= 5:
                day = str(day)
                url = (
                    base_url
                    + year
                    + "/"
                    + month
                    + "/"
                    + "smoke"
                    + year
                    + month
                    + day
                    + ".kml"
                )
                filename = (
                    "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/kml_smoke_polygons/smoke"
                    + year
                    + "/"
                    + "smoke"
                    + year
                    + month
                    + day
                    + ".kml"
                )

                counter += 1
                print("successfully downloaded " + str(counter) + " kml files")
                time.sleep(1)
                clear()


# %%
