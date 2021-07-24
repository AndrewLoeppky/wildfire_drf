# %% [markdown]
# # Process Ameriflux
#
# Author: Andrew Loeppky
# Project: DRF effect from wildfire smoke events, Dr. Ian Mckendry
#
# This code is for processing ameriflux data for OBS and OAS
#
# URL to download files: https://ameriflux.lbl.gov/sites/site-search/#searchbar=CA&filter-type=all&has-data=All&site_id=
#
# download manifest provided by site:
# ```
# #emailForSitePIs:andrew.black@ubc.ca
# #dataFiles
# SITE_ID,filename,start_year,end_year,version,filetype,timestamp
# CA-Oas,AMF_CA-Oas_BASE_HH_1-1.csv,1996,2010,1-1,FLUX-MET,201606150037
# CA-Obs,AMF_CA-Obs_BASE_HH_1-1.csv,1997,2010,1-1,FLUX-MET,201608150043
# ```
#
# Parameter list (from the README)
#
# ```-- TIMEKEEPING
# TIMESTAMP_START (YYYYMMDDHHMM): ISO timestamp start of averaging period
# TIMESTAMP_END   (YYYYMMDDHHMM): ISO timestamp end of averaging period
#
# -- GASES
# CO2         (umolCO2 mol-1): Carbon Dioxide (CO2) mole fraction
# H2O           (mmolH2O mol-1): Water (H2O) vapor mole fraction
# CH4        (nmolCH4 mol-1): Methane (CH4) mole fraction
# FC            (umolCO2 m-2 s-1): Carbon Dioxide (CO2) flux
# SC            (umolCO2 m-2 s-1): Carbon Dioxide (CO2) storage flux
# FCH4        (nmolCH4 m-2 s-1): Methane (CH4) flux
# SCH4        (nmolCH4 m-2 s-1): Methane (CH4) storage flux
#
# -- HEAT
# G           (W m-2): Soil heat flux
# H           (W m-2): Sensible heat flux
# LE          (W m-2): Latent heat flux
# SH          (W m-2): Heat storage in the air
# SLE         (W m-2): Latent heat storage flux
#
# -- MET_WIND
# WD            (Decimal degrees): Wind direction
# WS            (m s-1): Wind speed
# USTAR    (m s-1): Friction velocity
# ZL            (adimensional): Stability parameter
#
# -- MET_ATM
# PA             (kPa): Atmospheric pressure
# RH             (%): Relative humidity, range 0-100
# TA             (deg C): Air temperature
# VPD        (hPa): Vapor Pressure Deficit
#
# -- MET_SOIL
# SWC        (%): Soil water content (volumetric), range 0-100
# TS          (deg C): Soil temperature
# WTD        (m): Water table depth
#
# -- MET_RAD
# NETRAD       (W m-2): Net radiation
# PPFD_IN      (umolPhoton m-2 s-1): Photosynthetic photon flux density, incoming
# PPFD_OUT     (umolPhoton m-2 s-1): Photosynthetic photon flux density, outgoing
# SW_IN       (W m-2): Shortwave radiation, incoming
# SW_OUT       (W m-2): Shortwave radiation, outgoing
# LW_IN        (W m-2): Longwave radiation, incoming
# LW_OUT      (W m-2): Longwave radiation, outgoing
#
# -- MET_PRECIP
# P              (mm): Precipitation
#
# -- PRODUCTS
# NEE        (umolCO2 m-2 s-1): Net Ecosystem Exchange
# RECO        (umolCO2 m-2 s-1): Ecosystem Respiration
# GPP        (umolCO2 m-2 s-1): Gross Primary Productivity
# ```

# %%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# display all columns
pd.options.display.max_columns = None

# %%
# read in data from hard drive

obs_path = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/ameriflux/AMF_CA-Obs_BASE_HH_1-1.csv"
oas_path = "C:/Users/Owner/Wildfire_Smoke_Mckendry/data/ameriflux/AMF_CA-Oas_BASE_HH_1-1.csv"

obs = pd.read_csv(obs_path, skiprows=2)
oas = pd.read_csv(oas_path, skiprows=2)

# %%
# change -9999 to NaN
obs = obs.replace(-9999.0, np.nan)
oas = oas.replace(-9999.0, np.nan)

# %%
# make the datetimes into datetimes
obs["TIMESTAMP_START"] = pd.to_datetime(obs["TIMESTAMP_START"], format="%Y%m%d%H%M")
obs["TIMESTAMP_END"] = pd.to_datetime(obs["TIMESTAMP_END"], format="%Y%m%d%H%M")

oas["TIMESTAMP_END"] = pd.to_datetime(oas["TIMESTAMP_START"], format="%Y%m%d%H%M")
oas["TIMESTAMP_END"] = pd.to_datetime(oas["TIMESTAMP_END"], format="%Y%m%d%H%M")

# %%
obs = obs.resample("1H",on="TIMESTAMP_START").mean()
obs = oas.resample("1H",on="TIMESTAMP_START").mean()

# %%
obs.plot("TIMESTAMP_START", ["NEE_PI","RECO_PI"])

# %%
# save columns with CO2 fluxes as a csv 
obs.to_csv("")
oas.to_csv("")

# %% [markdown]
# ## Possible algorithm
#
# 1) apply time averaging filters to each dataset individually to remove measurement artifacts and properly reflect the characteristic timescale of each measured variable
#     
#         smoke (HMS) -- long range smoke effects have a characteristic time period of half a day or so, smoke does not suddenly appear and dissapear as described by HMS data
#     
#         fluxes (NEE and RECO) -- measured with a sonic anemometer so the characteristic time is milleseconds. could apply smoothing anyway? Consult a statistician to see if this is indeed a good idea
#         
#         aeronet (AOD500) -- hourly reported AODs will be the average of ~4 measurements (CIMELs sampling interval is a function of solar angle, not time). Minimalist smoothing algorithm maybe?
#         
# 2) Separate smokey days from non smokey days, or into "low," "med," and "high" if applicable (HAZMAP is binary smoke/non smoke before 2009). Look for covariance with AOD, T, RH, etc to identify possible third variables thay may complicate the DRF effect. Make sure covariance algorithm allows for time lags, accounts for seasonality (smoke is seasonal, as is the GPP of a forest, although they may or may not be strongly linked)
#
# 3) Report results...? how
#         
