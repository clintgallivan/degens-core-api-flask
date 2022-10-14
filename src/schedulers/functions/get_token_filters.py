
# * Run once a week to update token list - call get_token_metadata_and_post_concurrently(token_id_list)
import os
import requests
import pandas as pd
import numpy as np
import time
import random
import json
from pymongo import MongoClient

cluster = MongoClient(os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster["tokens"]
collection = db["token-filters"]

coingecko_base_url = os.getenv('COINGECKO_BASE_URL')
mongo_base_url = os.getenv('MONGO_DB_BASE_URL')


def get_platforms_api():
    output = []
    r = requests.get(f'{coingecko_base_url}/asset_platforms')
    for obj in r.json():
        output.append({'value': obj['id'], 'label': obj['name']})
    return output


def get_categories_api():
    output = []
    r = requests.get(f'{coingecko_base_url}/coins/categories/list')
    for obj in r.json():
        output.append({'value': obj['name'], 'label': obj['name']})
    return output


def build_output():
    output = {
        'categories': get_categories_api(),
        'platforms': get_platforms_api(),
    }
    return output


def post_to_db(ds):
    collection.delete_many({})
    collection.insert_one(ds)


def get_token_filters_and_post_concurrently():
    post_to_db(build_output())
    return
