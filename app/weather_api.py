
import requests

def get_weather(city="Delhi", api_key="2aeb8da061305552ded31a65e21e8dec"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()

        return {
            "city": res.get("name", city),
            "temp": res.get("main", {}).get("temp", 25),
            "humidity": res.get("main", {}).get("humidity", 50),
            "rain": res.get("rain", {}).get("1h", 0.0),
            "desc": res.get("weather", [{}])[0].get("description", "N/A")
        }

    except Exception as e:
        print("Weather API Error:", e)
        return {
            "city": city,
            "temp": 25,
            "humidity": 50,
            "rain": 0.0,
            "desc": "Unavailable"
        }
