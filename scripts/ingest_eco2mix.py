import json
import os
from datetime import date, timedelta

import boto3
import requests
from botocore.exceptions import ClientError

DATASET = "eco2mix-national-tr"
URL = f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{DATASET}/records"
BUCKET = "raw"


def get_s3_client():
    """Les valeurs par defaut visent le S3 local ; sur AWS on definit les variables."""
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT", "http://localhost:8333"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY", "minioadmin"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY", "minioadmin123"),
        region_name="us-east-1",
    )


def ensure_bucket(s3):
    try:
        s3.create_bucket(Bucket=BUCKET)
    except ClientError as e:
        if e.response["Error"]["Code"] not in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            raise


def fetch_day(jour):
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


if __name__ == "__main__":
    jour = date.today() - timedelta(days=1)
    s3 = get_s3_client()
    ensure_bucket(s3)
    donnees = fetch_day(jour)
    key = upload_raw(s3, jour, donnees)
    print(f"{len(donnees['results'])} lignes -> s3://{BUCKET}/{key}")