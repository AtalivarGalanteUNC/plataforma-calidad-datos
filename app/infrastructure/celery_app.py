import os
from datetime import timedelta

from celery import Celery
from celery.signals import worker_process_init

from app.infrastructure.db import engine


celery_app = Celery(
    "plataforma_calidad_datos",
    broker=os.environ["REDIS_URL"],
    include=["app.infrastructure.tareas"],
)

celery_app.conf.update(
    timezone="America/Argentina/Buenos_Aires",
    task_serializer="json",
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
    beat_schedule={
        # en producción: cada 6 horas
        "ingesta-dolar-cada-2-min": {
            "task": "tareas.ingestar_dolar",
            "schedule": timedelta(minutes=2),
        },
        # en producción: cada 6 horas, desfasada de la ingesta
        "checks-cada-5-min": {
            "task": "tareas.ejecutar_checks_activos",
            "schedule": timedelta(minutes=5),
        },
    },
)


@worker_process_init.connect
def _reiniciar_engine(**kwargs) -> None:
    engine.dispose(close=False)