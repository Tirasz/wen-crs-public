import json
import os
from pathlib import Path

configs_path = Path(__file__).parent

with open(configs_path / 'config.json', "r", encoding="utf-8") as f:
  config = json.load(f)

EMBEDDING_MODEL = config['EMBEDDING_MODEL']
SPACY_MODELS = config['SPACY_MODELS']
SUPPORTED_LANGUAGES = SPACY_MODELS.keys()

ELASTIC_CLIENT = os.getenv('ELASTIC_CLIENT')
DUMMY_CLIENT = os.getenv('DUMMY_CLIENT')
PROCESS_LIMIT = int(os.getenv('PROCESS_LIMIT', 3000))