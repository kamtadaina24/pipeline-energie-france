select
    (r->>'date_heure')::timestamptz   as date_heure_utc,
    r->>'nature'                      as nature,
    (r->>'consommation')::int         as consommation_mw,
    (r->>'nucleaire')::int            as nucleaire_mw,
    (r->>'eolien')::int               as eolien_mw,
    (r->>'solaire')::int              as solaire_mw,
    (r->>'hydraulique')::int          as hydraulique_mw,
    (r->>'gaz')::int                  as gaz_mw,
    (r->>'charbon')::int              as charbon_mw,
    (r->>'fioul')::int                as fioul_mw,
    (r->>'bioenergies')::int          as bioenergies_mw,
    (r->>'taux_co2')::int             as taux_co2_g_kwh
from {{ source('raw', 'eco2mix_jour') }},
     jsonb_array_elements(payload->'results') as r