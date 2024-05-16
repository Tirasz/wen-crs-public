import json 
import spacy
from tqdm import tqdm
from typing import List
from collections import defaultdict
from langdetect import detect, LangDetectException
from sentence_transformers import SentenceTransformer
from configs import SUPPORTED_LANGUAGES, EMBEDDING_MODEL, SPACY_MODELS
from utils import unmark

def _get_lang(text: str):
  try: 
    language = detect(text)
    return language if language in SUPPORTED_LANGUAGES else None
  except LangDetectException:
    return None
  
def _process_obj(raw_obj):

  if not ('content' in raw_obj and raw_obj['content'] is not None):
    return None
  
  id = raw_obj["id"]
  text = unmark(raw_obj["content"])
  date = raw_obj["updateTimestamp"] if ("updateTimestamp" in raw_obj and raw_obj["updateTimestamp"] is not None) else raw_obj["timestamp"]
  channel_id = raw_obj["channelId"]
  channel_name = raw_obj["channelName"]
  embed = raw_obj["embed"] 
  author = raw_obj["author"]
  
  lang = _get_lang(text)
  if lang not in SUPPORTED_LANGUAGES: 
    return None
  
  obj = {
    'id': id,
    'content': text,
    'author': author,
    'lang': lang,
    'createdDate': date,
    'channelId': channel_id,
    'channelName': channel_name,
  }
  
  if(embed is not None):
    obj.update({'embed': embed})

  return obj

LOADED_SPACY_MODELS = {}
LOADED_SENTENCE_TRANSFORMER = SentenceTransformer(EMBEDDING_MODEL)
print(f"Loaded sentence transformer model")

for lang in SUPPORTED_LANGUAGES:
  LOADED_SPACY_MODELS[lang] = spacy.load(SPACY_MODELS[lang])
  print(f"Loaded spacy model for [{lang}]")

def _process_by_language(objects):
  lang = objects[0]["lang"]
  print(f"Processing [{lang}] posts: ({len(objects)})")

  nlp = LOADED_SPACY_MODELS[lang]
  sentences = [obj['content'] for obj in objects]
  docs = list(nlp.pipe(sentences))

  for obj, doc in zip(objects, docs):
      lemmatized_tokens = set([token.lemma_ for token in doc if not (token.is_punct or token.is_stop or not token.is_alpha)])
      obj['lemmatized'] = ' '.join(lemmatized_tokens) if len(lemmatized_tokens) > 3 else None

  return objects

def process_json_from_file(path_to_json):
  with open(path_to_json, 'r', encoding='utf-8') as f:
    json_objects = json.load(f)
  return process_json(json_objects)
  
def process_json(json_objects) -> List:
  print("Filtering JSON objects by language:")
  objects = []
  for obj in json_objects:
    processed = _process_obj(obj)
    if processed is not None:
      objects.append(processed)

  print(f"{len(objects)} posts with a recognized language")
  if len(objects) == 0:
    return None

  # Separate processed objects by language
  by_language = defaultdict(list)
  for obj in objects:
    by_language[obj['lang']].append(obj)

  # Run spacy pipeline on separated posts
  objects = []
  for lang in by_language.keys():
    processed = _process_by_language(by_language[lang])
    objects.extend([obj for obj in processed if obj["lemmatized"] is not None])

  print(f"{len(objects)} posts with more than 3 lemmatized tokens")
  if len(objects) == 0:
    return None

  # Compute embeddings on lemmatized tokens
  sentences = [obj["lemmatized"] for obj in objects] 
  print(f"Computing embeddings for {len(sentences)} posts")
  model = LOADED_SENTENCE_TRANSFORMER 
  embeddings = model.encode(sentences)
    
  for embedding, obj in zip(embeddings, objects):
    obj["vector"] = embedding

  return objects



      
      