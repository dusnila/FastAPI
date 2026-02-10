from celery import Celery
from app.config import setting

celery = Celery(
    "tasks",
    broker= setting.RABBITMQ_URL,
    include=["app.tasks.tasks"]
)
