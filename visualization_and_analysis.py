#!/usr/bin/env python
# coding: utf-8

# ## Link to github repository:
# https://github.com/manqili0127/DSCI510_Final.git

# In[1]:


import pandas as pd
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import requests
import urllib
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# In[2]:


def concat_data(population_file, air_file, climate_file):
    '''
    This function is used to preprocess collected data and concat all into one dataframe
    Args:
        df: population csv, air quality csv, climate csv
    Returns:
        new df with population, air quality, and climate data
    '''
    #population data
    df_population = pd.read_csv (population_file,sep='\t')
    df_population=df_population.drop('Unnamed: 0', axis=1)
    df_population=df_population.rename(columns={"y-2016": "population"})
    df_population=df_population.iloc[:,[0,2,3,1]]
    
    # air quality data
    df_air_quality = pd.read_csv (air_file,sep='\t')
    df_air_quality=df_air_quality.drop('Unnamed: 0', axis=1)
    
    # climate data
    df_climate = pd.read_csv (climate_file,sep='\t')
    df_climate=df_climate.drop('Unnamed: 0', axis=1)
    
    # concat
    df_concat = pd.concat([df_population, df_air_quality, df_climate], axis=1)
    
    return df_concat

def get_fips(df_concat):
    '''
    This function is used to get the fips from lat and lon
    Args:
        df with population, air quality, and climate data
    Returns:
        new df with population, air quality, climate, and fips
    '''
    # create fips from lat and lon
    for i in range (len(df_concat)):
        #Sample latitude and longitudes
        lat = df_concat.loc[i,'latitude']
        lon = df_concat.loc[i,'longitude']

        #Contruct request URL
        params = 'latitude='+str(lat)+'&longitude='+str(lon)+'&format=json'
        url = 'https://geo.fcc.gov/api/census/block/find?' + params

        #Get response from API
        response = requests.get(url)

        #Parse json in response
        #get FIPS code
        data = response.json()
        fips=data['County']['FIPS']

        df_concat.loc[i,'fips']=fips
    return df_concat



def choropleth_map_plot(df_concat_fips):
    '''
    This function is used to plot choropleth map of overall air quality index distribution in California
    Args:
        df with population, air quality, climate, and fips
    Returns:
        choropleth map figure
    '''
    df_map=df_concat[['fips','aqi']]
    fig = px.choropleth_mapbox(df_map, geojson=counties, locations='fips', color='aqi',
                               color_continuous_scale="dense",
                               range_color=(df_map['aqi'].min(), df_map['aqi'].max()),
                               mapbox_style="carto-positron",
                               zoom=4.3, center = {"lat": 37.9577, "lon": -121.2908},
                               opacity=0.5,
                               labels={'aqi':'Air quality index'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def histogram_plot(df_concat_fips):
    '''
    This function is used to plot the air quality index histogram
    Args:
        df with population, air quality, and climate data
    Returns:
        none. (plot inside the function)
    '''
    fig, ax = plt.subplots()
    data = df_concat_fips['aqi']

    N, bins, patches = ax.hist(data, edgecolor='white', linewidth=1, bins=15)

    for i in range(0,3):
        patches[i].set_facecolor('green')
    for i in range(3,7):    
        patches[i].set_facecolor('yellow')
    for i in range(7, 11):
        patches[i].set_facecolor('orange')
    for i in range(11, 15):
        patches[i].set_facecolor('red')

    green_patch = mpatches.Patch(color='green', label='Good')
    yellow_patch = mpatches.Patch(color='yellow', label='Moderate')
    orange_patch = mpatches.Patch(color='orange', label='Unhealthy for sensitive groups')
    red_patch = mpatches.Patch(color='red', label='Unhealthy')
    plt.legend(handles=[green_patch,yellow_patch,orange_patch,red_patch])

    ax.set_ylim([0,280]) 


    plt.xlabel('Air quality index')
    plt.ylabel('Count')
    plt.title("Air quality index histogram")
    plt.savefig("Air quality index histogram.pdf")
    plt.show()

# make autopct for pie chart
def make_autopct(values):
    '''
    This function is used to return autopct for pie chart
    Args:
        np.array of data for pie chart
    Returns:
        nautopct setting
    '''
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def pie_chart_plot(df_concat_fips):
    '''
    This function is used to plot the air quality level pie chart
    Args:
        df with population, air quality, and climate data
    Returns:
        none. (plot inside the function)
    '''
    #aqi level:
    # <50:good, 50~100: moderate, 100~150: unhealthy for sensitive groups, >150: unhealthy
    count_good=df_concat_fips['aqi'].where(df_concat_fips['aqi'] < 50).count()
    count_moderate=df_concat_fips['aqi'].where((df_concat_fips['aqi'] >= 50)&(df_concat_fips['aqi'] < 100)).count()
    count_sensitive=df_concat_fips['aqi'].where((df_concat_fips['aqi'] >= 100)&(df_concat_fips['aqi'] < 150)).count()
    count_unhealthy=df_concat_fips['aqi'].where(df_concat_fips['aqi'] >= 150).count()
    values = np.array([count_good, count_moderate, count_sensitive, count_unhealthy])
    mylabels = ["Good", "Moderate", "Unhealthy for sensitive groups", "Unhealthy"]
    myexplode = [0.1, 0, 0, 0]

    plt.pie(values, labels = mylabels, explode = myexplode, shadow = True,colors = ['green','yellow','orange','red'], autopct=make_autopct(values))
    plt.title("Air quality level distribution")
    plt.savefig("Air quality level distribution.pdf")
    plt.show() 

def box_plot(df_concat_fips):
    '''
    This function is used to plot  boxplot of air polutant concentrationst
    Args:
        df with population, air quality, and climate data
    Returns:
        none. (plot inside the function)
    '''
    sns.boxplot(data=df_concat_fips.drop(['aqi','zip_code','latitude','longitude','population',
                                                        'wind_degree','humidity', 'temp_c'],axis=1));
    plt.xlabel('Major pollutants')
    plt.ylabel('Concentration index')
    plt.title("Air polutant concentrations")
    plt.savefig("Air polutant concentrations.pdf")    

    
    
def OLS_regression_results(X,y):
    '''
    This function is used to do OLS regression and print results
    Args:
        X:independent data, y:dependent data
    Returns:
        reguression model
    '''
    # Adding a constant to get an intercept
    X_constant = sm.add_constant(X)
    # Fitting the resgression line using 'OLS'
    lr = sm.OLS(y, X_constant).fit()
    # fiting sum
    return lr

def plot_regression_model(const,slop, X, y):
    '''
    This function is used to plot_regression_model with original data
    Args:
        const: constant of regression model, slope: slope of regression model,
        slopX:independent data, y:dependent data
    Returns:
        none(plot inside function)
    '''
# Visualizing the regression line
    plt.scatter(X, y)
    plt.plot(X, const  +slope *X, 'r')
    plt.xlabel('CO')
    plt.ylabel('NO2')
    plt.title('simple linear regression model CO to predict NO2')
    plt.savefig("simple linear regression model CO to predict NO2.pdf")
    plt.show()



if __name__ == '__main__':
    # get files
    population_file='population_zipcode_lat_lon.csv'
    air_file='air_quality.csv'
    climate_file='climate.csv'
    df_concat=concat_data(population_file, air_file, climate_file)
    
    # get fips
    df_concat_fips=get_fips(df_concat)
    
    
    # plot choropleth map of overall air quality index distribution in California
    fig=choropleth_map_plot(df_concat_fips)
    fig.show()

    # plot the air quality index histogram    
    histogram_plot(df_concat_fips)

    # air quality index statistical summary
    print(df_concat_fips[['aqi']].describe())

    # plot pie chart of air quality level
    pie_chart_plot(df_concat_fips)

    # plot boxplot of air polutant concentrations
    box_plot(df_concat_fips)

    # pairplot of air polutant concentrations
    rel=sns.pairplot(df_concat_fips.drop(['aqi','zip_code','latitude','longitude','population',
                                                            'wind_degree','humidity', 'temp_c'],axis=1))
    rel.fig.suptitle('Air poplutant concentration pairplot',y=1.03)

    # correlation matrix heatmap of air polutant concentrations
    sns.heatmap(df_concat_fips.drop(['aqi','zip_code','latitude','longitude','population',
                                                            'wind_degree','humidity', 'temp_c'],axis=1).corr());
    plt.title("Air pollutants correlation heatmap")
    plt.savefig("Air pollutants correlation heatmap.pdf")
    
    # Creating X and y with preditor 'CO' and 'NO2'
    X = df_concat_fips['CO']
    y = df_concat_fips['NO2']
    result=OLS_regression_results(X,y)
    print(result.summary())

    # plot regression model to predict'NO2' with 'CO'
    const=result.params[0]
    slope=result.params[1]
    plot_regression_model(const,slope, X, y)

    # Creating X and y with preditor 'PM2.5' and 'PM10'
    X = df_concat_fips['PM2.5']
    y = df_concat_fips['PM10']
    result=OLS_regression_results(X,y)
    print(result.summary())

    # plot regression model to predict'NO2' with 'CO'
    const=result.params[0]
    slope=result.params[1]
    plot_regression_model(const,slope, X, y)

    # plot correlation matrix of aqi, climate and population 
    print(df_concat_fips[['aqi','wind_degree','humidity','temp_c','population']].corr(method='pearson'))

