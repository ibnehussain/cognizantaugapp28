from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__, static_folder="static")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 5

# WMO weather interpretation codes -> human-readable description
WMO_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def describe_weather_code(code):
    return WMO_DESCRIPTIONS.get(code, "Unknown")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/weather")
def get_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "city parameter required"}), 400

    try:
        geo_resp = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1},
            timeout=REQUEST_TIMEOUT,
        )
        geo_resp.raise_for_status()
    except requests.RequestException:
        return jsonify({"error": "weather service unavailable"}), 502

    geo_data = geo_resp.json()
    results = geo_data.get("results")
    if not results:
        return jsonify({"error": "city not found"}), 404

    location = results[0]
    lat = location["latitude"]
    lon = location["longitude"]

    try:
        forecast_resp = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "daily": "weathercode,temperature_2m_max,temperature_2m_min",
                "temperature_unit": "celsius",
                "timezone": "auto",
            },
            timeout=REQUEST_TIMEOUT,
        )
        forecast_resp.raise_for_status()
    except requests.RequestException:
        return jsonify({"error": "weather service unavailable"}), 502

    forecast_data = forecast_resp.json()
    current_weather = forecast_data.get("current_weather", {})
    daily = forecast_data.get("daily", {})

    daily_entries = []
    dates = daily.get("time", [])
    codes = daily.get("weathercode", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    for i in range(min(5, len(dates))):
        daily_entries.append({
            "date": dates[i],
            "tempMax": temp_max[i],
            "tempMin": temp_min[i],
            "weathercode": codes[i],
            "description": describe_weather_code(codes[i]),
        })

    response = {
        "city": location.get("name", city),
        "country": location.get("country", ""),
        "current": {
            "temp": current_weather.get("temperature"),
            "windspeed": current_weather.get("windspeed"),
            "weathercode": current_weather.get("weathercode"),
            "description": describe_weather_code(current_weather.get("weathercode")),
            "time": current_weather.get("time"),
        },
        "daily": daily_entries,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
