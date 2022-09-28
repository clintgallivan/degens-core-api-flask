from flask import Blueprint
from ...schedulers.functions.get_token_timestamp import get_token_timestamp_and_post_concurrently, get_token_list

import datetime as dt
import pytz

token_timeseries_cron = Blueprint('token_timeseries_cron', __name__,
                                  template_folder='templates')

token_id_list = get_token_list()


@token_timeseries_cron.route("/tasks/token-timeseries-cron", methods=["GET"])
def get_token_timeseries_cron():
    print('Token Timestamp Scheduler Started')
    get_token_timestamp_and_post_concurrently(token_id_list)
    print(
        f'Token Timestamp Scheduler Finished at: {dt.datetime.now(pytz.utc)}')

    return 'Token timeseries cron successful'
