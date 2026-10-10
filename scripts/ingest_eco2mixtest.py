from datetime import date, timedelta

import requests

DATASET = "eco2mix-national-tr"   # remplace par l'identifiant de ton onglet API si différent
URL = f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{DATASET}/records"

jour = date.today() - timedelta(days=1)   # hier : une journée complète

params = {
    "where": f"date_heure >= date'{jour}' AND date_heure < date'{jour + timedelta(days=1)}'",
    "order_by": "date_heure",
    "limit": 100,
}

reponse = requests.get(URL, params=params, timeout=30)
reponse.raise_for_status()   # lève une erreur si le serveur répond 4xx/5xx
donnees = reponse.json()

print(donnees["total_count"], "lignes pour le", jour)
print(donnees["results"][0])