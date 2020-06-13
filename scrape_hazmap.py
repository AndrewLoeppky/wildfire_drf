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


# %%
url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/2018/08/"
filename = "smoke20180801.kml"  # or specify the whole path


# downloading with requests

# import the requests library
import requests


# download the file contents in binary format
r = requests.get(url)

# open method to open a file on your system and write the contents
with open(filename, "wb") as code:
    code.write(r.content)


# %%


# %%


# %%
# Loop through all urls with smoke shapefiles in them
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
