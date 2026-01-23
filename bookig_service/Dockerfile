FROM python:3.12

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r requirements.txt \
    && rm -rf /root/.cacge/pip

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
