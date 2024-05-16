from elasticsearch import NotFoundError
from flask import Flask, abort, request, jsonify
from flask_cors import CORS
from configs import PREFIXED_INDEX, PIPELINE_ID
from client.queries import knn, linear_hybrid, more_like_this, multi_match_lang, latest, bool, unique_channels
from client.utils import bulk_index, get_by_id
import urllib.parse

def create_app(client):
  app = Flask(__name__)
  CORS(app)
  
  @app.route('/elastic', methods=['POST'])
  def index():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
      return "Content type not supported."
    docs = request.json
    sent_for_indexing, indexed = bulk_index(client, PREFIXED_INDEX, PIPELINE_ID, docs)
    print(f"Indexed {indexed} out of {sent_for_indexing}")
    return {
      "sent_for_indexing": sent_for_indexing,
      "indexed_successfully": indexed
    }
  
  @app.route('/elastic/info')
  def info():
    return jsonify(client.info().body)
  
  @app.route('/elastic/latest')
  def _latest():
    query = latest()
    result = client.search(index=PREFIXED_INDEX, body=query)['hits']['hits']
    if(len(result)):
      return jsonify({
        'createdDate': result[0]['fields']['createdDate'][0]
      })
    abort(404)

  @app.route('/elastic/channel-info')
  def channel_info():
    afterId = request.args.get('channelId', None)
    afterName = request.args.get('channelName', None)
    after = None
    if(afterId and afterName):
      after = { 'channelId': urllib.parse.unquote(afterId), 'channelName': urllib.parse.unquote(afterName) }
    
    query = unique_channels(after)
    query_result = client.search(index=PREFIXED_INDEX, body=query)['aggregations']['channels']

    results = {
      'channels': [bucket['key'] for bucket in query_result['buckets']]
    }
    if 'after_key' in query_result:
      results.update({'after_key': query_result['after_key']})
    return jsonify(results)

  @app.route('/elastic/similar-mlt/<postId>')
  def similar_mlt(postId):
    postId = urllib.parse.unquote(postId).replace('(xd)', '/')
    must_not = [{"ids": { "values": [postId] }}]
    _from = int(request.args.get('from', 0))
    size = int(request.args.get('size', 10))
    factor = float(request.args.get('factor', 0.7))
    channelId = request.args.get('channelId', False)
    if(channelId):
      channelId = urllib.parse.unquote(channelId).replace('(xd)', '/')
      must_not.append({"term": { "channelId": { "value": channelId } }})


    post = get_post_by_id(postId)
    lang = post.get('lang')
    text_query = bool(
      more_like_this([postId], [lang]),
      must_not
    )
    vector_query = knn(post['vector'], filter=bool({}, must_not))

    query = linear_hybrid(text_query, vector_query, factor, **{'from': _from, 'size': size})
    return jsonify(client.search(index=PREFIXED_INDEX, body=query)['hits']['hits'])
  
  @app.route('/elastic/similar-mml/<postId>')
  def similar_mml(postId):
    postId = urllib.parse.unquote(postId).replace('(xd)', '/')
    must_not = [{"ids": { "values": [postId] }}]
    _from = int(request.args.get('from', 0))
    size = int(request.args.get('size', 10))
    factor = float(request.args.get('factor', 0.7))
    channelId = request.args.get('channelId', False)
    if(channelId):
      channelId = urllib.parse.unquote(channelId).replace('(xd)', '/')
      must_not.append({"term": { "channelId": { "value": channelId } }})
  
    post = get_post_by_id(postId)
    lang = post.get('lang')
    text_query = bool(
      multi_match_lang(post[lang], [lang]), 
      must_not
    )
    vector_query = knn(post['vector'], filter=bool({}, must_not))

    query = linear_hybrid(text_query, vector_query, factor, **{'from': _from, 'size': size})
    return jsonify(client.search(index=PREFIXED_INDEX, body=query)['hits']['hits'])
  
  def get_post_by_id(postId):
    try:
      post = get_by_id(client, PREFIXED_INDEX, postId)
      return post
    except NotFoundError:
      abort(404)

  return app