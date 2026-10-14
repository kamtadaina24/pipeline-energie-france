import json
import os
import re

import psycopg2
from psycopg2.extras import Json

from s3_utils import BUCKET, get_s3_client

UPSERT_ECO2MIX = """
    INSERT INTO raw.eco2mix_jour (jour, payload, s3_key)
    VALUES (%s, %s, %s)
    ON CONFLICT (jour) DO UPDATE
    SET payload = EXCLUDED.payload, s3_key = EXCLUDED.s3_key, loaded_at = now();
"""

UPSERT_METEO = """
    INSERT INTO raw.meteo_jour_ville (jour, ville, payload, s3_key)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (jour, ville) DO UPDATE
    SET payload = EXCLUDED.payload, s3_key = EXCLUDED.s3_key, loaded_at = now();
"""


def get_pg_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", "5433")),
        dbname=os.getenv("PG_DB", "energie"),
        user=os.getenv("PG_USER", "energie"),
        password=os.getenv("PG_PASSWORD", "energie123"),
    )


def list_keys(s3, prefix):
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            yield obj["Key"]


def read_json(s3, key):
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(obj["Body"].read())


def load_eco2mix(s3, cur):
    n = 0
    for key in list_keys(s3, "eco2mix/"):
        jour = re.search(r"date=(\d{4}-\d{2}-\d{2})", key).group(1)
        cur.execute(UPSERT_ECO2MIX, (jour, Json(read_json(s3, key)), key))
        n += 1
    return n


def load_meteo(s3, cur):
    n = 0
    for key in list_keys(s3, "meteo/"):
        jour = re.search(r"date=(\d{4}-\d{2}-\d{2})", key).group(1)
        ville = re.search(r"ville=([a-z]+)", key).group(1)
        cur.execute(UPSERT_METEO, (jour, ville, Json(read_json(s3, key)), key))
        n += 1
    return n


if __name__ == "__main__":
    s3 = get_s3_client()
    conn = get_pg_connection()
    try:
        with conn:                      # valide tout (commit) ou annule tout (rollback)
            with conn.cursor() as cur:
                n1 = load_eco2mix(s3, cur)
                n2 = load_meteo(s3, cur)
        print(f"eco2mix : {n1} fichiers charges | meteo : {n2} fichiers charges")
    finally:
        conn.close()