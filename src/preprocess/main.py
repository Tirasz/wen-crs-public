import json
import pickle
import torch
import requests
from configs import DUMMY_CLIENT, ELASTIC_CLIENT, PROCESS_LIMIT
from process import process_json
from utils import to_json, get_all_channel_ids, get_all_posts_for_channel
from datetime import datetime, timedelta
import concurrent.futures
import os
import math

os.environ["TOKENIZERS_PARALLELISM"] = "true"

def index(processed):
  print(f"Indexing {len(processed)} objects")
  index_url = ELASTIC_CLIENT + '/elastic'
  res = requests.post(index_url, json = to_json(processed))
  print("Indexing done!")


def main():

  print(f"Getting latest post in elasticsearch: ")
  res = requests.get(ELASTIC_CLIENT+'/elastic/latest')
  if(res.status_code == 200):
    # Start from a day before latest_timestamp to be sure + weird timestamp shenanigans
    latest_timestamp = (datetime.fromisoformat(res.json()['createdDate'][:-1]) - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')+".000Z"
  else:
    latest_timestamp = "1970-01-01T00:00:00.000Z"
  print(f"Latest timestamp: {latest_timestamp}")

  print(f"Getting all channel ids available: ")
  ids = get_all_channel_ids()
  print(f"Got {len(ids)} channel-ids")

  print(f"Getting channel posts created/updated after: {latest_timestamp}")
  crawled_channels = 0
  collected_posts = 0

  for channel_id in ids:
    channel_posts = get_all_posts_for_channel(channel_id, latest_timestamp)
    collected_posts += len(channel_posts)
    crawled_channels += 1
    print(f"Processed posts: {collected_posts} ({crawled_channels}/{len(ids)})")
    if len(channel_posts) > 0:
      process_in_batches(channel_posts)


def process_in_batches(_posts):
  start_index = 0
  total_posts = len(_posts)
  batch = 1
  print(f"Indexing {total_posts} posts in batches of size {PROCESS_LIMIT}")
  while start_index < total_posts:
    end_index = min(start_index + PROCESS_LIMIT, total_posts)
    posts_in_batch = _posts[start_index:end_index]
    print(f"######## Batch {batch}/{math.ceil(total_posts / PROCESS_LIMIT)} ########")
    processed = process_json(posts_in_batch)
    if processed is not None:
      index(processed)
    batch += 1
    start_index = end_index


if __name__ == '__main__' and DUMMY_CLIENT and ELASTIC_CLIENT:
  if(torch.cuda.is_available()):
    print(f"CUDA: {torch.cuda.device_count()} device(s):")
    for i in range(torch.cuda.device_count()):
      print(f"({i}): {torch.cuda.get_device_name(0)}")
  main()


