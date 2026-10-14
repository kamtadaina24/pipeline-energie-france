""" import json
from s3_utils import get_s3_client, BUCKET

s3 = get_s3_client()
for c in sorted(k["Key"] for k in s3.list_objects_v2(Bucket=BUCKET, Prefix="eco2mix/")["Contents"]):
    d = json.loads(s3.get_object(Bucket=BUCKET, Key=c)["Body"].read())
    print(c[-15:-5], len(d["results"])) """
    
    
import json

from s3_utils import BUCKET, get_s3_client

s3 = get_s3_client()
cles = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="eco2mix/")["Contents"])

for c in cles:
    lignes = json.loads(s3.get_object(Bucket=BUCKET, Key=c)["Body"].read())["results"]
    vides = sum(1 for l in lignes if l["consommation"] is None)
    print(c[-15:-5], len(lignes), "lignes,", vides, "consommation vide")