#!/bin/bash

echo "Waiting for database..."
sleep 10

echo "Running migrations..."
alembic upgrade head

echo "Starting Gunicorn..."
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000