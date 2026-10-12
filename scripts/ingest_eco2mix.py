import json
import os
from datetime import date, timedelta
from s3_utils import get_s3_client, ensure_bucket, BUCKET

import boto3
import requests
from botocore.exceptions import ClientError

import argparse
import time

DATASET = "eco2mix-national-tr"
URL = f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{DATASET}/records"



def fetch_city_day(jour):
    params = {
        "where": f"date_heure >= date'{jour}' AND date_heure < date'{jour + timedelta(days=1)}'",
        "order_by": "date_heure",
        "limit": 100,
    }
    reponse = requests.get(URL, params=params, timeout=30)
    reponse.raise_for_status()
    donnees = reponse.json()

    # Garde-fou : on refuse une reponse tronquee plutot que de la stocker en silence
    if len(donnees["results"]) != donnees["total_count"]:
        raise ValueError(
            f"Reponse incomplete : {len(donnees['results'])} lignes recues sur {donnees['total_count']}"
        )
    return donnees


def upload_raw(s3, jour, donnees):
    key = f"eco2mix/date={jour}/eco2mix_{jour}.json"
    corps = json.dumps(donnees, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=BUCKET, Key=key, Body=corps)
    return key


# if __name__ == "__main__":
#     jour = date.today() - timedelta(days=1)
#     s3 = get_s3_client()
#     ensure_bucket(s3)
#     donnees = fetch_day(jour)
#     key = upload_raw(s3, jour, donnees)
#     print(f"{len(donnees['results'])} lignes -> s3://{BUCKET}/{key}")




def parse_args():
    parser = argparse.ArgumentParser(description="Ingestion eCO2mix vers S3")
    parser.add_argument("--start", type=date.fromisoformat, help="Premier jour (AAAA-MM-JJ)")
    parser.add_argument("--end", type=date.fromisoformat, help="Dernier jour inclus (AAAA-MM-JJ)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    hier = date.today() - timedelta(days=1)
    debut = args.start or hier
    fin = args.end or debut

    if fin < debut:
        raise SystemExit("--end doit etre posterieur ou egal a --start")

    s3 = get_s3_client()
    ensure_bucket(s3)

    jour = debut
    while jour <= fin:
        donnees = fetch_day(jour)
        key = upload_raw(s3, jour, donnees)
        print(f"{len(donnees['results'])} lignes -> s3://{BUCKET}/{key}")
        jour += timedelta(days=1)
        time.sleep(1)