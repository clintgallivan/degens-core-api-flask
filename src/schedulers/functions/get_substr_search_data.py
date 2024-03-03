
# * Run once a day to update the substr-search collection - call get_token_substr_data_and_post_concurrently()
import os
import requests
import json
from pymongo import MongoClient

# Create a MongoDB client
cluster = MongoClient(os.getenv('MONGO_DB_SRV'), connect=False)

# Get the 'tokens' database and the 'token-metadata' collection
db = cluster["tokens"]
collection_token_metadata = db["token-metadata"]
collection_substr_search = db["substr-search"]


def get_token_current_metadata():
    # Fetch data directly from MongoDB collection
    tokens = collection_token_metadata.find()
    return [token for token in tokens]

def post_to_substring_db(ds):
    collection_substr_search.update_one(
        {'coingecko_id': ds['coingecko_id']},  # Query
        {'$set': ds},  # Update
        upsert=True  # If the document doesn't exist, create it
    )
    print(f"updated-token: {ds['coingecko_id']}")

def reduce_data_and_post(table):
    for item in table:
        ds = {}
        ds["coingecko_id"] = item.get('coingecko_id', '')
        ds["image"] = item.get("image", '')
        ds["market_cap_rank"] = item.get("market_cap_rank", '')
        ds["degen_rank"] = item.get("degen_rank", '')
        ds["iterator"] = [item.get("name", ''), item.get("symbol", '')]
        post_to_substring_db(ds)

def get_token_substr_data_and_post_concurrently():
    print('beginning parse through token list')
    table = get_token_current_metadata()
    reduce_data_and_post(table)
    print('done')

get_token_substr_data_and_post_concurrently()