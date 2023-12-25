FROM python:3.8

WORKDIR /app

COPY livedata.py utils.py influx.config.ini requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python3", "livedata.py"]
