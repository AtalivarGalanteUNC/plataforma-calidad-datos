from fastapi import FastAPI

app = FastAPI(title="Plataforma de Calidad de Datos")


@app.get("/")
def raiz():
    return {"mensaje": "La plataforma está viva"}