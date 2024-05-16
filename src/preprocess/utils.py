from io import StringIO
import json
from markdown import Markdown
import numpy as np
import requests
from configs import DUMMY_CLIENT

def _unmark_element(element, stream=None):
  if stream is None:
    stream = StringIO()
  if element.text:
    stream.write(element.text)
  for sub in element:
    _unmark_element(sub, stream)
  if element.tail:
    stream.write(element.tail)
  return stream.getvalue()

# patching Markdown
Markdown.output_formats["plain"] = _unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False

def unmark(text):
  return __md.convert(text)

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
def to_json(docs):
  return json.loads(json.dumps(docs, cls=NumpyEncoder))


def get_all_channel_ids():
  next = '/dummy/channels'
  ids = []
  batch = 1
  while next is not None:
    #print(f"Getting batch {batch} with {next}")

    response = requests.get(f"{DUMMY_CLIENT}{next}").json()
    _ids = [channel.get('id') for channel in response.get('channels')]

    #print(f"Got {len(_ids)} channel-ids")

    ids.extend(_ids)
    next = response.get('next', None)
    batch += 1
  return ids

def get_all_posts_for_channel(channel_id, timestamp = ""):
  next = f"/dummy/channel-posts?channel_id={channel_id}&timestamp={timestamp}&direction=Down"
  posts = []
  batch = 1
  while next is not None:
    #print(f"Getting batch {batch} with {next}")

    response = requests.get(f"{DUMMY_CLIENT}{next}").json()
    _posts = response.get('posts')
    _more = response.get('more')

    #print(f"Got {len(_posts)} posts")

    if _more:
      latest = max([post.get('timestamp') for post in _posts])
      next = f"/dummy/channel-posts?channel_id={channel_id}&timestamp={latest}&direction=Down"
    else:
      next = None
    
    posts.extend(_posts)
    batch += 1
  return sorted(posts, key=lambda x: x['timestamp'])