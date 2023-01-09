
# * Run once a day to update token timestamp - call get_token_timestamp_and_post_concurrently(token_id_list)
import os
from operator import index
import requests
import pandas as pd
import numpy as np
import time
import random
import json

mongo_base_url = os.getenv(host=os.getenv('MONGO_DB_SRV'), connect=False)


def get_token_current_metadata():
    r = requests.get(f'{mongo_base_url}/tokens', timeout=600)
    return r.json()


def post_to_substring_db(ds):
    headers = {'Content-type': 'application/json'}
    r = requests.post(f'{mongo_base_url}/substr-tokens',
                      data=ds, headers=headers)
    print(r)


def reduce_data_and_post(table):
    for item in table:
        ds = {}
        ds["coingecko_id"] = item.get('coingecko_id', '')
        # ds["symbol"] = item.get('symbol', '')
        # ds["name"] = item.get("name", '')
        ds["image"] = item.get("image", '')
        ds["market_cap_rank"] = item.get("market_cap_rank", '')
        ds["degen_rank"] = item.get("degen_rank", '')
        ds["iterator"] = [item.get("name", ''), item.get("symbol", '')]
        post_to_substring_db(json.dumps(ds))


def get_token_substr_data_and_post_concurrently():
    print('beginning parse through token list')
    table = get_token_current_metadata()
    reduce_data_and_post(table)
    print('done')


get_token_substr_data_and_post_concurrently()


# * Run once a day to insert top token document - call get_token_timestamp_and_post_concurrently(token_id_list)

# # * Run once a day to update token timestamp - call get_token_timestamp_and_post_concurrently(token_id_list)
# import os
# from operator import index
# import requests
# import pandas as pd
# import numpy as np
# import time
# import random
# import json

mongo_base_url = os.getenv('MONGO_DB_BASE_URL')


# def get_token_current_metadata():
#     r = requests.get(f'{mongo_base_url}/tokens', timeout=600)
#     return r.json()


# def post_to_substring_db(ds):
#     headers = {'Content-type': 'application/json'}
#     r = requests.post(f'{mongo_base_url}/substr-tokens',
#                       data=ds, headers=headers)
#     print(r)


# def reduce_data_and_post(table):
#     for item in table:
#         ds = {}
#         ds["coingecko_id"] = item.get('coingecko_id', '')
#         ds["symbol"] = item.get('symbol', '')
#         ds["name"] = item.get("name", '')
#         ds["image"] = item.get("image", '')
#         ds["market_cap_rank"] = item.get("market_cap_rank", '')
#         ds["degen_rank"] = item.get("degen_rank", '')
#         post_to_substring_db(json.dumps(ds))


# def get_token_substr_data_and_post_concurrently():
#     print('beginning parse through token list')
#     table = get_token_current_metadata()
#     reduce_data_and_post(table)
#     print('done')


# get_token_substr_data_and_post_concurrently()


# # * Run once a day to insert top token document - call get_token_timestamp_and_post_concurrently(token_id_list)
