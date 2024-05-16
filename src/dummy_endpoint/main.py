from flask import Flask, abort, request, jsonify
from flask_cors import CORS
from faker import Faker
import urllib.parse
import json
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session
import os

fake = Faker()
Faker.seed(420)

api_url = os.getenv('API_URL')
client_id = os.getenv('API_CLIENT_ID')
client_secret = os.getenv('API_CLIENT_SECRET')
token_url = os.getenv('API_TOKEN_URL')

def random_name():
  name = fake.first_name()
  job = fake.job().split(',')[0].strip()
  return f"{name}'s {job}s"


def create_app():
  app = Flask(__name__)
  CORS(app)

  client = BackendApplicationClient(client_id=client_id)
  oauth = OAuth2Session(client=client)
  oauth.fetch_token(token_url=token_url, client_secret=client_secret)
  print(f"Authenticated with token: {client.token}")

  channel_names = {}

  def get_protected(endpoint, params = {}):
    if not endpoint.startswith('/'):
      endpoint = '/' + endpoint
    print(f"Getting from {endpoint} with params: {params}")
    try:
      r = oauth.get(api_url + endpoint, params=params)
    except TokenExpiredError as e:
      print("Token expired, getting new one")
      oauth.refresh_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
      return get_protected(endpoint, params)
    return r.json()
  
  def post_protected(endpoint, params = {}):
    if not endpoint.startswith('/'):
      endpoint = '/' + endpoint
    print(f"Posting to {endpoint} with params: {params}")
    try:
      r = oauth.post(api_url + endpoint, json=params)
    except TokenExpiredError as e:
      print("Token expired, getting new one")
      oauth.refresh_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
      return post_protected(endpoint, params)
    return r.json()
    
  def get_channel_name(channel_id):
    if channel_id in channel_names.keys():
      return channel_names[channel_id]
    try:
      channel_details = get_protected('/channel/journal/channel/data', {'ids': [channel_id]}).get('channels')
      if channel_details and len(channel_details) == 1:
        channel_name = channel_details[0].get('title')
        channel_names[channel_id] = channel_name
        return channel_name
    except Exception:
      pass
    return random_name()

  def map_to_post(obj):
    channel_id = obj.get("channelId")
    embeds = [
      embed.get('fullUrl')
      for embed in obj.get('embeds')
      if type(embed) != list and embed.get('type') == 'media' and embed.get('subType') == 'picture'
    ]
    return {
        "channelId": channel_id,
        'id': obj.get('id'),
        'content': obj.get('content'),
        'author': obj.get('userId'),
        'embed': embeds[0] if len(embeds) else None,
        "channelName": get_channel_name(channel_id),
        "timestamp": obj.get('timestamp'),
        "updateTimestamp": obj.get('updateTimestamp')
      }

  @app.route('/dummy', methods=['GET'])
  def index():
    return "Hello from dummy-endpoint"
  
  @app.route('/dummy/channel-ids', methods=['GET'])
  def channel_ids(_next_id = '', _page_size = 100):
    next_id = str(request.args.get('id', _next_id))
    page_size = int(request.args.get('pageSize', _page_size))

    channel_ids_response = get_protected('/channel/journal/channel/init', {'id': next_id, 'pageSize': page_size})
    ids = [data.get('id') for data in channel_ids_response.get('data')]
    next = channel_ids_response.get('links', None)

    results = { "ids": ids }
    if(next):
      results.update({'next': next.get('next').replace('channel/journal/channel/init', '/dummy/channel-ids')})
    return results
  
  @app.route('/dummy/channels', methods=['GET'])
  def channels():
    next_id = str(request.args.get('id', ''))
    page_size = int(request.args.get('pageSize', 100))

    channel_ids_response = channel_ids(next_id, page_size)
    ids = channel_ids_response.get('ids')
    next = channel_ids_response.get('next', None)

    channel_details_response = get_protected('/channel/journal/channel/data', {'ids': ids})
    channel_details = [ 
      { 'id': channel.get('id'), 'name': channel.get('title') }
      for channel in channel_details_response.get('channels') 
    ]

    for details in channel_details:
      channel_names[details["id"]] = details["name"]

    results = { "channels": channel_details }
    if(next):
      results.update({'next': next.replace('/channel-ids', '/channels')})
    return results

  @app.route('/dummy/test-api')
  def test_api():
    response = get_protected('/channel/journal/channel/init')
    return response

  @app.route('/dummy/channel-posts')
  def posts(_direction = "Up", _timestamp = "", _channel_id = ""):
    request_params = {
      'direction': str(request.args.get('direction', _direction)),
      'timestamp': str(request.args.get('timestamp', _timestamp)),
      "channelId": str(request.args.get('channel_id', _channel_id)) 
    }
    channel_posts_response = post_protected('channel/messages/replay', request_params)
    if channel_posts_response.get('error', None):
      print(f"Error getting posts from {_channel_id}: {channel_posts_response.get('error')}")
      return { 'posts': [], 'more': False }
    
    posts = [map_to_post(post) for post in channel_posts_response.get('messages', [])]
    more = channel_posts_response.get('more', False)

    return {"posts": posts, "more": more}

    

  
  @app.route('/dummy/post/<postId>')
  def get_post(postId):
    ## TODO
    postId = urllib.parse.unquote(postId).replace('(xd)', '/')
    found_posts = [
      map_to_post(obj) 
      for obj in []
      if ('content' in obj and obj.get('_id').get('$binary').get('base64') == postId)
    ]
    if len(found_posts) == 0:
      abort(404)
    elif len(found_posts) > 1:
      print(found_posts)
      abort(500)
    return found_posts[0]

  return app


app = create_app()
