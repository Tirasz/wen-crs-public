FROM python:3.10.13-bookworm

WORKDIR /src
COPY ../src/elastic_client /src
COPY ../src/config.json /src/configs
RUN pip install -r ./requirements.txt

CMD ["gunicorn", "--conf", "configs/gunicorn_conf.py", "--bind", "0.0.0.0:80", "main:app"]


#  cd src
#  docker build -f .\elastic_client\Dockerfile -t elastic_client .