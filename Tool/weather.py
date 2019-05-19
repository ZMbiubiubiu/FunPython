#! /home/bingo/anaconda3/bin/python
# *- coding=utf-8 -*

__author__ = "ZzLee"
__date__ = "2019/04/26"
__mail__ = "zhangmeng.lee@foxmail.com"
"""
    If you want to know how to use OpenWeatherMap API
    see "https://openweathermap.org/appid"
"""

import click
import requests


# my api
SAMPLE_API_KEY = 'edc05b55d6c563c64bc95406d8d514ef'

# Fahrenheit to Celsius
def fah2cel(temp):
    return (temp-32) / 1.8

# capture information about the city you want to show
def current_weather(location, api_key=SAMPLE_API_KEY):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    query_params = {
        'q': location,
        'appid': api_key,
    }
    response = requests.get(url, params=query_params).json()
    weather = response['weather'][0]['description']
    tmp = response['main']['temp']
    temperature = str(round(fah2cel(float(tmp)), 2))
    city_id = response['id']
    coordinate = response['coord']
    longitude = coordinate['lon']
    latitude = coordinate['lat']
    return weather,temperature,city_id,longitude,latitude

"""
# if you use API as options, below @click.argument, you can write ...
@click.option('--api-key', '-a', 
    help='your API key for the OpenWeatherMap API'
    )

Notice that you should pass the option arguments to the main function
for example def main(api-key, location)

In case of an option, it strips the leading dashes and turns them 
into snake case. --api-key becomes api_key.

""" 
@click.command()
@click.argument('location')
def main(location):
    """
    A little weather tool that shows you the current weather in a LOCATION of
    your choice. Provide the city name and optionally a two-digit country code.
    Here are two examples:

    1. Beijing

    2. Tianjin

    You need a valid API key from OpenWeatherMap for the tool to work. You can
    sign up for a free account at https://openweathermap.org/appid.

    """
    weather,temp,id,lon,lat = current_weather(location)
    print('=========================================================')
    print(f'The weather of {location} is : {weather}')
    print(f'The temperature is : {temp}')
    print(f'The {location}"s city id is : {id}')
    print(f'The coordinate is longitude: {lon}, latitude : {lat}')
    print('=========================================================')

if __name__ == "__main__":
    main()