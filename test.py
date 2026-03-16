import requests
import json

url = "https://archive-api.open-meteo.com/v1/archive"
floodUrl = "https://flood-api.open-meteo.com/v1/flood"

tests = [
    {
        "name": "2025 Milwaukee Area Floods",
        "latitude": 43.0389,
        "longitude": -87.9065,
        "start_date": "2025-05-01",
        "end_date": "2025-05-01"
    },
    {
        "name": "2025 Pacific Northwest Floods",
        "latitude": 47.6062,
        "longitude": -122.3321,
        "start_date": "2025-01-01",
        "end_date": "2025-01-01"
    },
    {
        "name": "July 2025 Central Texas Floods",
        "latitude": 30.2672,
        "longitude": -97.7431,
        "start_date": "2025-07-01",
        "end_date": "2025-07-01"
    }
]

for test in tests:
    print(f"\n--- {test['name']} ---\n")
    
    params = {
        "latitude": test["latitude"],
        "longitude": test["longitude"],
        "start_date": test["start_date"],
        "end_date": test["end_date"],
        "hourly": "precipitation,surface_pressure",
        "daily": "river_discharge"
    }

    response = requests.get(url, params)
    floodResponse = requests.get(floodUrl, params)

    data = response.json()
    floodData = floodResponse.json()

    rain = data["hourly"]["precipitation"]
    pressure = data["hourly"]["surface_pressure"]
    time = data["hourly"]["time"]
    river_list = floodData.get("daily").get("river_discharge")
    river = river_list[0] 

    if river is None:
        print("No river data available\n")
    else:
        print(f"River discharge: {river} m³/s\n")

    if rain and pressure:
        max_r = max(rain)
        min_p = min(pressure)
        if max_r > 2 and min_p < 1000 and river and river > 50:
            print("!!! EXTREME FLOOD RISK WARNING FOR THE DAY !!!\n")
        elif max_r > 1 and min_p < 1010 and river and river > 20:
            print("!!! HIGH FLOOD RISK WARNING FOR THE DAY !!!\n")
        elif max_r > 0 and min_p < 1020 and river and river > 5:
            print("Moderate flood risk warning for the day\n")
        elif max_r > 0.5 and min_p < 1015:
            print("Heavy rain and low pressure warning for the day — watch conditions\n")

    for i in range(len(time)):
        r = rain[i]
        p = pressure[i] 

        print(f"{time[i]} - Rain: {r:.1f} mm | Pressure: {p:.1f} hPa")

    if river is not None:
        print(f"\n*** Total daily river discharge: {river} m³/s ***\n")