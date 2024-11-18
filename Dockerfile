FROM python:3.11

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# WORKDIR fast_app
# CMD gunicorn main:main_app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000