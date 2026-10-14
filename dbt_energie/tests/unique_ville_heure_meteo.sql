select ville, date_heure_utc, count(*)
from {{ ref('stg_meteo') }}
group by ville, date_heure_utc
having count(*) > 1