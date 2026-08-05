-- Crea la base "origen": el mundo externo que la plataforma vigila.
-- (Dos mundos: esta base es "de otro", la plataforma se conecta desde afuera.)
CREATE DATABASE origen;

-- Nos conectamos a "origen" para crear la tabla dolar adentro de ELLA,
-- no en calidad_datos. El \c es un comando de psql que cambia de base.
\c origen

CREATE TABLE dolar (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    casa                TEXT        NOT NULL,
    moneda              TEXT        NOT NULL,
    compra              NUMERIC(12, 2),
    venta               NUMERIC(12, 2),
    fecha_actualizacion TIMESTAMPTZ NOT NULL,
    ingestado_en        TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT dolar_casa_fecha_unica UNIQUE (casa, fecha_actualizacion)
);