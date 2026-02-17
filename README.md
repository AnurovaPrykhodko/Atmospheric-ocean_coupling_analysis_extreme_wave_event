# Atmospheric-ocean coupling analysis of an extreme wave event (ongoing):
This repository contains preprocessing and exploratory analysis of atmospheric and wave conditions associated with an extreme wave event that occurred at the Canary Islands in December 2025. 
The processed data will be used for a course project in multivariate statistical analysis. 
For the multivariate analysis, the goal is to investigate the spatial and temporal coupling between wind forcing and the wave event.

Implements Python 3.13, NumPy, Xarray, Pandas, Cartopy, and Matplotlib.

Data: Hourly ERA5 reanalysis downloaded for latitude: 10°N – 60°N, longitude: 60°W – 10°E, period: December 2025.

Variables:
- Surface pressure
- 10m u component wind
- 10m v component wind
- Significant wave height combined
- Significant height of total swell
- Significant height of wind waves
- Peak wave period

## List of content:

### my_functions.py: custom functions

### preprocessing.ipynb: Jupyter Notebook containing the preprocessing. The objective is to identify forcing and location regions for the wave event, which is done by
- Computing daily anomalies of min sea surface pressure, max mean wind speed, and max significant height of wind waves, swell and combined waves.
- Identification of extreme forcing and event dates
- Visualization of extreme dates to select regions
- Converting data into a data frame.
- Exporting to CSV.
