import os

import psycopg
from fastapi import FastAPI

from app.api.routers import checks, fuentes, resultados

app = FastAPI(title="Plataforma de Calidad de Datos")

app.include_router(checks.router)
app.include_router(resultados.router)
app.include_router(fuentes.router)


@app.get("/")
def raiz():
    return {"mensaje": "La plataforma está viva"}


@app.get("/health")
def health():
    try:
        with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"status": "ok", "base_de_datos": "conectada"}
    except Exception as e:
        return {"status": "error", "base_de_datos": str(e)}