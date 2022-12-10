#!/usr/bin/env python
# coding: utf-8

# ## Link to github repository:
# https://github.com/manqili0127/DSCI510_Final.git
# 

# In[2]:


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
from visualization_and_analysis import *


# In[3]:


# get files
population_file='population_zipcode_lat_lon.csv'
air_file='air_quality.csv'
climate_file='climate.csv'
df_concat=concat_data(population_file, air_file, climate_file)
print(df_concat.head(5))


# In[4]:


# get fips
df_concat_fips=get_fips(df_concat)


# In[5]:


# plot choropleth map of overall air quality index distribution in California
fig=choropleth_map_plot(df_concat_fips)
fig.show()


# In[6]:


# plot the air quality index histogram    
histogram_plot(df_concat_fips)
# air quality index statistical summary
print(df_concat_fips[['aqi']].describe())
# plot pie chart of air quality level
pie_chart_plot(df_concat_fips)
# plot boxplot of air polutant concentrations
box_plot(df_concat_fips)


# In[7]:


# pairplot of air polutant concentrations
rel=sns.pairplot(df_concat_fips.drop(['aqi','zip_code','latitude','longitude','population',
                                                        'wind_degree','humidity', 'temp_c'],axis=1))
rel.fig.suptitle('Air poplutant concentration pairplot',y=1.03)


# In[8]:


# correlation matrix heatmap of air polutant concentrations
sns.heatmap(df_concat_fips.drop(['aqi','zip_code','latitude','longitude','population',
                                                        'wind_degree','humidity', 'temp_c'],axis=1).corr());
plt.title("Air pollutants correlation heatmap")
plt.savefig("Air pollutants correlation heatmap.pdf")


# In[9]:


# Creating X and y with preditor 'CO' and 'NO2'
X = df_concat_fips['CO']
y = df_concat_fips['NO2']
result=OLS_regression_results(X,y)
print(result.summary())

# plot regression model to predict'NO2' with 'CO'
const=result.params[0]
slope=result.params[1]
plot_regression_model(const,slope, X, y)


# In[10]:


# Creating X and y with preditor 'PM2.5' and 'PM10'
X = df_concat_fips['PM2.5']
y = df_concat_fips['PM10']
result=OLS_regression_results(X,y)
print(result.summary())

# plot regression model to predict'NO2' with 'CO'
const=result.params[0]
slope=result.params[1]
plot_regression_model(const,slope, X, y)


# In[11]:


# plot correlation matrix of aqi, climate and population 
print(df_concat_fips[['aqi','wind_degree','humidity','temp_c','population']].corr(method='pearson'))


# In[ ]:




