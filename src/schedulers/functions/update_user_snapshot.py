
# * Run once per day to update user each historical[portfolio] and portfolio_metadata[portfolio].ranks
import os
from flask import jsonify
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

cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster["tokens"]
collection = db["users"]
coingecko_base_url = os.getenv('COINGECKO_BASE_URL')
mongo_base_url = os.getenv('MONGO_DB_BASE_URL')
headers = {
    'x-cg-pro-api-key': os.getenv('COINGECKO_API_KEY'),
}

new_users_data = []

active_portfolios = ['season_1', 'all_time']

def start_backend_job(users_collection):
    # Set the update_in_progress flag
    users_collection.update_many({}, {'$set': {'update_in_progress': True}})

def end_backend_job(users_collection):
    # Clear the update_in_progress flag
    users_collection.update_many({}, {'$set': {'update_in_progress': False}})

def get_user_info(page=1, items_per_page=100,):
    params = {'cron': 'true'}
    keys_to_include = {}
    if params.get('cron'):
        keys_to_include = {
            "uid": 1, "name": 1, "image": 1, "portfolio_metadata": 1
        }

        for portfolio in active_portfolios:
            keys_to_include[f"historical.portfolios.{portfolio}"] = {'$slice': 200}
        
    # Calculate number of documents to skip
    skip = (page - 1) * items_per_page

    paginated_users = list(collection.find({}, keys_to_include).skip(skip).limit(items_per_page).max_time_ms(10000))

    return paginated_users

# * This function gets all users from the db in paginated form to not throttle our mongodb
def get_all_users(items_per_page=100):
    all_users = []
    page = 1
    while True:
        users = get_user_info(page=page, items_per_page=items_per_page)
        if not users:
            break
        all_users.extend(users)
        page += 1
        time.sleep(2)
    return all_users

# * This creates a list of tokens to update that are in currently active portfolios (this is needed because seasons will will stop updating at a certain point when season concludes).
def create_token_list_sets_to_update(user_info):
    token_set = set([])
    for i in user_info:
        portfolios = i['historical']['portfolios']
        for i in portfolios:
            if i not in active_portfolios:
                continue
            token_obj = portfolios[i][0]['tokens']
            for i in token_obj:
                coingecko_id = i['coingecko_id']
                token_set.add(coingecko_id)
    split_up_set = [list(token_set)[x:x+250]
                    for x in range(0, len(list(token_set)), 250)]
    return split_up_set


def get_current_token_data(token_list_sets):
    output = {}
    for set in token_list_sets:
        parsed_token_ids = ",".join(set)
        params = {"vs_currency": "usd", "order": "market_cap_desc",
                  "per_page": 250, "page": 1, "ids": parsed_token_ids}
        for i in requests.get(f'{coingecko_base_url}/coins/markets', params=params, headers=headers).json():
            output[i['id']] = {
                'current_price': i['current_price'], 'mcap_rank': i['market_cap_rank'], 'image': i['image']}
    return output


def run_calcs_and_update_user(user_info, current_prices):
    # * For each user, update each active portfolio
    for user_original in user_info:
        user_updated = copy.deepcopy(user_original)
        historical_portfolios = user_original['historical']['portfolios']
        for portfolio in historical_portfolios:
            if portfolio not in active_portfolios:
                continue
            score_original = historical_portfolios[portfolio][0]['score']
            tokens = historical_portfolios[portfolio][0]['tokens']

            def percent_score_increase_and_new_token_arr():
                total_weight = 0
                # * Based on current price fluctuations, these two iterators below will calculate the new percent for each token in the portfolio, and then return the total weight (tokenPriceChange * percent) of all tokens in the portfolio
                for i in tokens:
                    price_after = current_prices[i['coingecko_id']]['current_price']
                    price_before = i['price']
                    percent = i['percent']
                    weighted_change = (price_after/price_before) * percent
                    total_weight = total_weight + weighted_change
                new_tokens = []
                for i in tokens:
                    price_after = current_prices[i['coingecko_id']]['current_price']
                    price_before = i['price']
                    percent = i['percent']
                    weighted_change = (price_after/price_before) * percent
                    new_token = {
                        "coingecko_id": i['coingecko_id'],
                        "price": price_after,
                        "percent": weighted_change/total_weight,
                        "mcap_rank": current_prices[i['coingecko_id']]['mcap_rank'],
                        "image": current_prices[i['coingecko_id']]['image']

                    }
                    new_tokens.append(new_token)
                user_updated['historical']['portfolios'][portfolio][0]['tokens'] = new_tokens
                return total_weight

            # * This function will update the user's score by taking the original score and then multiplying it by the total_weight (aka the percentage change)
            def update_score():
                score_after = percent_score_increase_and_new_token_arr() * score_original
                user_updated['historical']['portfolios'][portfolio][0]['score'] = score_after
                return
            
            # * This function will update the timestamp to the current time
            def update_timestamp():
                user_updated['historical']['portfolios'][portfolio][0]['timestamp'] = datetime.now(pytz.utc).isoformat(
                    timespec='seconds').replace('+00:00', 'Z')

            def update_avg_mcap_rank():
                og_prev = user_original['historical']['portfolios'][portfolio][0]['timestamp'].replace(
                    tzinfo=pytz.UTC)
                og_crea = user_original['portfolio_metadata'][portfolio]['creation_date'].replace(
                    tzinfo=pytz.UTC)

                previous_period_duration = og_prev - og_crea
                current_period_duration = datetime.now(pytz.utc) - og_prev
                total_duration = datetime.now(pytz.utc) - og_crea

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
        new_users_data.append(user_updated)

# * This function will calculate the ranks for each user based on their scores and the percentage change in their scores over the last 7 and 30 days
# * You will how the historical.portfolios[portfolio][0].rank, change_7_days_rank, change_30_days_rank, change_7_days, and change_30_days fields are updated. Also it replaces the same data in portfolio_metadata
def calc_ranks_and_update_user(new_users_data):
    # Prepare a dictionary to store user scores for each portfolio
    user_scores = {portfolio: [] for portfolio in active_portfolios}
    user_changes_7_days = {portfolio: [] for portfolio in active_portfolios}
    user_changes_30_days = {portfolio: [] for portfolio in active_portfolios}

    for user_data in new_users_data:
        if 'portfolio_metadata' not in user_data:
            user_data['portfolio_metadata'] = {}
        for portfolio in active_portfolios:
            if portfolio not in user_data['portfolio_metadata']:
                user_data['portfolio_metadata'][portfolio] = {}
            user_data['portfolio_metadata'][portfolio]['ranks'] = {'rank': None, 'change_7_days': None, 'change_30_days': None, 'change_7_days_rank': None, 'change_30_days_rank': None}

        historical_portfolios = user_data['historical']['portfolios']
        for portfolio_name in active_portfolios:
            portfolios = historical_portfolios.get(portfolio_name, [])
            if portfolios:  # only assign a score if the portfolio is not empty
                score = portfolios[0].get('score', 0)
                user_scores[portfolio_name].append((user_data, score))

                # Calculate the percentage change in score over the last 7 and 30 days
                now = datetime.now()
                for portfolio in reversed(portfolios):
                    timestamp = portfolio.get('timestamp')
                    if timestamp and (now - timestamp).days <= 7:
                        old_score = portfolio.get('score', 0)
                        change_7_days = (score - old_score) / old_score if old_score else 0
                        user_data['portfolio_metadata'][portfolio_name]['ranks']['change_7_days'] = change_7_days
                        user_changes_7_days[portfolio_name].append((user_data, change_7_days))
                    if timestamp and (now - timestamp).days <= 30:
                        old_score = portfolio.get('score', 0)
                        change_30_days = (score - old_score) / old_score if old_score else 0
                        user_data['portfolio_metadata'][portfolio_name]['ranks']['change_30_days'] = change_30_days
                        user_changes_30_days[portfolio_name].append((user_data, change_30_days))
                        break

    # Sort users by score in descending order and assign ranks for each portfolio
    for portfolio_name, scores in user_scores.items():
        scores.sort(key=lambda x: x[1], reverse=True)
        for i, (user_data, score) in enumerate(scores, start=1):
            user_data['portfolio_metadata'][portfolio_name]['ranks']['rank'] = i
            # Also store the rank in the historical.portfolios[portfolio][0].rank field
            historical_portfolios = user_data['historical']['portfolios']
            portfolios = historical_portfolios.get(portfolio_name, [])
            if portfolios:
                portfolios[0]['rank'] = i

    # Sort users by 7-day change in descending order and assign ranks
    for portfolio_name, changes in user_changes_7_days.items():
        changes.sort(key=lambda x: x[1], reverse=True)
        for i, (user_data, change) in enumerate(changes, start=1):
            user_data['portfolio_metadata'][portfolio_name]['ranks']['change_7_days_rank'] = i
            # Also store the rank and change in the historical.portfolios[portfolio][0].change_7_days_rank field
            historical_portfolios = user_data['historical']['portfolios']
            portfolios = historical_portfolios.get(portfolio_name, [])
            if portfolios:
                portfolios[0]['change_7_days_rank'] = i
                portfolios[0]['change_7_days'] = user_data['portfolio_metadata'][portfolio_name]['ranks']['change_7_days']

    # Sort users by 30-day change in descending order and assign ranks
    for portfolio_name, changes in user_changes_30_days.items():
        changes.sort(key=lambda x: x[1], reverse=True)
        for i, (user_data, change) in enumerate(changes, start=1):
            user_data['portfolio_metadata'][portfolio_name]['ranks']['change_30_days_rank'] = i
            # Also store the rank and change in the historical.portfolios[portfolio][0].change_30_days_rank field
            historical_portfolios = user_data['historical']['portfolios']
            portfolios = historical_portfolios.get(portfolio_name, [])
            if portfolios:
                portfolios[0]['change_30_days_rank'] = i
                portfolios[0]['change_30_days'] = user_data['portfolio_metadata'][portfolio_name]['ranks']['change_30_days']
    return new_users_data
                
def post_to_db(new_users_data):
    count = 0
    batchsize = 100
    for i in range(0, len(new_users_data), batchsize):
        batch = new_users_data[i:i+batchsize]
        bulk_requests = []
        for user in batch:
            count = count + 1
            portfolio_to_push = {}
            update_fields = {}
            for key in user['historical']['portfolios']:
                def str_to_datetime(timestamp_as_str):
                    if isinstance(timestamp_as_str, datetime):
                        return timestamp_as_str
                    return datetime.strptime(timestamp_as_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                timestamp_as_dt = user['historical']['portfolios'][f'{key}'][0]['timestamp']
                user['historical']['portfolios'][f'{key}'][0]['timestamp'] = str_to_datetime(
                    timestamp_as_dt)
                portfolio_to_push[f'historical.portfolios.{key}'] = {
                    '$each': [
                        user['historical']['portfolios'][f'{key}'][0],
                    ],
                    '$position': 0
                }
                ranks = user['portfolio_metadata'].get(key, {}).get('ranks', {})
                update_fields[f'portfolio_metadata.{key}.ranks'] = ranks
            bulk_requests.append(UpdateOne({'uid': user['uid']}, {
                '$push': portfolio_to_push,
                '$set': update_fields
            }))
        collection.bulk_write(bulk_requests)
        print(f'{count} users were updated!')
        time.sleep(1)
    new_users_data.clear()


def update_user_snapshot():
    print('started batch updating users')
    start_backend_job(collection)
    all_users = get_all_users(items_per_page=100)
    print('finished getting user info')
    token_list_sets = create_token_list_sets_to_update(all_users)
    curent_token_data = get_current_token_data(token_list_sets)
    run_calcs_and_update_user(all_users, curent_token_data)
    updated_user_data = calc_ranks_and_update_user(all_users)
    # * TODO: This would be where we take a snapshot and create a user_top_snapshot collection. It would be updated at this moment.
    print('posting')
    post_to_db(updated_user_data)
    end_backend_job(collection)
    print('finished batch updating users')


# update_user_snapshot()
