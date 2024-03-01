import os
from flask import Blueprint
from ...schedulers.functions.get_token_timestamp import get_token_timestamp_and_post_concurrently, get_token_list

import datetime as dt
import pytz
import requests

coingecko_base_url = os.getenv('COINGECKO_BASE_URL')

token_timeseries_cron = Blueprint('token_timeseries_cron', __name__,
                                  template_folder='templates')


def get_token_list():
    output = []
    headers = {
        'x-cg-pro-api-key': os.getenv('COINGECKO_API_KEY'),
    }
    r = requests.get(f'{coingecko_base_url}/coins/list', headers=headers)
    for token_object in r.json():
        output.append(token_object['id'])
    return output

# token_id_list = get_token_list()


@token_timeseries_cron.route("/tasks/token-timeseries-cron", methods=["GET"])
def get_token_timeseries_cron():
    print('Token Timestamp Scheduler Started')
    get_token_timestamp_and_post_concurrently(get_token_list())
    # get_token_timestamp_and_post_concurrently(token_id_list)
    print(
        f'Token Timestamp Scheduler Finished at: {dt.datetime.now(pytz.utc)}')
    return 'Token timeseries cron successful'

# curl -H "x-cg-pro-api-key: COINGECKO_API_KEY" "https://api.coingecko.com/api/v3/coins/list" #* curl request to get the list of tokens
# curl -s -H "x-cg-pro-api-key: COINGECKO_API_KEY" "https://api.coingecko.com/api/v3/coins/list" | jq '. | length' #* curl request to get the length of the list of tokens