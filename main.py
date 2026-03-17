import requests

url = "https://api.open-meteo.com/v1/forecast"
floodUrl = "https://flood-api.open-meteo.com/v1/flood"

params = {
    "latitude": 13.7563,
    "longitude": 100.5018,
    "hourly": "precipitation,surface_pressure",
    "daily": "river_discharge",
    "forecast_days": 1
}

response = requests.get(url, params=params)
floodResponse = requests.get(floodUrl, params=params)

data = response.json()
floodData = floodResponse.json()

rain = data["hourly"]["precipitation"]
pressure = data["hourly"]["surface_pressure"]
time = data["hourly"]["time"]
river_list = floodData.get("daily", {}).get("river_discharge", [])
river = river_list[0] if river_list else None

if rain and pressure:
    max_r = max(rain)
    min_p = min(pressure)
    if max_r > 10 and min_p < 990 and river and river > 50:
        print("!!! EXTREME FLOOD RISK WARNING FOR THE DAY !!!\n")
    elif max_r > 5 and min_p < 1000 and river and river > 30:
        print("!!! HIGH FLOOD RISK WARNING FOR THE DAY !!!\n")
    elif max_r > 2 and min_p < 1010 and river and river > 10:
        print("Moderate flood risk warning for the day\n")
    elif max_r > 10 and min_p < 1000:
        print("Heavy rain and low pressure warning for the day — watch conditions\n")

for i in range(len(time)):
    r = rain[i]
    p = pressure[i] 

    print(f"{time[i]} - Rain: {r:.1f} mm | Pressure: {p:.1f} hPa")

if river is not None:
    print(f"\n*** Forecasted daily river discharge: {river} m³/s ***\n")
