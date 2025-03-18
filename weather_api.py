from aisetup import print_llm_response, get_llm_response,authenticate
from dotenv import load_dotenv
import os
import requests
load_dotenv('.env',override=True)
api_key=os.getenv("WEATHER_API_KEY")
authenticate()
lat=37.441
lon=-122.1430

url=f"https://api.openweathermap.org/data/2.5/forecast?units=metric&cnt=1&lat={lat}&lon={lon}&appid={api_key}"

response = requests.get(url)

data = response.json()

print(data)
temperature = data['list'][0]['main']['temp']
description = data['list'][0]['weather'][0]['description']
wind_speed = data['list'][0]['wind']['speed']

weather_string = f"""The temperature is {temperature}°C. 
It is currently {description},
with a wind speed of {wind_speed}m/s.
"""

prompt = f"""Based on the following weather forecast, suggest the right clothing.
    Weather forecast: {weather_string}
"""

result=get_llm_response(prompt)
print(result)