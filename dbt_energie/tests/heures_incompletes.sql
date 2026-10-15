select heure_utc, nb_quarts
from {{ ref('mart_conso_meteo_horaire') }}
where nb_quarts <> 4