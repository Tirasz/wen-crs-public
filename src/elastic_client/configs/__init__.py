import json
import os
from pathlib import Path

configs_path = Path(__file__).parent

with open(configs_path / 'config.json', "r", encoding="utf-8") as f:
  config = json.load(f)

EMBEDDING_DIM = int(config['EMBEDDING_DIM'])
INDEX_NAME = config['INDEX_NAME']
PIPELINE_ID = config['PIPELINE_ID']

INDEX_PREFIX = os.getenv('INDEX_PREFIX')
ELASTIC_USERNAME = os.getenv('ELASTIC_USERNAME')
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD') 
ELASTIC_CERTS_PATH = os.getenv('ELASTIC_CERTS_PATH')
ELASTIC_SERVER = os.getenv('ELASTIC_SERVER')

PREFIXED_INDEX = INDEX_PREFIX + '-' + INDEX_NAME