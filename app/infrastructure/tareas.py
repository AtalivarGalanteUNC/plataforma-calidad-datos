from app.application.ejecutar_checks_activos import ejecutar_checks_activos
from app.application.ingestar_dolar import ingestar_dolar
from app.infrastructure.celery_app import celery_app


@celery_app.task(
    name="tareas.ingestar_dolar",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def tarea_ingestar_dolar() -> str:
    guardadas = ingestar_dolar()
    return f"ingesta ok: {guardadas} cotizaciones nuevas"


@celery_app.task(name="tareas.ejecutar_checks_activos")
def tarea_ejecutar_checks_activos() -> str:
    resultados = ejecutar_checks_activos()
    detalle = ", ".join(f"check {cid}={estado}" for cid, estado in resultados)
    return f"checks ejecutados: {detalle}"