CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.eco2mix_jour (
    jour       date        PRIMARY KEY,
    payload    jsonb       NOT NULL,
    s3_key     text        NOT NULL,
    loaded_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.meteo_jour_ville (
    jour       date        NOT NULL,
    ville      text        NOT NULL,
    payload    jsonb       NOT NULL,
    s3_key     text        NOT NULL,
    loaded_at  timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (jour, ville)
);