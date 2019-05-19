#! /home/bingo/anaconda3/bin/python
# *- coding=utf-8 -*

__author__ = "ZzLee"
__date__ = "2019/04/28"
__mail__ = "zhangmeng.lee@foxmail.com"
"""
    # 新增功能
        子命令 config - 确认并打印api-key
        子命令 current - 获得某地的天气信息
        将环境变量作为默认值
        api-key值验证
    # 运行逻辑
        >>> current --> if 'api-key file' exists then run --> get result
                |                                         |
                |                                         |
                |                                          --> unauthorized |
                |                                                           |
                |                                                           |
            file not exists -- run 'config' command to get 'api-key'  <------
                                                |
                                                |
                            by environment  <---  ---> by user input
"""

import os
import re
import click
import requests

# the default file for saving the API-KEY
API_FILE = os.path.expanduser('~/.weather.cfg')

# validate the api-key
class ApiKey(click.ParamType):
    name = 'api-key'
    def convert(self, value, params, ctx): #api-key, Click.option or Click.argument, context of the command
        found = re.match('[0-91-f]',value)
        if not found:
            self.fail(
                f'{value} is not a 32-bit hexadecimal string',
                params,
                ctx,
            )
        return value

# Fahrenheit to Celsius
def fah2cel(temp):
    return (temp-32) / 1.8

# capture information about the city you want to show
def current_weather(location, api_key):
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

@click.group()
def main():
    pass

@main.command()
@click.option(
    '--api-key',
    '-a',
    type=ApiKey(),
    envvar="API_KEY", # if Env has the api_key, then get it.If not, ask for user.
    help="Your API KEY for OpenWeatherMap"
)
def config(api_key):
    if not api_key:
        api_key = input("You should input a api-key : ")
    with open(API_FILE, 'w') as f:
        print(api_key)
        f.write(api_key)

@main.command()
@click.argument('location')
#@click.option('--api-key', '-a', envvar="API_KEY") #use Environment variable 'API_KEY' as api_key 's default value
def current(location):
    """
    A little weather tool that shows you the current weather in a LOCATION of
    your choice. Provide the city name and optionally a two-digit country code.
    Here are two examples:

    1. Beijing

    2. Tianjin

    You need a valid API key from OpenWeatherMap for the tool to work. You can
    sign up for a free account at https://openweathermap.org/appid.

    """
    # get the api-key from the config file
    try:
        f = open(API_FILE, 'r')
        api_key = f.read()
    except FileNotFoundError as e:
        print("No config file found!\nPlease set a new key Use 'config' command.")
        return 1
    try:
        weather,temp,id,lon,lat = current_weather(location, api_key=api_key)
        print('=========================================================')
        print(f'The weather of {location} is : {weather}')
        print(f'The temperature is : {temp}')
        print(f'The {location}"s city id is : {id}')
        print(f'The coordinate is longitude: {lon}, latitude : {lat}')
        print('=========================================================')
    except:
        raise ValueError("Invalid API_KEY.\n Please set a new key Use 'config' command.")

if __name__ == "__main__":
    main()
# test
# python weather_strength.py current Beijing
# python weather_strength.py config