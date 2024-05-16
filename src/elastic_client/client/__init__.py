from elasticsearch import Elasticsearch
from configs import ELASTIC_USERNAME, ELASTIC_PASSWORD, ELASTIC_CERTS_PATH, ELASTIC_SERVER, INDEX_NAME, PIPELINE_ID, PREFIXED_INDEX
from .utils import load_mapping, load_pipeline


def create_client():

  client = Elasticsearch(
    ELASTIC_SERVER,
    ca_certs=ELASTIC_CERTS_PATH+'/ca/ca.crt',
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
  )

  if not client.indices.exists(index=PREFIXED_INDEX):
    print(f"# Creating index: {PREFIXED_INDEX}")
    index_settings = load_mapping(INDEX_NAME)
    ingest_pipeline = load_pipeline(INDEX_NAME)
    client.ingest.put_pipeline(id=PIPELINE_ID, body=ingest_pipeline)
    client.indices.create(index=PREFIXED_INDEX, body=index_settings)

  return client