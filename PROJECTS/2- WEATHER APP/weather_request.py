import requests
from keys import *
from twilio.rest import Client

client = Client(account_sid, auth_token)

weather_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{LOCATION_KEY}?apikey={ACCU_KEY}"
req_data = requests.get(weather_url)
print("Status Code:", req_data.status_code)
resp_data = req_data.json()

headline = resp_data["Headline"]["Text"]
link = resp_data["Headline"]["Link"]
daily_forecast = []
for day in resp_data["DailyForecasts"]:
    date = " DATE: "+day["Date"][0:10]+""+"\n"
    temp = f'Temperature: \nMin: {day["Temperature"]["Minimum"]["Value"]} F \nMax: {day["Temperature"]["Maximum"]["Value"]} F\n'
    weather = f'Weather:{(day["Day"]["IconPhrase"]).strip()} in the day  and {(day["Night"]["IconPhrase"]).strip()} in the night\n\n'
    daily_weather = "".join([date,temp,weather])
    daily_forecast.append(daily_weather)
    

message_body = f"\n\nThis weeks weather Forecast:\n{headline}\n{' '.join(daily_forecast)}\nLink:{link}"

message = client.messages.create(
    messaging_service_sid=f'{MESSAGE__ID}',
    body=message_body,
  to=f'{PHONE_NUMBER}'
)