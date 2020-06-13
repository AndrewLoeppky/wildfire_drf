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
import bs4

# %%
# test run for a single case
url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/2018/08/"
filename = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/kml_smoke_polygons/smoke2009/big_smokey.kml"  # or specify the whole path

r = requests.get(str(url + filename))
with open(filename, "wb") as code:
    code.write(r.content)

# %%
# get all the .kml files and save them in a folder called smoke_kml, sorted by month
base_url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/"

years = range(2009, 2021)
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09"] + list(range(10, 32))

for year in years:
    year = str(year)
    for month in months:
        month = str(month)
        for day in days:
            day = str(day)
            the_url = (
                base_url
                + year
                + "/"
                + month
                + "/"
                + day
                + "/"
                + "smoke"
                + year
                + month
                + day
                + ".kml"
            )
            filename = "smoke" + year + month + day + ".kml"

# %%
base_url = (
    "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/"
)

years = range(2005, 2021)
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

for year in years:
    year = str(year)
    for month in months:
        print(base_url + year + "/" + month + "/")


# %%
