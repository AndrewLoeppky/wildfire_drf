import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import scipy
import datetime
import time


def load_files():
    # shortened files for debugging/testing
    wask_aod_test_10 = pd.read_csv(
        "C:/Users/Owner/Wildfire_Smoke_Mckendry/code/Waskesiu_lev10.csv", skiprows=6
    )
    wask_aod_test_15 = pd.read_csv(
        "C:/Users/Owner/Wildfire_Smoke_Mckendry/code/Waskesiu_lev15.csv", skiprows=6
    )
    """
    # full length sets (1993-2020)
    wask_aod_10 = pd.read_csv('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/Waskesiu10.csv', skiprows=6)
    wask_aod_15 = pd.read_csv('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/Waskesiu15.csv', skiprows=6)
    wask_aod_20 = pd.read_csv('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/Waskesiu20.csv', skiprows=6)

    # total AOD, whatever that means
    wask_tot_10 = 0
    wask_tot_15 = 0
    wask_tot_20 = 0 
    """
    return wask_aod_test_10


def drop_empty(dataset):
    """if column name contains the string "Empty", drop it
    """
    for index in dataset.columns:
        if "Empty" in index:
            dataset.drop([index], axis=1, inplace=True)


def replace_999(dataset):
    """replaces default -999 with numpy NaN
    """
    dataset.replace(-999.0, np.nan, inplace=True)


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


def plot_aod(dataset):
    """Function for plotting aeronet dataset
    """
    fig = plt.figure()
    '''
    for index in dataset.columns:
        if index[:3] == "AOD":
            plt.scatter(dataset['datetime'], dataset[index])
    '''

    plt.scatter(dataset['datetime'], dataset['AOD_1640nm'])
    plt.scatter(dataset['datetime'], dataset['AOD_870nm'])
    plt.savefig('C:/Users/Owner/Wildfire_Smoke_Mckendry/data/out_data/sample_fig.png')


def main():
    data = load_files()
    drop_empty(data)
    replace_999(data)
    reformat_datetime(data)
    data.to_csv(r"C:/Users/Owner/Wildfire_Smoke_Mckendry/data/out_data/sample_data.csv")
    plot_aod(data)
    # print(data)


if __name__ == "__main__":
    main()
