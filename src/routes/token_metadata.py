import os
from flask import Flask, Blueprint
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np

cluster = MongoClient(os.getenv('MONGO_DB_SRV'))
db = cluster["tokens"]
collection = db["token-metadata"]

token_metadata = Blueprint('token_metadata', __name__,
                           template_folder='templates')


@token_metadata.route("/tokens", methods=["GET"])
def get_tokens_metadata():
    all_tokens = list(collection.find({}))
    return json.dumps(all_tokens, default=json_util.default)


@token_metadata.route("/tokens/<coingecko_id>", methods=["GET"])
def get_token_metadata(coingecko_id):
    if not coingecko_id:
        all_tokens = list(collection.find({}))
    else:
        all_tokens = list(collection.find({"coingecko_id": coingecko_id}))
    return json.dumps(all_tokens, default=json_util.default)


@token_metadata.route("/update-token", methods=["POST"])
def update_token():
    html_output = ''
    request_payload = request.json
    token = request_payload
    print(len(token))
    # ! a.1 delete
    if len(token) > 13000:
        for idx, i in enumerate(request_payload):
            print({idx: idx})
            collection.update_one(
                {'coingecko_id': i["coingecko_id"]},
                {"$set": {
                    "degen_rank": i['degen_rank'],
                    "dev_rank": i['dev_rank'],
                    "community_rank": i['community_rank'],
                    "liquidity_rank": i['liquidity_rank'],
                }}
            )
        print('=======done doing that ======')
        return 'Post was successful'
    else:
        # ! a.1 delete
        existing_token = collection.find(
            {"coingecko_id": token["coingecko_id"]})
        existing_token_exists = collection.count_documents(
            {"coingecko_id": token["coingecko_id"]})
        if existing_token_exists > 0:
            for token_document in existing_token:
                print(token_document)
                collection.find_one_and_update({"coingecko_id": token["coingecko_id"]}, {"$set": {
                                               "coingecko_id": token["coingecko_id"], "symbol": token["symbol"],    "name": token["name"], "platforms": token["platforms"],   "categories": token["categories"], "description": token["description"], "homepage": token["homepage"], "blockchain_site":    token["blockchain_site"], "discord": token["discord"], "medium":    token["medium"], "twitter": token["twitter"], "telegram": token["telegram"], "reddit": token["reddit"], "github": token["github"],    "image": token["image"], "contract_address": token["contract_address"], "sentiment_votes_up_percent": token["sentiment_votes_up_percent"], "sentiment_votes_down_percent":     token["sentiment_votes_down_percent"], "market_cap_rank": token["market_cap_rank"], "coingecko_rank": token["coingecko_rank"],   "coingecko_score": token["coingecko_score"], "dev_score": token["dev_score"], "community_score": token["community_score"],     "liquidity_score": token["liquidity_score"],    "public_interest_score": token["public_interest_score"]}},    upsert=True)
                html_output = f"Token with coingecko_id: {token['coingecko_id']}, was updated!"
        else:
            collection.insert_one(
                {"coingecko_id": token["coingecko_id"], "symbol": token["symbol"], "name": token["name"],     "platforms": token["platforms"], "categories": token["categories"], "description": token["description"], "homepage": token["homepage"], "blockchain_site": token["blockchain_site"],    "discord": token["discord"], "medium": token["medium"], "twitter": token["twitter"], "telegram":    token["telegram"], "reddit": token["reddit"], "github": token["github"], "image": token["image"],    "contract_address": token["contract_address"], "sentiment_votes_up_percent": token["sentiment_votes_up_percent"], "sentiment_votes_down_percent": token["sentiment_votes_down_percent"], "market_cap_rank": token["market_cap_rank"], "coingecko_rank":     token["coingecko_rank"], "coingecko_score": token["coingecko_score"], "dev_score": token["dev_score"], "community_score": token["community_score"], "liquidity_score": token["liquidity_score"], "public_interest_score": token["public_interest_score"]})
            html_output = f"Token with coingecko_id did not exist. Created new token with coingecko_id: {token    ['coingecko_id']}!"
        return html_output


@token_metadata.route("/tokens-dataframe", methods=["GET"])
def get_tokens_df():
    all_tokens = list(collection.find({}))
    sorted_tokens = sorted(
        all_tokens, key=lambda k: k['coingecko_score'], reverse=True)
    result = json.dumps(sorted_tokens[0:100], default=json_util.default)
    df = pd.read_json(result, orient='records')
    return df.to_html()
