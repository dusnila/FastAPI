from celery import Celery
from app.config import setting

celery = Celery(
    "tasks",
    broker=f"amqp://guest:guest@localhost:5672//",
    include=["app.tasks.tasks"]
)

