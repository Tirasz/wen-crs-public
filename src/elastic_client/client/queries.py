from typing import List
from .utils import get_stopwords, load_query
from configs import PREFIXED_INDEX

def more_like_this(ids: List[str], languages: List[str], **kwargs):
  """https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-mlt-query.html"""
  query = load_query('mlt')
  query['more_like_this']['like'] = [{'_index': PREFIXED_INDEX, '_id': id} for id in ids]
  query['more_like_this']['stop_words'] = get_stopwords()
  query['more_like_this']['fields'] = languages 
  query['more_like_this'].update(kwargs)
  return query


def knn(vector, **kwargs):
  """https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html"""
  query = load_query('knn')
  query["query_vector"] = vector
  query.update(kwargs)
  return query

def multi_match_lang(query_str, languages: List[str], **kwargs):
  """
  https://www.elastic.co/blog/multilingual-search-using-language-identification-in-elasticsearch
  https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html
  """
  query = load_query("mml")
  query['multi_match']['query'] = query_str
  query['multi_match']['fields'] = languages
  query['multi_match'].update(kwargs)
  return query

def linear_hybrid(text_query, vector_query, vector_ratio = 0.5, **kwargs):
  """
  https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html#_combine_approximate_knn_with_other_features
  """
  t_query_key = list(text_query.keys())[0]
  text_query[t_query_key].update({"boost": 1-vector_ratio})
  vector_query.update({"boost": vector_ratio})

  query = load_query("lin-hybrid")
  query.update({
    "query": text_query,
    "knn": vector_query
  })
  query.update(kwargs)
  return query

def rrf_hybrid(text_query, vector_query, **kwargs):
  """
  paid feature? :(
  https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html#rrf-api
  """
  query = load_query("rrf-hybrid")
  query.update({
    "query": text_query,
    "knn": vector_query
  })
  query.update(kwargs)
  return query

def bool(must_query, must_not_query, **kwargs):
  """https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html"""
  b_query = {}
  if must_query:
    b_query['must'] = must_query
  if must_not_query:
    b_query['must_not'] = must_not_query
  
  query = {
    "bool": b_query
  }
  query.update(kwargs)
  return query

def latest():
  query = load_query("latest")
  return query


def unique_channels(after = None):
  query = load_query("unique-channels")
  if(after):
    query["aggs"]["channels"]["composite"]["after"] = after
  return query
  