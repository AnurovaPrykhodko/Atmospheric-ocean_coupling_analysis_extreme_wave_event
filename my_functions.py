import numpy as np
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

def compute_anomaly(ds, variable, method, window_hours):
    """
    Compute smoothed variable, anomaly, and daily aggregated anomaly.
    
    Parameters
    ----------
    ds : xr.Dataset
        Dataset containing the specified variable with 'valid_time' dimension.
    variable : str
        Name of the variable to process.
    method : str
        Aggregation method: 'mean', 'max', or 'min'.
    window_hours : int
        Rolling window size in hours.
    
    Returns
    -------
    xr.Dataset
        Dataset with added variables:
        - {variable}_smooth: rolling aggregation of the variable
        - {variable}_anomaly: variable minus smooth
        - {variable}_anomaly_{method}: daily aggregation of anomaly
    """
    ds[f'{variable}_smooth'] = ds[variable].rolling(valid_time=window_hours, center=True).mean()
    # Anomaly from the smoothed signal
    ds[f'{variable}_anomaly'] = ds[variable] - ds[f'{variable}_smooth']
    
    if method == 'max':
        anomaly_daily = ds[f'{variable}_anomaly'].groupby('valid_time.date').max()
    if method == 'mean':
        anomaly_daily = ds[f'{variable}_anomaly'].groupby('valid_time.date').mean()

    if method == 'min':
       anomaly_daily = ds[f'{variable}_anomaly'].groupby('valid_time.date').min()     

    anomaly_daily['date'] = pd.to_datetime(anomaly_daily['date'])
    ds[f'{variable}_anomaly_{method}'] = anomaly_daily
    
    return ds

def get_extreme_dates(ds, variable, start_date, end_date, method, n=5):
    """
    Find dates with the most extreme values of a variable.
    
    Parameters
    ----------
    ds : xarray.Dataset
        Dataset containing the variable.
    variable : str
        Name of the variable to analyze.
    start_date, end_date : str
        Date range (e.g., '2025-12-02', '2025-12-15').
    method : str
        'max' to find dates with highest values, 'min' for lowest.
    n : int
        Number of dates to return.
    
    Returns
    -------
    numpy.ndarray
        Array of the top n dates.
    """
    ds_subset = ds.sel(date=slice(start_date, end_date))
    
    if method == 'max':
        daily_extreme = ds_subset[variable].max(dim=['latitude', 'longitude'])
        ascending = False
        values_type = 'highest'
    if method == 'min':
        daily_extreme = ds_subset[variable].min(dim=['latitude', 'longitude'])
        ascending = True
        values_type = 'lowest'

    dates = daily_extreme.sortby(daily_extreme, ascending=ascending).date.values[:n]
    values = daily_extreme.sortby(daily_extreme, ascending=False).values[:n]
    print(f'Days with {values_type} values of {variable}: {np.sort(dates)} \n'
          f'Values: {values} \n')
    return dates

def plotting_func(ds, variable, date=None, valid_time=None):
    """
    Plot a variable for a specific date.
    
    Parameters
    ----------
    ds : xarray.Dataset
    date : str
        Date to select (e.g., '2025-12-10').
    valid_time : str
        Valid_time to select (e.g., '2025-12-15T00:00:00').
    variable : str, optional
        Name of the variable to plot.
    
    Returns
    -------
    plots
    """
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    
    if not date == None:
        ds[variable].sel(date=date).plot(ax=ax, transform=ccrs.PlateCarree())
        ax.set_title(f'{variable}, \n date={date}')
    if not valid_time == None:
        ds[variable].sel(valid_time=valid_time).plot(ax=ax, transform=ccrs.PlateCarree())
        ax.set_title(f'{variable}, \n valid_time={valid_time}')
    ax.coastlines()

    #add gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    return plt.show()

def select_variables(ds, name, variables_wanted):
    ds['location'] = ('valid_time', [name] * len(ds.valid_time))
    ds = ds[variables_wanted]
    ds = ds.drop_vars(["number"]) 
    return ds