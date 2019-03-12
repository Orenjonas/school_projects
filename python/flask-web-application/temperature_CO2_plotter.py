import matplotlib
matplotlib.use('Agg') # pyplot backend for web server usage
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64

"""
Module used for plotting various csv data of temperature and CO2 emissions.
"""

def get_temperature_months_and_years():
    """Returns a list of the months and years included in the dataframe"""
    stats = pd.read_csv('temperature.csv')
    months = list(stats)[1:]
    years = list(stats['Year'])
    return months, years

def get_CO2_years():
    """Returns a list of the years included in the dataframe"""
    stats = pd.read_csv('co2.csv')
    years = list(stats['Year'])
    return years

def make_mask(stats, year_from, year_to):
    """Used by the plot functions to create a masked array for plotting the desired years.

    If year paramaters are None, no elements are masked.

    returns:
        a masked array to use as an index for the dataframe to be plotted.
    """
    if year_from == None:
        year_from = stats['Year'].min()

    if year_to == None:
        year_to = stats['Year'].max()

    mask = (stats['Year'] >= pd.to_datetime(year_from, format='%Y')) & \
           (stats['Year'] <= pd.to_datetime(year_to,   format='%Y'))

    return mask

def plot_temperature(month, year_from=None, year_to=None, y_min=None, y_max=None):
    """ Plot temperatures and store the plot in memory.

    Access the plot in a html document using the img_url string with the following line:
        .. code-block:: html

        <img src="data:image/png;base64,{{img_url}}">

    Args:
        Required:
            month (str): Month to present temperature for
        Optional:
            year_from (str/int): Starting year
            year_to   (str/int): End year
            y_min (int): minimum value on y-axis
            y_max (int): maximum value on y-axis

    returns:
        img_url (str): a base 64 encoded string used for accessing the image stored in memory.

    """
    stats = pd.read_csv('temperature.csv', parse_dates=['Year'])

    mask = make_mask(stats, year_from, year_to)

    stats.loc[mask].plot(x='Year', y=month.capitalize(), ylim=(y_min,y_max))

    # Create a unique image address with bytes
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def plot_CO2(year_from=None, year_to=None, y_min=None, y_max=None):
    """ Plot CO2 emission values and store the plot in memory.

    Access the plot in a html document using the img_url string with the following line:
    ``` html
    <img src="data:image/png;base64,{{img_url}}">
    ```

    Args:
        Optional:
            year_from (str/int): Starting year
            year_to   (str/int): End year
            y_min (int): minimum value on y-axis
            y_max (int): maximum value on y-axis

    returns:
        a base 64 encoded string used for accessing the image stored in memory.

    """
    stats = pd.read_csv('co2.csv', parse_dates=['Year'])

    mask = make_mask(stats, year_from, year_to)

    stats.loc[mask].plot(x='Year', ylim=(y_min,y_max))

    # Create a unique image address with bytes
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def bar_CO2(lower, upper):
    """ Plot bar chart of countries with CO2 emission values in the given treshold and store the plot in memory.

    Access the plot in a html document using the img_url string with the following line:
    ``` html
    <img src="data:image/png;base64,{{img_url}}">
    ```

    Args:
        lower (str/int/float): lower threshold
        upper (str/int/float): upper threshold

    returns:
        a base 64 encoded string used for accessing the image stored in memory.
    """
    stats = pd.read_csv('CO2_by_country.csv')
    stats.set_index('Country Name')

    lower = 18 if (lower == None or lower >  20) else float(lower)
    upper = 25 if (upper == None or upper <= lower) else float(upper)

    year = '2013'
    countries = stats.loc[(stats[year] >= lower) & (stats[year] <= upper)] # dafaframe of countries with emissinsion in threshold

    countries.plot(x="Country Name", y=year, kind='bar')
    plt.ylabel('CO2 emissions (metric tons per capita')
    plt.title('CO2 emissions in 2013')
    plt.legend().remove()
    plt.tight_layout()

    # Create a unique image address with bytes
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url
