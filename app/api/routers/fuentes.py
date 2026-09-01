from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import DatasetLeer, FuenteLeer
from app.infrastructure.repositorio_fuentes import listar_datasets, listar_fuentes

router = APIRouter(prefix="/api", tags=["fuentes y datasets"])


@router.get("/fuentes", response_model=list[FuenteLeer])
def get_fuentes(db: Session = Depends(get_db)):
    return listar_fuentes(db)


@router.get("/datasets", response_model=list[DatasetLeer])
def get_datasets(db: Session = Depends(get_db)):
    return listar_datasets(db)