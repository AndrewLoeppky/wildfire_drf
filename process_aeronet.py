# %%
# %% [markdown]
# # Effects of Wildfire Smoke on Forest Productivity in Central Canada.
# ## Data Aquisition and Scrubbing - Function Library
# Program Author: Andrew Loeppky <br>
# Supervising Professor: Dr. Ian Mckendry <br>
# Date: May 2020
#

# %%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
#import scipy
import datetime
import time
import os

pd.set_option("display.max_columns", None)


# %%
### read in data

# test data (JFM in 2020)
wask_aod_test_10 = pd.read_csv(
    "C:/Users/Owner/Wildfire_Smoke_Mckendry/code/Waskesiu_lev10.csv", skiprows=6
)
wask_aod_test_15 = pd.read_csv(
    "C:/Users/Owner/Wildfire_Smoke_Mckendry/code/Waskesiu_lev15.csv", skiprows=6
)

# full length sets (1993-2020)
wask_aod_10 = pd.read_csv('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/Waskesiu10.csv', skiprows=6)
wask_aod_15 = pd.read_csv('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/Waskesiu15.csv', skiprows=6)
wask_aod_20 = pd.read_csv('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/Waskesiu20.csv', skiprows=6)

# total AOD, whatever that means
wask_tot_10 = 0
wask_tot_15 = 0
wask_tot_20 = 0 

# test longer dataset
long_test = pd.read_csv('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/Waskesiu_long_test10.csv', skiprows=6)


# %%

### Get rid of -999.0 values
def replace_999(dataset):
    """replaces default -999 with numpy NaN
    """
    dataset = dataset.replace(-999.0, np.nan)
    return dataset


# %%
### Drop empty columns
def drop_empty(dataset):
    """if column name contains the string "Empty", drop it
    """
    for index in dataset.columns:
        if "Empty" in index:
            dataset.drop([index], axis=1, inplace=True)

    return dataset


# %%
### Properly reformat date and time scipy datetime
def reformat_datetime(dataset):
    """generates a datetime column for aeronet formatted raw data, drops old columns
    """
    dataset["year"] = dataset["Date(dd:mm:yyyy)"].str[6:11]
    dataset["month"] = dataset["Date(dd:mm:yyyy)"].str[3:5]
    dataset["day"] = dataset["Date(dd:mm:yyyy)"].str[0:2]

    dataset["hour"] = dataset["Time(hh:mm:ss)"].str[0:2]
    dataset["minute"] = dataset["Time(hh:mm:ss)"].str[3:5]
    dataset["second"] = dataset["Time(hh:mm:ss)"].str[6:8]

    dataset["datetime"] = pd.to_datetime(
        dataset[["year", "month", "day", "hour", "minute", "second"]]
    )
    dataset.drop(
        [
            "Date(dd:mm:yyyy)",
            "Time(hh:mm:ss)",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
        ],
        axis=1,
        inplace=True,
    )

    return dataset


# %%
def keep_relevant(dataset):
    """
    keeps only select columns
    """
    relevant_cols = ["AOD_1640nm",
                     "AOD_1020nm",
                     "AOD_870nm",
                     "AOD_865nm",
                     "AOD_779nm",
                     "AOD_675nm",
                     "AOD_667nm",
                     "AOD_620nm",
                     "AOD_560nm",
                     "AOD_555nm",
                     "AOD_551nm",
                     "AOD_532nm",
                     "AOD_531nm",
                     "AOD_510nm",
                     "AOD_500nm",
                     "AOD_490nm",
                     "AOD_443nm",
                     "AOD_440nm",
                     "AOD_412nm",
                     "AOD_400nm",
                     "AOD_380nm",
                     "AOD_340nm",
                     "Precipitable_Water(cm)",
                     "AOD_681nm",
                     "AOD_709nm",
                     "Ozone(Dobson)",
                     "NO2(Dobson)"
                     ]
    return dataset[relevant_cols]


# %%
def resample_hourly(dataset):
    """creates hourly data with pandas resample. Please replace this with a proper 
    interpolation algorithm before publishing results
    
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
    """
    dataset = dataset.resample("1H",on="datetime").mean()
    return dataset


# %%
### Plotting function
def plot_aod(dataset):
    fig, ax = plt.subplots(1, 1, figsize=(20, 8))

    for index in dataset.columns:
        if index[0:3] == "AOD":
            ax.scatter(dataset["datetime"], dataset[index], label=index, alpha=0.5)

    ax.set_title("Test Time Series of AOD at All Available $\lambda$")
    ax.set_xlabel("Date")
    ax.set_ylabel("AOD")
    ax.legend(loc="best")

    plt.savefig("AOD_timeseries.png", dpi=150)


# %%
### timer decorator function from the internet
def timeit(method):
    """
    https://www.laurivan.com/braindump-use-a-decorator-to-time-your-python-function/
    """

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        elapsed = te - ts

        # print(f'time to generate plot: {elapsed}s')
        return result, elapsed

    return timed


# %%
def save_dataset(dataset, cols=["AOD_500nm"]):
    """
    saves pd dataframe as a .csv in the local directory, or modify this to include a path
    default includes only datetime and 500nm optical depth, add data to arg "cols" as needed
    """
    save_data = pd.DataFrame()
    save_data["datetime"] = dataset["datetime"]
    for col in cols:
        save_data[col] = dataset[col]
    try:
        os.remove("../data/out_data/dataaeronet_aod.csv") # delete the old file if it exists
    except:
        pass
    
    save_data.to_csv("../data/out_data/dataaeronet_aod.csv") # save the current one


# %%
@timeit
def main(dataset):
    data = replace_999(dataset)
    data = drop_empty(data)
    data = reformat_datetime(data)
    data = resample_hourly(data)
    data = keep_relevant(data)    
    data.to_csv("../data/out_data/aeronet_aod.csv")


# %%
main(wask_aod_15)


# %%

# %%

# %%

# %%
