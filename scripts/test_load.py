from s3_utils import get_s3_client
from load_raw import list_keys, read_json

s3 = get_s3_client()
cles = list(list_keys(s3, "eco2mix/"))
print(len(cles), cles[0])

d = read_json(s3, cles[0])
print(type(d), list(d.keys()))
print(len(d["results"]))

for c in cles:
    print(c)
    