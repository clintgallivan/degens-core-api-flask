
# * Run once a week to update token list - call get_token_metadata_and_post_concurrently(token_id_list)

import requests
import pandas as pd
import numpy as np
import time
import random
import json
coingecko_base_url = 'https://api.coingecko.com/api/v3'
mongo_base_url = 'http://127.0.0.1:5000'


def get_token_list():
    output = []
    r = requests.get(f'{coingecko_base_url}/coins/list')
    for token_object in r.json():
        output.append(token_object['id'])
    return output


def get_token_metadata(token_id):
    ds = {}
    r = requests.get(f'{coingecko_base_url}/coins/{token_id}')
    result = r.json()
    # print(result.get("links", '').get("telegram_channel_identifier", ''))
    ds["coingecko_id"] = result.get('id', '')
    ds["symbol"] = result.get('symbol', '')
    ds["name"] = result.get("name", '')
    ds["platforms"] = (list(result['platforms'].keys()))
    ds["categories"] = result.get('categories', '')
    ds['description'] = result.get('description', '').get('en', '')
    ds["homepage"] = result.get('links', '').get('homepage', '')
    ds["blockchain_site"] = result.get("links", '').get("blockchain_site", '')
    ds["discord"] = result.get("links", '').get("chat_url", '')
    ds["medium"] = result.get("links", '').get("announcement_url", '')
    if check_if_value(result.get("links", '').get("twitter_screen_name", '')):
        ds["twitter"] = "https://twitter.com/" + \
            result.get("links", '').get("twitter_screen_name", '')
    else:
        ds["twitter"] = "https://twitter.com/"
    if check_if_value(result.get("links", '').get("telegram_channel_identifier", '')):
        ds["telegram"] = "https://t.me/" + \
            result.get("links", '').get("telegram_channel_identifier", '')
    else:
        ds["telegram"] = "https://t.me/"
    ds["reddit"] = result.get("links", '').get("subreddit_url", '')
    ds["github"] = result.get("links", '').get(
        "repos_url", '').get("github", '')
    ds["image"] = result.get("image", '').get("large", '')
    ds["contract_address"] = result.get("contract_address", '')
    ds["sentiment_votes_up_percent"] = result.get(
        "sentiment_votes_up_percentage", '')
    ds["sentiment_votes_down_percent"] = result.get(
        "sentiment_votes_down_percentage", '')
    ds["market_cap_rank"] = result.get("market_cap_rank", '')
    ds["coingecko_rank"] = result.get("coingecko_rank", '')
    ds["coingecko_score"] = result.get("coingecko_score", '')
    ds["dev_score"] = result.get("developer_score", '')
    ds["community_score"] = result.get("community_score", '')
    ds["liquidity_score"] = result.get("liquidity_score", '')
    ds["public_interest_score"] = result.get("public_interest_score", '')
    print('captured token object')
    return json.dumps(ds)


def check_if_value(result_key):
    if result_key != None:
        return True
    else:
        return False


def post_to_db(ds):
    headers = {'Content-type': 'application/json'}
    r = requests.post(f'{mongo_base_url}/update-token',
                      data=ds, headers=headers)
    # print(r.content)


def get_token_metadata_and_post_concurrently(token_id_list):
    for token_id in token_id_list[6520:]:
        ds = get_token_metadata(token_id)
        post_to_db(ds)
        time.sleep(1.4)
    return
