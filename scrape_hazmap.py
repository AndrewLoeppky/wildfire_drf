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
import gzip
import shutil

# %%
# test run for a single case (july 29 2009)
"""
# url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/2011/08/smoke20110801.kml"
# filename = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/kml_smoke_polygons/smoke2011/smoke20110801.kml"

url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/2009/07/smoke20090729.kml"
filename = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/kml_smoke_polygons/smoke2009/smoke20090729.kml"

# if the file exists, download and save
# note status code 200 = file exists
# 404 = file does not exist
r = requests.get(url)

if r.status_code == 200:
    with open(filename, "wb") as code:
        code.write(r.content)
    # dwldcounder += 1
    print("Downloading KML for date = [date]")
    print("url = " + url)

# catch case for zipped files (.gz), or ignore them if they don't exist
elif r.status_code != 200:
    url = url + ".gz"
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, "wb") as code:
            code.write(gzip.decompress(r.content))
        print("Downloading KML for date = [date]")
        print("url = " + url)
    else:
        print("No files found at [date]")

# this shouldnt ever happen
else:
    print("status code " + str(r.status_code))
    print("Crashed at date = [date]")
    # break
"""

# %%
# get all the .kml files and save them in a folder called smoke_kml, sorted by year
base_url = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/KML/"

years = range(2009, 2021)
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

                if r.status_code == 200:
                    with open(filename, "wb") as code:
                        code.write(r.content)
                    dwldcounder += 1
                    print(
                        "Downloading KML for date = " + year + "/" + month + "/" + day
                    )
                    print("url = " + url)

                # check if files are zipped (.gz) and extract
                elif r.status_code != 200:
                    url = url + ".gz"
                    r = requests.get(url)
                    if r.status_code == 200:
                        with open(filename, "wb") as code:
                            code.write(gzip.decompress(r.content))
                        dwldcounder += 1
                        print(
                            "Downloading KML for date = "
                            + year
                            + "/"
                            + month
                            + "/"
                            + day
                        )
                        print("url = " + url)

                    else:
                        print(
                            "No file found at date = " + year + "/" + month + "/" + day
                        )
                        print("url = " + url)

                # this shouldnt happen
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
