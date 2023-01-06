
# * Run once an hour to update user historical data - call
import os
import requests
import pandas as pd
import numpy as np
import time
import random
import json
from bson import json_util
from datetime import datetime, timedelta
from pymongo import MongoClient, UpdateOne
import pytz
import copy
coingecko_base_url = os.getenv('COINGECKO_BASE_URL')
mongo_base_url = os.getenv('MONGO_DB_BASE_URL')

cluster = MongoClient(os.getenv('MONGO_DB_SRV'))
db = cluster["tokens"]
collection = db["users"]

now = datetime.now(pytz.utc)
new_user_data = []


def get_user_info():
    params = {'cron': 'true'}
    keys_to_include = {}
    if params.get('cron'):
        keys_to_include = {
            "uid": 1, "portfolio_metadata": 1, "historical.portfolios.season_1": {'$slice': 1}, "historical.portfolios.all_time": {'$slice': 1}}
    all_users = list(collection.find(
        {}, keys_to_include))
    return all_users


def create_token_list_to_update(user_info):
    token_set = set([])
    for i in user_info:
        portfolios = i['historical']['portfolios']
        for i in portfolios:
            token_obj = portfolios[i][0]['tokens']
            for i in token_obj:
                coingecko_id = i['coingecko_id']
                token_set.add(coingecko_id)
    split_up_set = [list(token_set)[x:x+250]
                    for x in range(0, len(list(token_set)), 250)]
    return split_up_set


def get_current_prices(token_list):
    output = {}
    for set in token_list:
        parsed_token_ids = ",".join(set)
        params = {"vs_currency": "usd", "order": "market_cap_desc",
                  "per_page": 250, "page": 1, "ids": parsed_token_ids}
        r = requests.get(f'{coingecko_base_url}/coins/markets', params=params)
        for i in r.json():
            output[i['id']] = {
                'current_price': i['current_price'], 'mcap_rank': i['market_cap_rank']}
    return output


def run_calcs_and_update_user(user_info, current_prices):
    for user_original in user_info:
        user_updated = copy.deepcopy(user_original)
        historical_portfolios = user_original['historical']['portfolios']
        for portfolio in historical_portfolios:
            score_original = historical_portfolios[portfolio][0]['score']
            tokens = historical_portfolios[portfolio][0]['tokens']

            def percent_score_increase_and_new_token_arr():
                total_weight = 0
                for i in tokens:
                    price_after = current_prices[i['coingecko_id']
                                                 ]['current_price']
                    price_before = i['price']
                    percent = i['percent']
                    weighted_change = (price_after/price_before) * percent
                    total_weight = total_weight + weighted_change

                new_tokens = []
                for i in tokens:
                    price_after = current_prices[i['coingecko_id']
                                                 ]['current_price']
                    price_before = i['price']
                    percent = i['percent']
                    weighted_change = (price_after/price_before) * percent
                    new_token = {
                        "coingecko_id": i['coingecko_id'],
                        "price": price_after,
                        "percent": weighted_change/total_weight,
                        "mcap_rank": current_prices[i['coingecko_id']]['mcap_rank']
                    }
                    new_tokens.append(new_token)
                user_updated['historical']['portfolios'][portfolio][0]['tokens'] = new_tokens
                return total_weight

            def update_score():
                score_after = percent_score_increase_and_new_token_arr() * score_original
                user_updated['historical']['portfolios'][portfolio][0]['score'] = score_after
                return

            def update_timestamp():
                user_updated['historical']['portfolios'][portfolio][0]['timestamp'] = now.isoformat(
                    timespec='seconds').replace('+00:00', 'Z')

            def update_avg_mcap_rank():
                og_prev = user_original['historical']['portfolios'][portfolio][0]['timestamp'].replace(
                    tzinfo=pytz.UTC)
                og_crea = user_original['portfolio_metadata'][portfolio]['creation_date'].replace(
                    tzinfo=pytz.UTC)

                previous_period_duration = og_prev - og_crea
                current_period_duration = now - og_prev
                total_duration = now - og_crea

                current_period_total_weight = current_period_duration/total_duration
                previous_period_total_weight = previous_period_duration/total_duration

                def current_period_avg_mcap_rank():
                    total_average = 0
                    for i in user_original['historical']['portfolios'][portfolio][0]['tokens']:
                        mcap_rank = i['mcap_rank']
                        starting_percent = i['percent']
                        ending_percent = starting_percent
                        for token_obj in user_updated['historical']['portfolios'][portfolio][0]['tokens']:
                            if i['coingecko_id'] == token_obj['coingecko_id']:
                                ending_percent = token_obj['percent']
                        avg_percent = (starting_percent + ending_percent) / 2
                        total_average = total_average + \
                            (mcap_rank * avg_percent)
                    return total_average

                previous_period_avg = previous_period_total_weight * \
                    user_original['historical']['portfolios'][portfolio][0]['average_mcap_rank']
                current_period_avg = current_period_total_weight * current_period_avg_mcap_rank()
                new_avg_rank = previous_period_avg + current_period_avg
                user_updated['historical']['portfolios'][portfolio][0]['average_mcap_rank'] = new_avg_rank
                return

            update_score()
            update_avg_mcap_rank()
            update_timestamp()
        new_user_data.append(user_updated)


def post_to_db():
    count = 0
    batchsize = 100
    for i in range(0, len(new_user_data), batchsize):
        batch = new_user_data[i:i+batchsize]
        bulk_requests = []
        for user in batch:
            count = count + 1
            portfolio_to_push = {}
            for key in user['historical']['portfolios']:
                def str_to_datetime(timestamp_as_str):
                    return datetime.strptime(timestamp_as_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                user['historical']['portfolios'][f'{key}'][0]['timestamp'] = str_to_datetime(
                    user['historical']['portfolios'][f'{key}'][0]['timestamp'])
                portfolio_to_push[f'historical.portfolios.{key}'] = {
                    '$each': [
                        user['historical']['portfolios'][f'{key}'][0],
                    ],
                    '$position': 0
                }
            bulk_requests.append(UpdateOne({'uid': user['uid']}, {
                '$push': portfolio_to_push
            }))
        collection.bulk_write(bulk_requests)
        print(f'{count} users were updated!')
        time.sleep(1)


def batch_update_user_leaderboards():
    print('started batch updating users')
    user_info = get_user_info()
    token_list = create_token_list_to_update(user_info)
    current_prices = get_current_prices(token_list)
    run_calcs_and_update_user(user_info, current_prices)
    print('posting')
    post_to_db()
    print('finished batch updating users')


# batch_update_user_leaderboards()
