# Link to github repository:
# https://github.com/manqili0127/DSCI510_Final.git


import pandas as pd
import pgeocode
import requests
import time

def population_zip_lat_log(df):
    '''
    This function is used to get the population data with zip code and convert zip to lat_log
    
    Args:
        df: original cvs file, population and zip
    Returns:
        new df with population, zip, lat_log 
    '''
    nomi = pgeocode.Nominatim('us')

    latitude_list=[]
    longitude_list=[]
    # convert zip to lat_log
    for i in range(len(df)):
        zipcode=str(df.loc[i,'zip_code'])
        zipcode_info=nomi.query_postal_code(zipcode)
        latitude_list.append(zipcode_info[9])
        longitude_list.append(zipcode_info[10])

    df['latitude'] = latitude_list
    df['longitude'] = longitude_list
    
    # save converted data to csv file
    df.to_csv("population_zipcode_lat_lon2.csv", sep='\t', encoding='utf-8')
    return df


def air_quality(url):
    '''
    This function is used to get the air quality data
    Args:
        url: api url
    Returns:
        air quality dataframe
    '''

    df_air = pd.DataFrame()
    # divided into 9 runs, each loop 200 data, total 1761 data
    loop_list=[range(0,200),range(200,400),range(400,600), range(600,800),range(800,1000),
              range(1000,1200),range(1200,1400),range(1400,1600),range(1600,1761)]

    for loop in loop_list:
        for i in loop:

            querystring = {"lat":df.loc[i,'latitude'],"lon":df.loc[i,'longitude']}

            headers = {
                "X-RapidAPI-Key": "c048900bfdmsh50e74fe167c3d99p15472fjsn87990fe32453",
                "X-RapidAPI-Host": "air-quality-by-api-ninjas.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            df_air.loc[i,'CO']=response.json()["CO"]["concentration"]
            df_air.loc[i,'NO2']=response.json()["NO2"]["concentration"]
            df_air.loc[i,'O3']=response.json()["O3"]["concentration"]
            df_air.loc[i,'SO2']=response.json()["SO2"]["concentration"]
            df_air.loc[i,'PM2.5']=response.json()["PM2.5"]["concentration"]
            df_air.loc[i,'PM10']=response.json()["PM10"]["concentration"]
            df_air.loc[i,'aqi']=response.json()["overall_aqi"]

        time.sleep(15) # Sleep for 15 seconds

    df_air.to_csv("air_quality2.csv", sep='\t', encoding='utf-8')  
    return df_air



def climate(url):
    '''
    This function is used to get the climate data
    Args:
        url: api url
    Returns:
        climate dataframe
    '''
    
    df_climate=pd.DataFrame()

    for i in range(1761):

        querystring = {"q":df.loc[i,'zip_code']}

        headers = {
            "X-RapidAPI-Key": "c048900bfdmsh50e74fe167c3d99p15472fjsn87990fe32453",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        df_climate.loc[i,'wind_degree']=response.json()["current"]["wind_degree"]
        df_climate.loc[i,'humidity']=response.json()["current"]["humidity"]
        df_climate.loc[i,'temp_c']=response.json()["current"]["temp_c"]
        df_climate.to_csv("climate2.csv", sep='\t', encoding='utf-8')
        
    return df_climate



if __name__ == '__main__':
    # get dataset 1 (population data), convert zip to lat and log geolocation
    df = pd.read_csv ('pop-by-zip-code.csv')
    #print(population_zip_lat_log(df))
    
    #get dataset 2 (air quality data) using API
    url_air = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"
    #print(air_quality(url_air))
    
    #get dataset 3 (climate data) using API
    url_climate = "https://weatherapi-com.p.rapidapi.com/current.json"
    print(climate(url_climate))
    
    




