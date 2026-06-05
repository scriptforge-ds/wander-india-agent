import requests
from datetime import datetime

def get_weather(lat: float, lon: float, months: list[int]) -> dict:
    """
    Fetches historical climate normals for a location.
    Uses Open-Meteo's free climate API — no key needed.
    months: list of ints (1-12)
    """
    try:
        # Use climate normals endpoint (historical averages, not forecast)
        url = "https://climate-api.open-meteo.com/v1/climate"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "1990-01-01",
            "end_date": "2020-12-31",
            "monthly": "temperature_2m_mean,precipitation_sum,windspeed_10m_mean"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        monthly = data.get("monthly", {})
        times = monthly.get("time", [])
        temps = monthly.get("temperature_2m_mean", [])
        precip = monthly.get("precipitation_sum", [])

        # Aggregate by month number
        month_data = {m: {"temps": [], "precip": []} for m in range(1, 13)}
        for i, t in enumerate(times):
            m = int(t.split("-")[1])
            if temps[i] is not None:
                month_data[m]["temps"].append(temps[i])
            if precip[i] is not None:
                month_data[m]["precip"].append(precip[i])

        result = {}
        for m in months:
            t_list = month_data[m]["temps"]
            p_list = month_data[m]["precip"]
            result[m] = {
                "avg_temp_c": round(sum(t_list) / len(t_list), 1) if t_list else None,
                "avg_precip_mm": round(sum(p_list) / len(p_list), 1) if p_list else None,
                "condition": _classify_weather(
                    sum(t_list) / len(t_list) if t_list else None,
                    sum(p_list) / len(p_list) if p_list else None
                )
            }

        return {"status": "ok", "data": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def _classify_weather(temp: float, precip: float) -> str:
    if temp is None:
        return "Unknown"
    if precip and precip > 200:
        return "🌧️ Heavy Monsoon — avoid"
    if precip and precip > 80:
        return "🌦️ Rainy — not ideal"
    if temp < 2:
        return "🥶 Very Cold — snow likely"
    if temp < 10:
        return "🧥 Cold — pack warm layers"
    if temp < 20:
        return "😊 Pleasant"
    if temp < 30:
        return "☀️ Warm & comfortable"
    return "🥵 Hot — plan for heat"


# Coordinates for known destinations
DESTINATION_COORDS = {
    "kedarkantha":       {"lat": 31.02,  "lon": 78.25},
    "coorg":             {"lat": 12.33,  "lon": 75.80},
    "spiti":             {"lat": 32.24,  "lon": 78.07},
    "hampi":             {"lat": 15.33,  "lon": 76.46},
    "chopta":            {"lat": 30.52,  "lon": 79.22},
    "gokarna":           {"lat": 14.55,  "lon": 74.31},
    "ladakh":            {"lat": 34.17,  "lon": 77.58},
    "majuli":            {"lat": 26.95,  "lon": 94.17},
    "chikmagalur":       {"lat": 13.32,  "lon": 75.77},
    "valley_of_flowers": {"lat": 30.72,  "lon": 79.61},
}


def get_weather_for_destination(destination_key: str, months: list[int]) -> dict:
    coords = DESTINATION_COORDS.get(destination_key)
    if not coords:
        return {"status": "error", "message": f"No coordinates for {destination_key}"}
    return get_weather(coords["lat"], coords["lon"], months)