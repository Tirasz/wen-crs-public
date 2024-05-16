# run if SECURITY_ENABLED:
# docker cp wen-crs-es01-1:/usr/share/elasticsearch/config/certs/ca/ca.crt ./cert/.
# python -m flask --app elastic_client run
from flask_app import create_app
from client import create_client

client = create_client()
app = create_app(client)