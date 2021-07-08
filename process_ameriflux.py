# %% [markdown]
# Process Ameriflux
#
# Author: Andrew Loeppky
# Project: DRF effect from wildfire smoke events, Dr. Ian Mckendry
#
# This code is for processing ameriflux data for OBS and OAS
#
# URL to download files: https://ameriflux.lbl.gov/sites/site-search/#searchbar=CA&filter-type=all&has-data=All&site_id=
#
# download manifest provided by site:
# #emailForSitePIs:andrew.black@ubc.ca
# #dataFiles
# SITE_ID,filename,start_year,end_year,version,filetype,timestamp
# CA-Oas,AMF_CA-Oas_BASE_HH_1-1.csv,1996,2010,1-1,FLUX-MET,201606150037
# CA-Obs,AMF_CA-Obs_BASE_HH_1-1.csv,1997,2010,1-1,FLUX-MET,201608150043
#

# %%
import pandas as pd
from matplotlib import pyplot as plt

# %%
