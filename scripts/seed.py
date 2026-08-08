from sqlalchemy import select

from app.infrastructure.db import SessionLocal
from app.infrastructure.models import Check, Dataset, Fuente


def seed() -> None:
    with SessionLocal() as session:
        ya_existe = session.scalar(select(Fuente).where(Fuente.nombre == "origen"))
        if ya_existe is not None:
            print("El seed ya se corrió antes. No hago nada.")
            return

        fuente = Fuente(
            nombre="origen",
            tipo="postgres",
            referencia_conexion="ORIGEN_DATABASE_URL",
        )
        session.add(fuente)
        session.flush()

        dataset = Dataset(
            fuente_id=fuente.id,
            nombre="dolar",
            esquema="public",
            tabla="dolar",
        )
        session.add(dataset)
        session.flush()

        check = Check(
            dataset_id=dataset.id,
            tipo="frescura",
            nombre="frescura de dolar (24h)",
            activo=True,
            configuracion={
                "columna": "fecha_actualizacion",
                "umbral_horas": 24,
            },
        )
        session.add(check)

        session.commit()

        print(f"Seed listo. fuente_id={fuente.id}, dataset_id={dataset.id}, check_id={check.id}")


if __name__ == "__main__":
    seed()