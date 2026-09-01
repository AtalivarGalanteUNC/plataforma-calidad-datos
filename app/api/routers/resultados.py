from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import ResultadoLeer
from app.infrastructure.repositorio_resultados import listar_resultados

router = APIRouter(prefix="/api/resultados", tags=["resultados"])


@router.get("", response_model=list[ResultadoLeer])
def get_resultados(
    db: Session = Depends(get_db),
    check_id: int | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    return listar_resultados(db, check_id=check_id, limit=limit, offset=offset)