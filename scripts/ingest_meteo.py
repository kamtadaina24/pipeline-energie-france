import argparse
import json
import time
from datetime import date, timedelta

import requests

from s3_utils import BUCKET, ensure_bucket, get_s3_client

URL = "https://archive-api.open-meteo.com/v1/archive"
VARIABLES = "temperature_2m,wind_speed_10m,shortwave_radiation"

VILLES = {
    "paris": (48.85, 2.35),
    "lyon": (45.76, 4.84),
    "marseille": (43.30, 5.37),
    "lille": (50.63, 3.06),
    "toulouse": (43.60, 1.44),
    "bordeaux": (44.84, -0.58),
}


def fetch_city_day(ville, latitude, longitude, jour):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": jour.isoformat(),
        "end_date": jour.isoformat(),
        "hourly": VARIABLES,
        "timezone": "UTC",
    }
    reponse = requests.get(URL, params=params, timeout=30)
    reponse.raise_for_status()
    donnees = reponse.json()

    # Garde-fou : une journee UTC doit avoir exactement 24 heures
    nb_heures = len(donnees["hourly"]["time"])
    if nb_heures != 24:
        raise ValueError(f"{ville} {jour} : {nb_heures} heures recues au lieu de 24")
    return donnees


def upload_raw(s3, ville, jour, donnees):
    key = f"meteo/date={jour}/ville={ville}/meteo_{ville}_{jour}.json"
    corps = json.dumps(donnees, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=BUCKET, Key=key, Body=corps)
    return key


def parse_args():
    parser = argparse.ArgumentParser(description="Ingestion meteo vers S3")
    parser.add_argument("--start", type=date.fromisoformat, required=True)
    parser.add_argument("--end", type=date.fromisoformat)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    debut = args.start
    fin = args.end or debut
    if fin < debut:
        raise SystemExit("--end doit etre posterieur ou egal a --start")

    s3 = get_s3_client()
    ensure_bucket(s3)

    jour = debut
    while jour <= fin:
        for ville, (lat, lon) in VILLES.items():
            donnees = fetch_city_day(ville, lat, lon, jour)
            key = upload_raw(s3, ville, jour, donnees)
            print(f"s3://{BUCKET}/{key}")
            time.sleep(1)
        jour += timedelta(days=1)