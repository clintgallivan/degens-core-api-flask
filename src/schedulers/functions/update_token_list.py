
# * Run this once per day before any jobs execute to update the token list
# TODO: try and batch upate to mongodb because it posts one at a time and takes a long time
import os
import requests
from pymongo import MongoClient

cluster = MongoClient(os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster["tokens"]
collection = db["token-list"]

coingecko_base_url = os.getenv('COINGECKO_BASE_URL')
headers = {
    'x-cg-pro-api-key': os.getenv('COINGECKO_API_KEY'),
}

def get_token_list():
    r = requests.get(f'{coingecko_base_url}/coins/list', headers=headers)
    return r.json()

def update_token_list_in_db(token_list):
    for token in token_list:
        # Map the token to the expected structure
        mapped_token = {
            'coingecko_id': token['id'],
        }
        collection.update_one(
            {'coingecko_id': token['id']},  # Query
            {'$set': mapped_token},  # Update
            upsert=True  # If the document doesn't exist, create it
        )
        print(f"updated-token: {token['id']}")

def get_token_list_and_update_db_concurrently():
    update_token_list_in_db(get_token_list())
