from datetime import date, timedelta

import requests

from ingest_eco2mix import URL

jour = date.today()
params = {
    "where": f"date_heure >= date'{jour}' AND date_heure < date'{jour + timedelta(days=1)}'",
    "order_by": "date_heure",
    "limit": 100,
}
lignes = requests.get(URL, params=params, timeout=30).json()["results"]

print(len(lignes), "lignes")
print("premiere :", lignes[0]["date_heure"])
print("derniere :", lignes[-1]["date_heure"])
print("consommation vide :", sum(1 for l in lignes if l["consommation"] is None))
print("premiere :", lignes[0]["date"], lignes[0]["heure"])
print("derniere :", lignes[-1]["date"], lignes[-1]["heure"])