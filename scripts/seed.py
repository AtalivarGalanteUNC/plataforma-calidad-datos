from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.db import SessionLocal
from app.infrastructure.models import Check, Dataset, Fuente


def _obtener_o_crear_fuente(session: Session) -> Fuente:
    fuente = session.scalar(select(Fuente).where(Fuente.nombre == "origen"))
    if fuente is not None:
        return fuente

    fuente = Fuente(
        nombre="origen",
        tipo="postgres",
        referencia_conexion="ORIGEN_DATABASE_URL",
    )
    session.add(fuente)
    session.flush()
    return fuente


def _obtener_o_crear_dataset(session: Session, fuente: Fuente) -> Dataset:
    dataset = session.scalar(
        select(Dataset).where(
            Dataset.fuente_id == fuente.id,
            Dataset.nombre == "dolar",
        )
    )
    if dataset is not None:
        return dataset

    dataset = Dataset(
        fuente_id=fuente.id,
        nombre="dolar",
        esquema="public",
        tabla="dolar",
    )
    session.add(dataset)
    session.flush()
    return dataset


def _obtener_o_crear_check(
    session: Session,
    dataset: Dataset,
    tipo: str,
    nombre: str,
    configuracion: dict,
) -> Check:
    check = session.scalar(
        select(Check).where(
            Check.dataset_id == dataset.id,
            Check.nombre == nombre,
        )
    )
    if check is not None:
        return check

    check = Check(
        dataset_id=dataset.id,
        tipo=tipo,
        nombre=nombre,
        activo=True,
        configuracion=configuracion,
    )
    session.add(check)
    session.flush()
    return check


def seed() -> None:
    with SessionLocal() as session:
        fuente = _obtener_o_crear_fuente(session)
        dataset = _obtener_o_crear_dataset(session, fuente)

        checks_a_sembrar = [
            (
                "frescura",
                "frescura de dolar (24h)",
                {"columna": "fecha_actualizacion", "umbral_horas": 24},
            ),
            (
                "nulls",
                "nulls de venta en dolar (0%)",
                {"columna": "venta", "umbral_pct": 0},
            ),
            (
                "volumen",
                "volumen de dolar (entre 5 y 10)",
                {"min_filas": 5, "max_filas": 10},
            ),
        ]

        creados = []
        for tipo, nombre, configuracion in checks_a_sembrar:
            check = _obtener_o_crear_check(session, dataset, tipo, nombre, configuracion)
            creados.append((check.id, tipo, nombre))

        session.commit()

        print(f"Seed listo. fuente_id={fuente.id}, dataset_id={dataset.id}")
        for check_id, tipo, nombre in creados:
            print(f"  check_id={check_id} tipo={tipo} nombre={nombre!r}")


if __name__ == "__main__":
    seed()