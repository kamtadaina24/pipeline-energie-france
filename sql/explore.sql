-- 1. Combien de quarts d'heure par jour ?
SELECT jour, jsonb_array_length(payload->'results') AS nb_lignes
FROM raw.eco2mix_jour
ORDER BY jour;

-- 2. Une ligne par quart d'heure
SELECT
    r->>'date_heure'               AS date_heure,
    (r->>'consommation')::int      AS consommation,
    (r->>'nucleaire')::int         AS nucleaire
FROM raw.eco2mix_jour,
     jsonb_array_elements(payload->'results') AS r
WHERE jour = '2026-10-10'
ORDER BY date_heure
LIMIT 5;