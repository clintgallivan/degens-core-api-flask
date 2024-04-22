import os
from flask import Blueprint
from flask_jwt_extended import jwt_required
# from ....schedulers.functions.get_token_timestamp import get_token_timestamp_and_post_concurrently, get_token_list
from ..functions.handler import handler

import datetime as dt
import pytz
import requests


jupiter_timeseries_cron = Blueprint('jupiter_timeseries_cron', __name__,
                                  template_folder='templates')

@jupiter_timeseries_cron.route("/tasks/jupiter-timeseries-cron", methods=["GET"])
@jwt_required()
def get_jupiter_timeseries_cron():
    print(f'Jupiter Timeseries Cron Started at: {dt.datetime.now(pytz.utc)}')
    handler()
    print(
        f'Jupiter Timeseries Cron Finished at: {dt.datetime.now(pytz.utc)}')
    return 'Jupiter timeseries cron successful'
