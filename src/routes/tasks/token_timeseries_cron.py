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
    r = requests.get(f'{coingecko_base_url}/coins/list')
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
