from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import CheckCrear, CheckLeer
from app.application.ejecutar_check import (
    CheckInactivo,
    CheckNoEncontrado,
    TipoDeCheckDesconocido,
    ejecutar_check,
)
from app.infrastructure.repositorio_checks import listar_checks, obtener_check_por_id
from app.infrastructure.models import Check, Dataset

router = APIRouter(prefix="/api/checks", tags=["checks"])


@router.get("", response_model=list[CheckLeer])
def get_checks(db: Session = Depends(get_db)):
    return listar_checks(db)


@router.get("/{check_id}", response_model=CheckLeer)
def get_check(check_id: int, db: Session = Depends(get_db)):
    check = obtener_check_por_id(db, check_id)
    if check is None:
        raise HTTPException(status_code=404, detail=f"no existe el check {check_id}")
    return check


@router.post("", response_model=CheckLeer, status_code=201)
def crear_check(datos: CheckCrear, db: Session = Depends(get_db)):
    dataset = db.get(Dataset, datos.dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail=f"no existe el dataset {datos.dataset_id}")

    check = Check(
        dataset_id=datos.dataset_id,
        tipo=datos.tipo,
        nombre=datos.nombre,
        activo=True,
        configuracion=datos.configuracion,
    )
    db.add(check)
    db.commit()
    db.refresh(check)
    return check


@router.post("/{check_id}/ejecutar")
def ejecutar_check_endpoint(check_id: int):
    try:
        resultado = ejecutar_check(check_id)
    except CheckNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CheckInactivo as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TipoDeCheckDesconocido as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"check_id": check_id, "estado": resultado.estado, "valor_medido": resultado.valor_medido, "mensaje": resultado.mensaje}