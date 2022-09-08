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
collection = db["substr-search"]

substr_search = Blueprint('substr_search', __name__,
                          template_folder='templates')


@ substr_search.route("/substr-tokens", methods=["GET", "POST"])
def get_substr_tokens():
    if request.method == 'POST':
        html_output = ''
        request_payload = request.json
        token = request_payload
        print(token)
        existing_token = collection.find(
            {"coingecko_id": token["coingecko_id"]})
        existing_token_exists = collection.count_documents(
            {"coingecko_id": token["coingecko_id"]})
        if existing_token_exists > 0:
            for token_document in existing_token:
                print(token_document)
                collection.find_one_and_update({"coingecko_id": token["coingecko_id"]}, {"$set": {
                    "coingecko_id": token["coingecko_id"], "iterator": token["iterator"], "market_cap_rank": token["market_cap_rank"], "degen_rank": token["degen_rank"], "image": token["image"]}}, upsert=True)
                html_output = f"Token with coingecko_id: {token['coingecko_id']}, was updated!"
        else:
            collection.insert_one(
                {
                    "coingecko_id": token["coingecko_id"], "iterator": token["iterator"], "market_cap_rank": token["market_cap_rank"], "degen_rank": token["degen_rank"], "image": token["image"]
                }
            )
            html_output = f"Token with coingecko_id did not exist. Created new token with coingecko_id: {token['coingecko_id']}!"
        return html_output
    else:
        all_tokens = list(collection.find({}))
        return json.dumps(all_tokens, default=json_util.default)
# from flask import Flask, Blueprint
# from flask import request
# import pymongo
# from pymongo import MongoClient
# import json
# from bson import json_util
# import pandas as pd
# import numpy as np

# cluster = MongoClient(
#     "mongodb+srv://cgallivan:P%40perless2020@cluster0.r1pdh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = cluster["tokens"]
# collection = db["substr-search"]

# substr_search = Blueprint('substr_search', __name__,
#                           template_folder='templates')


# @substr_search.route("/substr-tokens", methods=["GET", "POST"])
# def get_substr_tokens():
#     if request.method == 'POST':
#         html_output = ''
#         request_payload = request.json
#         token = request_payload
#         print(token)
#         existing_token = collection.find(
#             {"coingecko_id": token["coingecko_id"]})
#         existing_token_exists = collection.count_documents(
#             {"coingecko_id": token["coingecko_id"]})
#         if existing_token_exists > 0:
#             for token_document in existing_token:
#                 print(token_document)
#                 collection.find_one_and_update({"coingecko_id": token["coingecko_id"]}, {"$set": {
#                     "coingecko_id": token["coingecko_id"], "symbol": token["symbol"], "name": token["name"], "market_cap_rank": token["market_cap_rank"], "degen_rank": token["degen_rank"], "image": token["image"]}}, upsert=True)
#                 html_output = f"Token with coingecko_id: {token['coingecko_id']}, was updated!"
#         else:
#             collection.insert_one(
#                 {
#                     "coingecko_id": token["coingecko_id"], "symbol": token["symbol"], "name": token["name"], "market_cap_rank": token["market_cap_rank"], "degen_rank": token["degen_rank"], "image": token["image"]
#                 }
#             )
#             html_output = f"Token with coingecko_id did not exist. Created new token with coingecko_id: {token['coingecko_id']}!"
#         return html_output
#     else:
#         all_tokens = list(collection.find({}))
#         return json.dumps(all_tokens, default=json_util.default)
