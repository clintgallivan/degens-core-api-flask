import os
from flask import Flask, Blueprint
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np
import datetime as dt
import pytz

cluster = MongoClient(os.getenv('MONGO_DB_SRV'))
db = cluster["tokens"]
collection = db["token-timeseries"]

token_timeseries = Blueprint('token_timeseries', __name__,
                             template_folder='templates')


@token_timeseries.route("/token-timeseries", methods=["GET", "POST"])
def get_tokens_timeseries():
    if request.method == 'GET':
        all_tokens = list(collection.find({}))
        return json.dumps(all_tokens, default=json_util.default)
    # else:
    #     print('Can not process this request.')

    #     html_output = ''
    #     request_payload = request.json
    #     token = request_payload
    #     print(token)
    #     print(len(token))
    #     timestamp = dt.datetime.now(pytz.utc)
    #     if len(token) == 14:
    #         existing_token = collection.find(
    #             {"coingecko_id": token["coingecko_id"]})
    #         existing_token_exists = collection.count_documents(
    #             {"coingecko_id": token["coingecko_id"]})
    #         if existing_token_exists > 0:
    #             for token_document in existing_token:
    #                 collection.update_one(
    #                     {'coingecko_id': token["coingecko_id"]},
    #                     {"$push": {
    #                         "historical": {
    #                             "$each": [
    #                                 {
    #                                     "timestamp": timestamp,
    #                                     "price": token["price"],
    #                                     "market_cap": token["market_cap"],
    #                                     "market_cap_rank": token["market_cap_rank"],
    #                                     "coingecko_rank": token["coingecko_rank"],
    #                                     "coingecko_score": token["coingecko_score"],
    #                                     "dev_score": token["dev_score"],
    #                                     "community_score": token["community_score"],
    #                                     "liquidity_score": token["liquidity_score"],
    #                                     "public_interest_score": token["public_interest_score"],
    #                                     "community_data": token["community_data"],
    #                                     "developer_data": token["developer_data"],
    #                                     "degen_rank": None,
    #                                     "dev_rank": None,
    #                                     "community_rank": None,
    #                                     "liquidity_rank": None
    #                                 }
    #                             ],
    #                             "$position": 0
    #                         }
    #                     }}
    #                 )
    #             html_output = f"Token with coingecko_id: {token['coingecko_id']}, was updated!"
    #         else:
    #             collection.insert_one(
    #                 {
    #                     "coingecko_id": token["coingecko_id"],
    #                     "symbol": token["symbol"],
    #                     "name": token["name"],
    #                     "historical": [{
    #                         "timestamp": timestamp,
    #                         "price": token["price"],
    #                         "market_cap": token["market_cap"],
    #                         "market_cap_rank": token["market_cap_rank"],
    #                         "coingecko_rank": token["coingecko_rank"],
    #                         "coingecko_score": token["coingecko_score"],
    #                         "dev_score": token["dev_score"],
    #                         "community_score": token["community_score"],
    #                         "liquidity_score": token["liquidity_score"],
    #                         "public_interest_score": token["public_interest_score"],
    #                         "community_data": token["community_data"],
    #                         "developer_data": token["developer_data"]
    #                     }]
    #                 }
    #             )
    #             html_output = f"Token with coingecko_id did not exist. Created new token with coingecko_id: {token    ['coingecko_id']}!"
    #     else:
    #         print(request_payload)
    #         output = []
    #         print('starting loop')
    #         for idx, i in enumerate(request_payload):
    #             print({idx: idx})
    #             collection.update_one(
    #                 {'coingecko_id': i["coingecko_id"]},
    #                 {"$set": {
    #                     "historical.0.degen_rank": i['degen_rank'],
    #                     "historical.0.dev_rank": i['dev_rank'],
    #                     "historical.0.community_rank": i['community_rank'],
    #                     "historical.0.liquidity_rank": i['liquidity_rank'],
    #                 }}
    #             )
    #             output.append(i["coingecko_id"])
    #         print('=======done doing that ======')
    #         html_output = f"Tokens with coingecko_ids {output}: , was updated!"
    # return html_output


@token_timeseries.route("/token-timeseries/<coingecko_id>", methods=["GET", "POST"])
def get_token_metadata(coingecko_id):
    if request.method == "GET":
        if not coingecko_id:
            all_tokens = list(collection.find({}))
        else:
            all_tokens = list(collection.find({"coingecko_id": coingecko_id}))
        return json.dumps(all_tokens, default=json_util.default)
    else:
        print('can not process this request')
