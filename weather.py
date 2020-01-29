# weather.py
import requests
import json
import os
import datetime
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('WEATHER_API')
base_url = "http://api.openweathermap.org/data/2.5/forecast?"

def getCurrWeather(loc:str):
    complete_url = base_url + "appid=" + api_key + "&q=" + loc
    response = requests.get(complete_url) 
    x = response.json() 
    if x["cod"] != "404": 
        t0 = x["list"][0]
        y = t0["main"] 
        current_temperature = int(y["temp"] -273)
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 
        z = t0["weather"]
        weather_description = z[0]["description"] 

        t1=x["list"][2]
        y1=t1["main"]
        temp1=int(y1["temp"]-273)
        pree1=y1["pressure"]
        hum1=y1["humidity"]
        z1=t1["weather"]
        weather1=z1[0]["description"]

        return ("At "+  (datetime.datetime.now().strftime('%H:%M:%S')) + ", Current Temperature (in C unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description)+
            "\n At " + (datetime.datetime.now() + datetime.timedelta(hours=6)).strftime('%H:%M:%S') + ", it is as follow: \n"+

            "Temperature (in C unit) = " +
                    str(temp1) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(pree1) +
          "\n humidity (in percentage) = " +
                    str(hum1) +
          "\n description = " +
                    str(weather1)+
            "\n"
            )
    else:
        return "error"

if __name__ == '__main__':
    print(getCurrWeather('ithaca'))