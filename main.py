from flask import Flask
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np
from src.routes.tokens import token_metadata


cluster = MongoClient(
    "mongodb+srv://cgallivan:newui123@cluster0.r1pdh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["tokens"]
collection = db["token-metadata"]

app = Flask(__name__)

app.register_blueprint(token_metadata)


@app.route("/tokens-dataframe", methods=["GET"])
def get_tokens_df():
    all_tokens = list(collection.find({}))
    sorted_tokens = sorted(
        all_tokens, key=lambda k: k['coingecko_score'], reverse=True)
    result = json.dumps(sorted_tokens[0:100], default=json_util.default)
    df = pd.read_json(result, orient='records')
    # df.to_csv('datafram.csv')
    return df.to_html()
    # return df.to_csv('datafram.csv')
    # return sorted_result

# *instead of: key=lambda k:k['KEY'] -> key=lambda_func


def lambda_func(e):
    return e['coingecko_score']


@ app.route("/update-token", methods=["POST"])
def update_token():
    html_output = ''
    request_payload = request.json
    token = request_payload
    print(token)
    existing_token = collection.find({"coingecko_id": token["coingecko_id"]})
    existing_token_exists = collection.count_documents(
        {"coingecko_id": token["coingecko_id"]})

    if existing_token_exists > 0:
        for token_document in existing_token:
            print(token_document)
            collection.find_one_and_update({"coingecko_id": token["coingecko_id"]}, {"$set": {
                                           "coingecko_id": token["coingecko_id"], "symbol": token["symbol"], "name": token["name"], "platforms": token["platforms"], "categories": token["categories"], "description": token["description"], "homepage": token["homepage"], "blockchain_site": token["blockchain_site"], "discord": token["discord"], "medium": token["medium"], "twitter": token["twitter"], "telegram": token["telegram"], "reddit": token["reddit"], "github": token["github"], "image": token["image"], "contract_address": token["contract_address"], "sentiment_votes_up_percent": token["sentiment_votes_up_percent"], "sentiment_votes_down_percent": token["sentiment_votes_down_percent"], "market_cap_rank": token["market_cap_rank"], "coingecko_rank": token["coingecko_rank"], "coingecko_score": token["coingecko_score"], "dev_score": token["dev_score"], "community_score": token["community_score"], "liquidity_score": token["liquidity_score"], "public_interest_score": token["public_interest_score"]}}, upsert=True)
            html_output = f"Token with coingecko_id: {token['coingecko_id']}, was updated!"
    else:
        collection.insert_one(
            {"coingecko_id": token["coingecko_id"], "symbol": token["symbol"], "name": token["name"], "platforms": token["platforms"], "categories": token["categories"], "description": token["description"], "homepage": token["homepage"], "blockchain_site": token["blockchain_site"], "discord": token["discord"], "medium": token["medium"], "twitter": token["twitter"], "telegram": token["telegram"], "reddit": token["reddit"], "github": token["github"], "image": token["image"], "contract_address": token["contract_address"], "sentiment_votes_up_percent": token["sentiment_votes_up_percent"], "sentiment_votes_down_percent": token["sentiment_votes_down_percent"], "market_cap_rank": token["market_cap_rank"], "coingecko_rank": token["coingecko_rank"], "coingecko_score": token["coingecko_score"], "dev_score": token["dev_score"], "community_score": token["community_score"], "liquidity_score": token["liquidity_score"], "public_interest_score": token["public_interest_score"]})
        html_output = f"Token with coingecko_id did not exist. Created new token with coingecko_id: {token['coingecko_id']}!"
    return html_output


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
