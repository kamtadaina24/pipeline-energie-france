select
    m.ville,
    (t.valeur::timestamp at time zone 'UTC')                                  as date_heure_utc,
    (m.payload->'hourly'->'temperature_2m'->>((t.pos - 1)::int))::float       as temperature_c,
    (m.payload->'hourly'->'wind_speed_10m'->>((t.pos - 1)::int))::float       as vent_kmh,
    (m.payload->'hourly'->'shortwave_radiation'->>((t.pos - 1)::int))::float  as rayonnement_wm2
from {{ source('raw', 'meteo_jour_ville') }} as m,
     jsonb_array_elements_text(m.payload->'hourly'->'time') with ordinality as t(valeur, pos)