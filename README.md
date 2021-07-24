<!-- #region -->
# Effects of Large Scale Smoke Events on Forest Productivity in Central Canada

Code Author: Andrew Loeppky

Supervisor: Dr. Ian Mckendry

This code repository is meant to acquire and process long-term timeseries related to smoke events throughout Canada and draw conclusions about the effects of high optical-depth smoke events on ecosystems ability to act as atmospheric CO2 sinks. In the current state, all code is aimed at the Old Black Spruce/Waskesiu Aeronet sites in Prince Albert National Park, SK, CAN, but efforts have been made to write code that is as general as possible, so analyses can be performed at other locations with both Ameriflux and AERONET stations.

## Data Sources and Processing Routines

### Aerocan

Aerocan is the Canadian division of AERONET, a global network of sun photometers, the measurement of interest to this study is the aerosol optical depth in the photosynthetically active radiation band (currently represented by the 500nm measurement, although the code can be configured to process more bands or a wider average)

https://aeronet.gsfc.nasa.gov/cgi-bin/data_display_aod_v3?site=Waskesiu&nachal=2&level=1&place_code=10

To acquire this data, follow the URL above and download the AOD level 1.5 data (at Waskesiu or from your site of choice, be sure to credit the site PI for data used). Unzip the file and change the file extension from `filename.lev15` to `filename.csv`

### `process_aeronet.py`

Once the data is downloaded, open `process_aeronet.py` in an editor (I'm using jupyter notebooks adapted to write .py files, see [jupytext docs](https://pypi.org/project/jupytext/) or [VScode extension for jupyter](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)) and modify the file paths (cell 2 and the `main()` function call at the end of the code) to point to your raw dataset. Run the program to produce a cleaned csv file. (modify the function `save_dataset()` to choose where to save your output)


### Hazard Mapping System

The wildfire hazard mapping system (HMS) is a series of satallite data products generated by NOAA to do with North American wildfires. The main site for the hazard mapping system can be found [here](https://www.ospo.noaa.gov/Products/land/hms.html#maps), however, this project accesses data from the data archives found at:

https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/

For processing short datasets, shapefiles describing smoke plumes can be downloaded manually from this website. For longer datasets, use the `scrape_hazmap.py` program to save the data to your local disk for further processing. Smoke polygons are available in KML (i.e. google earth) or shapefile (i.e. arcGIS) formats, and `scrape_hazmap.py` included functionality for aquiring either. Note the scraper takes ~12 hours to run over a 20 year period depending on your processor. The author recommends first running a short interval to make sure it is working, then ask for the full dataset.

After downloading or scraping the data over your specified time interval, 



### Ameriflux

Ameriflux is a network of field sites throughout north, central and south america dedicated to monitoring CO2, water, and energy fluxes. Data can be found here:

https://ameriflux.lbl.gov/sites/site-search/#searchbar=CA&filter-type=all&has-data=All&site_id=

Which data products are available depend on site-specific instrumentation. See particular site metadata for further details.


<!-- #endregion -->
