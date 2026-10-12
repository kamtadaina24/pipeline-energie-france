import requests

r = requests.get(
    "https://archive-api.open-meteo.com/v1/archive",
    params={
        "latitude": 48.85,
        "longitude": 2.35,
        "start_date": "2026-10-05",
        "end_date": "2026-10-07",
        "hourly": "temperature_2m,wind_speed_10m,shortwave_radiation",
        "timezone": "UTC",
    },
    timeout=30,
)
r.raise_for_status()
d = r.json()

print(d.keys())
print(f'd["hourly_units"]: {d["hourly_units"]}')
print({k: len(v) for k, v in d["hourly"].items()})
print({k: v.count(None) for k, v in d["hourly"].items()})
print(f'd["hourly"]["time"][:5]: {d["hourly"]["time"][:5]}')
print(f'd["latitude"]: {d["latitude"]}, d["longitude"]: {d["longitude"]}')