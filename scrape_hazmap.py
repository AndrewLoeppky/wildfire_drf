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
import gzip

# %%
# test run for a single case (july 29 2009)

# url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/2009/01/smoke20090101.kml"
# filename = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/kml_smoke_polygons/smoke2018/smoke20090101.kml"

url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/2009/07/smoke20090729.kml"
filename = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/kml_smoke_polygons/smoke2009/smoke20090729.kml"

# if the file exists, download and save
r = requests.get(url)

if str(r) == "<Response [200]>":
    with open(filename, "wb") as code:
        code.write(r.content)
    # dwldcounder += 1
    print("Downloading KML for date = [date]")
    print("url = " + url)

elif str(r) == "<Response [404]>":
    url = url + ".gz"
    r = requests.get(url)
    if str(r) == "<Response [200]>":
        with gzip.open(filename, "wb") as code:
            code.write(r.content)
        print("Downloading KML for date = [date]")
        print("url = " + url)
    else:
        print("No files found at [date]")

else:
    print("Crashed at date = [date]")
    # break


# %%
# get all the .kml files and save them in a folder called smoke_kml, sorted by year
# note: currently cannot handle .gz zip files... a task for tomorrow i guess
base_url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/"

years = range(2011, 2021)
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09"] + list(range(10, 32))

parsecounter = 0
dwldcounder = 0
for year in years:
    year = str(year)
    for month in months:
        month = str(month)
        for day in days:
            if parsecounter <= 10000:  # hard limit ~ 25 years
                day = str(day)

                # make variables that match website conventions
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

                # if the file exists, download and save
                r = requests.get(url)

                if str(r) == "<Response [200]>":
                    with open(filename, "wb") as code:
                        code.write(r.content)
                    dwldcounder += 1
                    print(
                        "Downloading KML for date = " + year + "/" + month + "/" + day
                    )
                    print("url = " + url)

                elif str(r) == "<Response [404]>":
                    print("No file found at date = " + year + "/" + month + "/" + day)
                    print("url = " + url)

                else:
                    print("Crashed at date = " + year + "/" + month + "/" + day)
                    break

                # housekeeping
                parsecounter += 1
                print(str(parsecounter) + " days parsed")
                print(str(dwldcounder) + " files downloaded\n")
                time.sleep(1)


# %%
# get all the
