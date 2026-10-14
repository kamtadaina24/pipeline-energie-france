import json

from s3_utils import BUCKET, get_s3_client

s3 = get_s3_client()
key = "eco2mix/date=2026-10-10/eco2mix_2026-10-10.json"
lignes = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())["results"]

for l in lignes:
    if l["consommation"] is None:
        print(l["date_heure"], l["date"], l["heure"])