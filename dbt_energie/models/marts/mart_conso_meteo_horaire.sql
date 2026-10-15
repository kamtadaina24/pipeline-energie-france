{{ config(materialized='table') }}

with eco as (
    select
        date_trunc('hour', date_heure_utc)  as heure_utc,
        avg(consommation_mw)                as consommation_moy_mw,
        avg(nucleaire_mw)                   as nucleaire_moy_mw,
        avg(eolien_mw)                      as eolien_moy_mw,
        avg(solaire_mw)                     as solaire_moy_mw,
        count(*)                            as nb_quarts
    from {{ ref('stg_eco2mix') }}
    group by 1
),

meteo as (
    select
        date_heure_utc                      as heure_utc,
        avg(temperature_c)                  as temperature_moy_c,
        avg(vent_kmh)                       as vent_moy_kmh,
        avg(rayonnement_wm2)                as rayonnement_moy_wm2,
        count(*)                            as nb_villes
    from {{ ref('stg_meteo') }}
    group by 1
)

select
    eco.*,
    meteo.temperature_moy_c,
    meteo.vent_moy_kmh,
    meteo.rayonnement_moy_wm2,
    meteo.nb_villes
from eco
left join meteo using (heure_utc)