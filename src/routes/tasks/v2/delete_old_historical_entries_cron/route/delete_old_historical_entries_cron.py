import os
from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..functions.handler import handler

import datetime as dt
import pytz
import requests


delete_old_historical_entries_cron = Blueprint('delete_old_historical_entries_cron', __name__,
                                  template_folder='templates')

@delete_old_historical_entries_cron.route("/tasks/v2/delete-old-historical-entries-cron", methods=["GET"])
@jwt_required()
def get_delete_old_historical_entries_cron():
    print(f'Clean tokens-timeseries Cron Started at: {dt.datetime.now(pytz.utc)}')
    handler()
    print(
        f'Clean tokens-timeseries Cron Finished at: {dt.datetime.now(pytz.utc)}')
    return 'Clean tokens-timeseries Cron successful'
