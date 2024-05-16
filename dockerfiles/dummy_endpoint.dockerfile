FROM python:3.10.13-bookworm

WORKDIR /src
COPY ../src/dummy_endpoint /src
RUN pip install -r ./requirements.txt

CMD ["gunicorn", "--conf", "configs/gunicorn_conf.py", "--bind", "0.0.0.0:80", "main:app"]
