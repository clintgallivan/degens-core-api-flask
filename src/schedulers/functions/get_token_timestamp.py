
# * Run once a day to update token timestamp - call get_token_timestamp_and_post_concurrently(token_id_list)
import os
import requests
import pandas as pd
import numpy as np
import time
import random
import json
# from datetime import date
# import datetime as dt
# import pytz
coingecko_base_url = os.getenv('COINGECKO_BASE_URL')
mongo_base_url = os.getenv('MONGO_DB_BASE_URL')

logs = []


def get_token_list():
    output = []
    r = requests.get(f'{coingecko_base_url}/coins/list')
    for token_object in r.json():
        output.append(token_object['id'])
    return output


def get_token_timestamp_data(token_id):
    print('beginning object build')
    ds = {}
    ds_meta = {}
    value = 'success'
    tryCount = 6
    waitTime = 5
    for i in range(tryCount):
        try:
            r = requests.get(
                f'{coingecko_base_url}/coins/{token_id}', timeout=waitTime)
            # print(r)
            r.raise_for_status()

            result = r.json()

            # * meta db update
            ds_meta["coingecko_id"] = result.get('id', '')
            ds_meta["symbol"] = result.get('symbol', '')
            ds_meta["name"] = result.get("name", '')
            ds_meta["platforms"] = (list(result['platforms'].keys()))
            ds_meta["categories"] = result.get('categories', '')
            ds_meta['description'] = result.get(
                'description', '').get('en', '')
            ds_meta["homepage"] = result.get('links', '').get('homepage', '')
            ds_meta["blockchain_site"] = result.get(
                "links", '').get("blockchain_site", '')
            ds_meta["discord"] = result.get("links", '').get("chat_url", '')
            ds_meta["medium"] = result.get(
                "links", '').get("announcement_url", '')
            if check_if_value(result.get("links", '').get("twitter_screen_name", '')):
                ds_meta["twitter"] = "https://twitter.com/" + \
                    result.get("links", '').get("twitter_screen_name", '')
            else:
                ds_meta["twitter"] = "https://twitter.com/"
            if check_if_value(result.get("links", '').get("telegram_channel_identifier", '')):
                ds_meta["telegram"] = "https://t.me/" + \
                    result.get("links", '').get(
                        "telegram_channel_identifier", '')
            else:
                ds_meta["telegram"] = "https://t.me/"
            ds_meta["reddit"] = result.get(
                "links", '').get("subreddit_url", '')
            ds_meta["github"] = result.get("links", '').get(
                "repos_url", '').get("github", '')
            ds_meta["image"] = result.get("image", '').get("large", '')
            ds_meta["contract_address"] = result.get("contract_address", '')
            ds_meta["sentiment_votes_up_percent"] = result.get(
                "sentiment_votes_up_percentage", '')
            ds_meta["sentiment_votes_down_percent"] = result.get(
                "sentiment_votes_down_percentage", '')
            # ds_meta["price"] = result.get('market_data', {}).get(
            #     'current_price', {}).get('usd', '')
            # ds_meta["market_cap"] = result.get('market_data', {}).get(
            #     'market_cap', {}).get('usd', '')
            ds_meta["market_cap_rank"] = result.get("market_cap_rank", '')
            ds_meta["coingecko_rank"] = result.get("coingecko_rank", '')
            ds_meta["coingecko_score"] = result.get("coingecko_score", '')
            ds_meta["dev_score"] = result.get("developer_score", '')
            ds_meta["community_score"] = result.get("community_score", '')
            ds_meta["liquidity_score"] = result.get("liquidity_score", '')
            ds_meta["public_interest_score"] = result.get(
                "public_interest_score", '')
            # ds_meta["community_data"] = result.get("community_data", {})
            # ds_meta["developer_data"] = result.get("developer_data", {})

          # * timeseries db update
            ds["coingecko_id"] = result.get('id', '')
            ds["symbol"] = result.get('symbol', '')
            ds["name"] = result.get("name", '')
            ds["price"] = result.get('market_data', {}).get(
                'current_price', {}).get('usd', '')
            ds["market_cap"] = result.get('market_data', {}).get(
                'market_cap', {}).get('usd', '')
            ds["market_cap_rank"] = result.get("market_cap_rank", '')
            ds["coingecko_rank"] = result.get("coingecko_rank", '')
            ds["coingecko_score"] = result.get("coingecko_score", '')
            ds["dev_score"] = result.get("developer_score", '')
            ds["community_score"] = result.get("community_score", '')
            ds["liquidity_score"] = result.get("liquidity_score", '')
            ds["public_interest_score"] = result.get(
                "public_interest_score", '')
            ds["community_data"] = result.get("community_data", {})
            ds["developer_data"] = result.get("developer_data", {})
            print('object caputured')

        except requests.exceptions.Timeout as e:
            if i < tryCount - 2:
                print('Timeout error, trying again...', e)
                time.sleep(2)
                continue
            elif i < tryCount - 1:
                print('Timeout error, trying once more...', e)
                time.sleep(5)
                waitTime = 63
                continue
            else:
                value = 'failure'
                print(f"Aborting Script, failed on id: '{token_id}'", e)
                raise
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            if code in [404]:
                if i < 1:
                    print(f"{token_id} not found...", e)
                    time.sleep(2)
                    continue
                elif i >= 1:
                    print(f"{token_id} not found, moving on...", e)
            else:
                if i < tryCount - 2:
                    print("Failure, trying again...", e)
                    time.sleep(2)
                    continue
                elif i < tryCount - 1:
                    print('Timeout error', e)
                    print("Failure, trying last time...", e)
                    time.sleep(5)
                    continue
                else:
                    value = 'failure'
                    print(f"Aborting Script, failed on id: '{token_id}';", e)
                    raise
        except requests.exceptions.ConnectionError as e:
            if i < tryCount - 3:
                print('Connection Error, trying again...', e)
                time.sleep(.01)
                continue
            if i < tryCount - 2:
                print('Connection Error, trying again...', e)
                time.sleep(2)
                continue
            elif i < tryCount - 1:
                print('Connection Error, trying once more...', e)
                time.sleep(5)
                waitTime = 63
                continue
            else:
                value = 'failure'
                print(f"Aborting Script, failed on id: '{token_id}'", e)
                raise
        break
    return [value, json.dumps(ds), json.dumps(ds_meta)]


def check_if_value(result_key):
    if result_key != None:
        return True
    else:
        return False


def post_to_db(ds):
    headers = {'Content-type': 'application/json'}
    r = requests.post(f'{mongo_base_url}/token-timeseries',
                      data=ds, headers=headers)


def post_to_meta_db(ds):
    headers = {'Content-type': 'application/json'}
    r = requests.post(f'{mongo_base_url}/update-token',
                      data=ds, headers=headers)


def get_token_timestamp_and_post_concurrently(token_id_list):
    # timestamp = date.today().strftime("%m-%d-%YT%H:%M:%S")
    # timestamp = dt.datetime.now(pytz.utc)
    # logs = []
    print('beginning loop through token list')
    for token_id in token_id_list:

        ds = get_token_timestamp_data(token_id)
        # print(ds)
        if ds[0] == 'failure':
            print(ds)
            print('not posting object to db')
            return
        else:
            print(ds)
            print('posting to db')
            post_to_db(ds[1])
            post_to_meta_db(ds[2])
            print('posted')
        time.sleep(1.4)
    print(logs)
    # logs = ''
    return


# * Run once a day to update token timestamp - call get_token_timestamp_and_post_concurrently(token_id_list)

# # * Run once a day to update token timestamp - call get_token_timestamp_and_post_concurrently(token_id_list)
# import os
# import requests
# import pandas as pd
# import numpy as np
# import time
# import random
# import json
# # from datetime import date
# # import datetime as dt
# # import pytz
# coingecko_base_url = os.getenv('COINGECKO_BASE_URL')
# mongo_base_url = os.getenv('MONGO_DB_BASE_URL')

# logs = []


# def get_token_list():
#     output = []
#     r = requests.get(f'{coingecko_base_url}/coins/list')
#     for token_object in r.json():
#         output.append(token_object['id'])
#     return output


# def get_token_timestamp_data(token_id):
#     print('beginning object build')
#     ds = {}
#     value = 'success'
#     tryCount = 6
#     waitTime = 5
#     for i in range(tryCount):
#         try:
#             r = requests.get(
#                 f'{coingecko_base_url}/coins/{token_id}', timeout=waitTime)
#             # print(r)
#             r.raise_for_status()

#             result = r.json()
#             ds["coingecko_id"] = result.get('id', '')
#             ds["symbol"] = result.get('symbol', '')
#             ds["name"] = result.get("name", '')
#             ds["price"] = result.get('market_data', {}).get(
#                 'current_price', {}).get('usd', '')
#             ds["market_cap"] = result.get('market_data', {}).get(
#                 'market_cap', {}).get('usd', '')
#             ds["market_cap_rank"] = result.get("market_cap_rank", '')
#             ds["coingecko_rank"] = result.get("coingecko_rank", '')
#             ds["coingecko_score"] = result.get("coingecko_score", '')
#             ds["dev_score"] = result.get("developer_score", '')
#             ds["community_score"] = result.get("community_score", '')
#             ds["liquidity_score"] = result.get("liquidity_score", '')
#             ds["public_interest_score"] = result.get(
#                 "public_interest_score", '')
#             ds["community_data"] = result.get("community_data", {})
#             ds["developer_data"] = result.get("developer_data", {})
#             print('object caputured')

#         except requests.exceptions.Timeout as e:
#             if i < tryCount - 2:
#                 print('Timeout error, trying again...', e)
#                 time.sleep(2)
#                 continue
#             elif i < tryCount - 1:
#                 print('Timeout error, trying once more...', e)
#                 time.sleep(5)
#                 waitTime = 63
#                 continue
#             else:
#                 value = 'failure'
#                 print(f"Aborting Script, failed on id: '{token_id}'", e)
#                 raise
#         except requests.exceptions.HTTPError as e:
#             code = e.response.status_code
#             if code in [404]:
#                 if i < 1:
#                     print(f"{token_id} not found...", e)
#                     time.sleep(2)
#                     continue
#                 elif i >= 1:
#                     print(f"{token_id} not found, moving on...", e)
#             else:
#                 if i < tryCount - 2:
#                     print("Failure, trying again...", e)
#                     time.sleep(2)
#                     continue
#                 elif i < tryCount - 1:
#                     print('Timeout error', e)
#                     print("Failure, trying last time...", e)
#                     time.sleep(5)
#                     continue
#                 else:
#                     value = 'failure'
#                     print(f"Aborting Script, failed on id: '{token_id}';", e)
#                     raise
#         except requests.exceptions.ConnectionError as e:
#             if i < tryCount - 3:
#                 print('Connection Error, trying again...', e)
#                 time.sleep(.01)
#                 continue
#             if i < tryCount - 2:
#                 print('Connection Error, trying again...', e)
#                 time.sleep(2)
#                 continue
#             elif i < tryCount - 1:
#                 print('Connection Error, trying once more...', e)
#                 time.sleep(5)
#                 waitTime = 63
#                 continue
#             else:
#                 value = 'failure'
#                 print(f"Aborting Script, failed on id: '{token_id}'", e)
#                 raise
#         break
#     return [value, json.dumps(ds)]


# def post_to_db(ds):
#     headers = {'Content-type': 'application/json'}
#     r = requests.post(f'{mongo_base_url}/token-timeseries',
#                       data=ds, headers=headers)

# def post_to_meta_db(ds):
#     headers = {'Content-type': 'application/json'}
#     r = requests.post(f'{mongo_base_url}/update-token',
#                       data=ds, headers=headers)


# def get_token_timestamp_and_post_concurrently(token_id_list):
#     # timestamp = date.today().strftime("%m-%d-%YT%H:%M:%S")
#     # timestamp = dt.datetime.now(pytz.utc)
#     # logs = []
#     print('beginning loop through token list')
#     for token_id in token_id_list:

#         ds = get_token_timestamp_data(token_id)
#         # print(ds)
#         if ds[0] == 'failure':
#             print(ds)
#             print('not posting object to db')
#             return
#         else:
#             print(ds)
#             print('posting to db')
#             post_to_db(ds[1])
#             post_to_meta_db(ds[1])
#             print('posted')
#         time.sleep(1.4)
#     print(logs)
#     # logs = ''
#     return


# # * Run once a day to update token timestamp - call get_token_timestamp_and_post_concurrently(token_id_list)
